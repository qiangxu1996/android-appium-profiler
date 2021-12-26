import logging
import time

import adb
from .. import app_test
from ..dummy_driver import TouchAction

logger = logging.getLogger(__name__)

INPUT_APP = 'edu.purdue.dsnl.asktest'


class App(app_test.AppTest):
    """
    Build and install INPUT_APP before start
    """

    def __init__(self, **kwargs):
        kwargs.setdefault(
            'cov_activity',
            'com.anysoftkeyboard.ui.settings.MainSettingsActivity')
        super().__init__(
            'com.menny.android.anysoftkeyboard', '.LauncherSettingsActivity',
            **kwargs)
        self.clear_cache()
        self._build_key_table()
        self._ime_activity = self.package + '/.SoftKeyboard'

    def warmup(self):
        adb.shell(['ime', 'enable', self._ime_activity])

    def actions(self):
        adb.shell(['ime', 'set', self._ime_activity])
        self.driver.terminate_app(INPUT_APP)
        self.driver.activate_app(INPUT_APP)
        touch = TouchAction(self.driver)
        time.sleep(1)
        self.may_start_profiler()
        time.sleep(1)
        # time.sleep(10)  # cov
        self.find_element_by_res_id('username', INPUT_APP).click()
        time.sleep(2)
        for a in 'dsnltest\t19@\vgmail\f':
            x, y = self._email_key_coord[a]
            touch.tap(x=x, y=y).perform()
            time.sleep(0.5)
        self.find_element_by_res_id('password', INPUT_APP).click()
        time.sleep(1)
        for a in '10qpalzm,.\n':
            x, y = self._password_key_coord[a]
            touch.tap(x=x, y=y).perform()
            time.sleep(0.5)
        time.sleep(1)
        self.may_stop_profiler()

        username = self.find_element_by_res_id('username', INPUT_APP).text
        if username != 'dsnltest19@gmail.com':
            raise ValueError('Username is', username)
        password = self.find_element_by_res_id('password', INPUT_APP).text
        if password != '••••••••••':
            raise ValueError('Password is', password)

    def _build_key_table(self):
        self._email_key_coord = {
            '\t': (200, 1120), '\v': (900, 1120), '\f': (80, 1680)}
        self._password_key_coord = {
            ',': (380, 1670), '.': (750, 1670), '\n': (1000, 1670)}
        for i, k in enumerate('1234567890'):
            self._email_key_coord[k] = (108 * i + 54, 1240)
            self._password_key_coord[k] = (108 * i + 54, 1120)
        for i, k in enumerate('qwertyuiop'):
            self._email_key_coord[k] = (108 * i + 54, 1240)
            self._password_key_coord[k] = (108 * i + 54, 1240)
        for i, k in enumerate('asdfghjkl'):
            self._email_key_coord[k] = (108 * (i + 1), 1380)
            self._password_key_coord[k] = (108 * (i + 1), 1380)
        for i, k in enumerate('!@#$%^&*()'):
            self._email_key_coord[k] = (108 * i + 54, 1380)
        for i, k in enumerate('zxcvbnm'):
            self._email_key_coord[k] = (108 * (i + 2), 1530)
            self._password_key_coord[k] = (108 * (i + 2), 1530)
