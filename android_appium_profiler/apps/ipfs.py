import logging
import time

from appium.webdriver.extensions.android.nativekey import AndroidKey

from .. import app_test

logger = logging.getLogger(__name__)


class App(app_test.AppTest):
    def __init__(self, **kwargs):
        extra_cap = kwargs.setdefault('extra_cap', {})
        extra_cap.setdefault('waitForIdleTimeout', 500)
        super().__init__('threads.server', '.MainActivity', **kwargs)
        self.clear_cache()

    def warmup(self):
        self.find_element_by_res_id('action_browser').click()
        time.sleep(1)
        self.find_element_by_res_id('search_src_text')\
            .send_keys('https://en.wikipedia-on-ipfs.org')
        self.driver.press_keycode(AndroidKey.ENTER)
        time.sleep(1)
        self.find_element_by_res_id('action_bookmark').click()

    def actions(self):
        self.find_element_by_res_id('action_bookmarks').click()
        time.sleep(1)
        self.find_element_by_res_id('bookmark_title').click()
        time.sleep(3)
        self.driver.switch_to.context(self.driver.contexts[-1])
        self.may_start_profiler()
        time.sleep(1)
        for res_id in 'mwEA', 'mwEQ', 'mwEg', 'mwFA', 'mwFQ':
            self.driver.find_element_by_id(res_id).click()
            time.sleep(3)
            self.back()
            time.sleep(1)
        self.may_stop_profiler()
