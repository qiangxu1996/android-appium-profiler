import logging
import time
from selenium.webdriver.support.wait import WebDriverWait

from .. import app_test

logger = logging.getLogger(__name__)


class App(app_test.AppTest):
    def __init__(self, **kwargs):
        super().__init__('org.fdroid.fdroid.debug',
                         'org.fdroid.fdroid.views.main.MainActivity',
                         **kwargs)
        self.clear_cache()

    def warmup(self):
        WebDriverWait(self.driver, 90, 5)\
            .until(lambda d: d.find_element_by_id(self.res_id('summary')))
        time.sleep(5)

    def actions(self):
        self.may_start_profiler()
        time.sleep(1)
        self.find_element_by_name('Categories').click()
        time.sleep(8)
        # time.sleep(10)  # cov
        for i in range(3):
            self.find_elements_by_res_id('summary')[i].click()
            time.sleep(4)
            self.swipe()
            time.sleep(2)
            # time.sleep(10)  # cov
            self.back()
            time.sleep(2)
        self.may_stop_profiler()
