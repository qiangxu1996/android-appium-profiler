import base64
import logging
import os
import pathlib
import string
import tempfile
import time

from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.common.exceptions import WebDriverException

import adb
import dummy_driver
try:
    import measure
except ImportError:
    pass
try:
    from ftrace_energy import FtraceEnergy
except ImportError:
    pass

logger = logging.getLogger(__name__)

PROFILE_LOG_MAGIC = '`~-_=+'

INTERNAL_DATA = pathlib.PurePosixPath('/data/data')
EXTERNAL_DATA = pathlib.PurePosixPath('/sdcard/Android/data')
ANDROID_TMP = '/data/local/tmp'

DEFAULT_CAPABILITIES = {
    'platformName': 'Android',
    'automationName': 'UIAutomator2',
    'noReset': True,
    'newCommandTimeout': 120,
    'adbExecTimeout': 60000,
}


class AppTest:
    def __init__(self, app_package: str, app_activity: str, **kwargs):
        self._capabilities = DEFAULT_CAPABILITIES.copy()

        self._dummy = kwargs.get('dummy', False)
        if self._dummy:
            self._capabilities['appPackage']\
                = dummy_driver.DummyDriver.DUMMY_APP_PACKAGE
            self._capabilities['appActivity']\
                = dummy_driver.DummyDriver.DUMMY_APP_ACTIVITY
        else:
            self._capabilities['appPackage'] = app_package
            self._capabilities['appActivity'] = app_activity

        if not kwargs.get('restart', True):
            self._capabilities['dontStopAppOnReset'] = 'true'

        self._server_port = kwargs.get('server_port', 4723)
        udid = kwargs.get('udid')
        if udid:
            self._capabilities['udid'] = udid
            adb.default_device(udid)

        self._coverage = kwargs.get('coverage')
        if self._coverage:
            self._capabilities['androidCoverage'] \
                = 'edu.purdue.dsnl.appiumcoverage/.CoverageInstrumentation'
            self._capabilities['androidCoverageEndIntent']\
                = 'edu.purdue.dsnl.appiumcoverage.END_EMMA'
            cov_act = kwargs.get('cov_activity')
            if cov_act and not self._dummy:
                self._capabilities['appActivity'] = cov_act

        for k, v in kwargs.get('extra_cap', {}).items():
            self._capabilities[k] = v

        self._init_keycode_map()

        self.package = app_package
        self.driver = None
        self._ftrace = None
        self._ftrace_separate = False
        self._ftrace_file = None
        self._logcat_file = None
        self._screen_record = None
        self._battery = None
        self._init_battery = None

    def warmup(self):
        pass

    def actions(self):
        raise NotImplementedError('Please override it.')

    def cleanup(self):
        pass

    def manual(self, duration=180):
        self.may_start_profiler()
        print('manual start')
        time.sleep(duration)
        print('manual stop')
        self.may_stop_profiler()

    def switch_to_dummy(self):
        self.driver.activate_app('edu.purdue.dsnl.dummy')

    def run(self, **kwargs):
        ports = []
        try:
            warmup = kwargs.get('warmup', False)
            if warmup:
                self._capabilities.pop('noReset', None)

            if 'mjpegServerPort' not in self._capabilities:
                port = self._next_avail_port(9200)
                self._capabilities['mjpegServerPort'] = port
                ports.append(port)
            if 'systemPort' not in self._capabilities:
                port = self._next_avail_port(8200)
                self._capabilities['systemPort'] = port
                ports.append(port)

            self._logcat_file = kwargs.get('logcat')
            if self._logcat_file:
                adb.command(['logcat', '--clear'])

            self.driver = dummy_driver.DummyDriver(
                f'http://127.0.0.1:{self._server_port}/wd/hub',
                self._capabilities)
            self.driver.dummy(self._dummy)

            self._screen_record = kwargs.get('screen_record')
            if kwargs.get('battery', False):
                self._battery = measure.BatteryMeasure()
            if kwargs.get('ftrace', False):
                self._ftrace_separate = kwargs.get('ftrace_separate', False)
                self._ftrace_file = kwargs.get('ftrace_file')
                self._ftrace = FtraceEnergy()
                self._ftrace.prepare()
            time.sleep(2)

            logger.debug('test starts.')
            if warmup:
                self.warmup()
            self.actions()
        except WebDriverException:
            self.driver.save_screenshot(
                'except-' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.png')
            raise
        finally:
            self.cleanup()
            if self.driver:
                self.driver.quit()
            self.driver = None
            for p in ports:
                self._release_port(p)

        self.may_pull_coverage()

    def may_start_profiler(self):
        logger.info(PROFILE_LOG_MAGIC)
        if self._ftrace:
            self._ftrace.start()
        if self._screen_record:
            self.driver.start_recording_screen()
        if self._battery:
            self._init_battery = self._battery.measure()

    def may_stop_profiler(self):
        logger.info(PROFILE_LOG_MAGIC)
        if self._battery:
            print(self._init_battery - self._battery.measure())
        if self._ftrace:
            energy = self._ftrace.stop_and_calc(
                self._ftrace_separate, self._ftrace_file)
            if self._ftrace_separate:
                for k, v in energy.items():
                    print(k, v)
            else:
                print(energy)
        if self._logcat_file:
            log = adb.command(['logcat', '-d']).stdout
            with open(self._logcat_file, 'w', encoding='utf-8') as f:
                f.write(log)
        if self._screen_record:
            video = self.driver.stop_recording_screen()
            with open(self._screen_record, 'wb') as out:
                out.write(base64.b64decode(video))

    def may_pull_coverage(self):
        if self._coverage:
            adb.pull(f'/sdcard/Android/data/{self.package}/files/coverage.ec',
                     self._coverage)

    def get_pid(self) -> int:
        output = adb.shell(['ps']).stdout
        for line in output.splitlines():
            if line.endswith(self.package):
                return int(line.split()[1])
        raise ValueError(f'PID of {self.package} not found.')

    def grant_permissions(self, perm):
        self._capabilities.setdefault('autoGrantPermissions', True)
        for p in perm:
            adb.shell(['pm', 'grant', self.package, f'android.permission.{p}'])

    def clear_cache(self):
        adb.shell(['run-as', self.package,
                   'rm', '-rf', f'/data/data/{self.package}/cache'])

    def swipe(self, direction: str = 'up'):
        size = self.driver.get_window_size()
        w = size['width']
        h = size['height']
        hw = w // 2
        hh = h // 2
        qw = w // 4
        qh = h // 4
        if direction == 'up':
            self.driver.swipe(hw, 3 * qh, hw, qh)
        elif direction == 'down':
            self.driver.swipe(hw, qh, hw, 3 * qh)
        elif direction == 'left':
            self.driver.swipe(3 * qw, hh, qw, hh)
        elif direction == 'right':
            self.driver.swipe(qw, hh, 3 * qw, hh)

    def tap_center(self):
        size = self.driver.get_window_size()
        x = size['width'] // 2
        y = size['height'] // 2
        dummy_driver.TouchAction(self.driver).tap(x=x, y=y).perform()

    def back(self):
        self.driver.press_keycode(AndroidKey.BACK)

    def home(self):
        self.driver.press_keycode(AndroidKey.HOME)

    @staticmethod
    def send_keys(element, keys, interval=0):
        for i in range(len(keys)):
            element.send_keys(keys[:i+1])
            time.sleep(interval)

    def _init_keycode_map(self):
        letter_keys = range(AndroidKey.A, AndroidKey.Z + 1)
        self._key2keycode = dict(zip(string.ascii_lowercase, letter_keys))
        self._key2keycode.update(zip(string.ascii_uppercase, letter_keys))
        self._key2keycode.update({
            '.': AndroidKey.PERIOD, ' ': AndroidKey.SPACE,
            '\n': AndroidKey.ENTER, ':': AndroidKey.SEMICOLON,
            '/': AndroidKey.SLASH, '_': AndroidKey.MINUS
        })

    @staticmethod
    def _shift(key):
        shift_symbols = {':', '_'}
        if key in string.ascii_uppercase or key in shift_symbols:
            return True
        else:
            return False

    def press_keycode(self, keys: str):
        for k in keys:
            mod = 1 if self._shift(k) else None
            self.driver.press_keycode(self._key2keycode[k], mod)

    def res_id(self, suffix, package=None):
        if package is None:
            package = self.package
        return package + ':id/' + suffix

    def find_element_by_name(self, name: str):
        return self.driver.find_element_by_android_uiautomator(
            f'new UiSelector().text("{name}")')

    def find_element_by_res_id(self, suffix, package=None):
        return self.driver.find_element_by_id(self.res_id(suffix, package))

    def find_elements_by_res_id(self, suffix, package=None):
        return self.driver.find_elements_by_id(self.res_id(suffix, package))

    @staticmethod
    def _next_avail_port(port: int) -> int:
        while True:
            try:
                AppTest._lock_file_name(port).touch(exist_ok=False)
                break
            except FileExistsError:
                port += 1
        return port

    @staticmethod
    def _release_port(port: int):
        os.remove(AppTest._lock_file_name(port))

    @staticmethod
    def _lock_file_name(port: int):
        return pathlib.Path(tempfile.gettempdir(), f'appium-port-{port}.lock')

    @staticmethod
    def _copy_internal(src: str, dest: str, restore: bool = False):
        logger.debug(f'Before copying {src} to {dest}: %s',
                     adb.shell(['ls', '-lZ', str(INTERNAL_DATA)], True).stdout)
        adb.shell(['rm', '-rf', dest], True)
        adb.shell(['cp', '-a', src, dest], True)
        if restore:
            adb.shell(['restorecon', '-R', dest], True)
            adb.shell(['rm', '-r', src], True)
        logger.debug(f'After copying {src} to {dest}: %s',
                     adb.shell(['ls', '-lZ', str(INTERNAL_DATA)], True).stdout)

    @staticmethod
    def _copy_external(src: str, dest: str, restore: bool = False):
        adb.shell(['rm', '-rf', dest])
        adb.shell(['cp', '-a', src, dest])
        if restore:
            adb.shell(['rm', '-r', src], True)

    def save_state(self, tag: str):
        internal_data = str(INTERNAL_DATA / self.package)
        internal_data_bak = internal_data + '_' + tag
        self._copy_internal(internal_data, internal_data_bak)

        external_data = str(EXTERNAL_DATA / self.package)
        external_data_bak = external_data + '_' + tag
        self._copy_external(external_data, external_data_bak)

    def restore_state(self, tag: str):
        internal_data = str(INTERNAL_DATA / self.package)
        internal_data_bak = internal_data + '_' + tag
        self._copy_internal(internal_data_bak, internal_data, True)

        external_data = str(EXTERNAL_DATA / self.package)
        external_data_bak = external_data + '_' + tag
        self._copy_external(external_data_bak, external_data, True)
