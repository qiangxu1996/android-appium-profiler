import logging
import time

import adb
from .. import app_test

logger = logging.getLogger(__name__)


class App(app_test.AppTest):
    """
    Manually put the Instagram and Vid Mate APK files in
    /sdcard/Download before start
    """

    def __init__(self, **kwargs):
        super().__init__('com.aefyr.sai.fdroid',
                         'com.aefyr.sai.ui.activities.MainActivity',
                         **kwargs)
        self.grant_permissions(
            ['READ_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STORAGE'])
        adb.shell(['appops', 'set', self.package,
                   'REQUEST_INSTALL_PACKAGES', 'allow'])

    def actions(self):
        adb.command(['uninstall', 'com.instagram.android'], False)
        adb.command(['uninstall', 'com.nemo.vidmate'], False)
        self.may_start_profiler()
        time.sleep(1)
        install_time = (12, 5)
        for i in range(2):
            self.find_element_by_res_id('button_install').click()
            time.sleep(1)
            self.find_element_by_res_id('button_installerx_fp_internal').click()
            time.sleep(1)
            self.find_element_by_name('Download').click()
            time.sleep(1)
            self.find_elements_by_res_id('fname')[i+1].click()
            self.find_element_by_res_id('select').click()
            time.sleep(2)
            self.find_element_by_res_id('button_bottom_sheet_dialog_base_ok')\
                .click()
            time.sleep(1)
            self.find_element_by_res_id('button1', 'android').click()
            # self.find_element_by_res_id(
            #     'ok_button', 'com.android.packageinstaller').click()
            time.sleep(install_time[i])
            self.find_element_by_res_id('button2', 'android').click()
            time.sleep(1)
        self.may_stop_profiler()
