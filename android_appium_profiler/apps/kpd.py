import time

from .. import app_test


class App(app_test.AppTest):
    """
    Manually push keepass.kdbx to /sdcard/keepass before start
    """

    def __init__(self, **kwargs):
        extra_cap = kwargs.setdefault('extra_cap', {})
        extra_cap.setdefault('noReset', False)
        extra_cap.setdefault('autoGrantPermissions', True)
        kwargs.setdefault('cov_activity',
                          'com.keepassdroid.fileselect.FileSelectActivity')
        super().__init__('com.android.keepass', '.KeePass', **kwargs)

    def actions(self):
        self.find_element_by_res_id('open').click()
        time.sleep(1)
        # time.sleep(4)  # cov
        self.find_element_by_res_id('password').send_keys('10qpalzm,.')
        time.sleep(1)
        self.find_element_by_res_id('pass_ok').click()
        time.sleep(2)
        self.may_start_profiler()
        for i in range(8):
            self.find_elements_by_res_id('entry_text')[i].click()
            time.sleep(1)
            self.driver.find_element_by_accessibility_id('More options').click()
            time.sleep(1)
            self.find_element_by_name('Copy Password').click()
            time.sleep(1)
            self.back()
            time.sleep(1)
        self.may_stop_profiler()
