import logging
import time

import adb
from .. import app_test

logger = logging.getLogger(__name__)


class App(app_test.AppTest):
    def __init__(self, **kwargs):
        extra_cap = kwargs.setdefault('extra_cap', {})
        extra_cap.setdefault('noReset', False)
        super().__init__('ws.xsoh.etar.debug', 'com.android.calendar.AllInOneActivity', **kwargs)
        self.grant_permissions(
            ['READ_CALENDAR', 'WRITE_CALENDAR', 'READ_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STORAGE', 'READ_CONTACTS'])
        adb.shell(['content', 'delete', '--uri',
                   '"content://com.android.calendar/calendars'
                   '?caller_is_syncadapter=true&account_name=Offline%20Calendar&account_type=LOCAL"'])

    def actions(self):
        self.driver.find_element_by_accessibility_id('Navigate up').click()
        time.sleep(1)
        self.find_element_by_res_id('action_settings').click()
        time.sleep(1)
        self.find_element_by_name('Add offline calendar').click()
        time.sleep(1)
        self.find_element_by_res_id('offline_calendar_name').send_keys('cal')
        self.find_element_by_res_id('button1', 'android').click()
        time.sleep(1)
        self.back()
        time.sleep(1)

        self.may_start_profiler()
        time.sleep(1)
        for i in range(1, 4):
            self.find_element_by_res_id('floating_action_button').click()
            time.sleep(1)
            self.driver.hide_keyboard()
            time.sleep(1)
            self.send_keys(self.find_element_by_res_id('title'), f'Event{i}', 0.1)
            self.find_element_by_res_id('is_all_day').click()
            self.find_element_by_res_id('action_done').click()
            time.sleep(1)
        self.may_stop_profiler()
