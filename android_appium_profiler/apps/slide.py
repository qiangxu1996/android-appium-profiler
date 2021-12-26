import logging
import time

from .. import app_test
from ..dummy_driver import TouchAction

logger = logging.getLogger(__name__)


class App(app_test.AppTest):
    def __init__(self, **kwargs):
        extra_cap = kwargs.setdefault('extra_cap', {})
        extra_cap.setdefault('noReset', False)
        extra_cap.setdefault('autoGrantPermissions', True)
        kwargs.setdefault('cov_activity',
                          'me.ccrama.redditslide.Activities.Tutorial')
                          # 'me.ccrama.redditslide.Activities.MainActivity')  # cov
        super().__init__('me.ccrama.redditslide.debug',
                         'me.ccrama.redditslide.Activities.Slide',
                         **kwargs)

    def _tap_title(self):
        rect = self.find_element_by_res_id('title').rect
        x = rect['x'] + 1
        y = rect['y'] + rect['height'] - 1
        TouchAction(self.driver).tap(x=x, y=y).perform()

    def _view_thread(self):
        self.find_element_by_res_id('title').click()
        time.sleep(5)
        self.back()

    def view_posts(self):
        self.find_element_by_res_id('title').click()
        time.sleep(1)
        self.back()
        time.sleep(3)
        self.back()

        time.sleep(1)
        self.driver.find_element_by_accessibility_id('all').click()
        time.sleep(8)
        self._view_thread()

        time.sleep(1)
        self.driver.find_element_by_accessibility_id('announcements').click()
        time.sleep(8)
        self._view_thread()

    def scan_posts(self):
        for _ in range(5):
            self.swipe()
            time.sleep(3)

    def actions(self):
        self.driver.implicitly_wait(2)
        self.find_element_by_res_id('next').click()
        time.sleep(1)
        # return  # cov
        self.find_element_by_res_id('next').click()

        time.sleep(12)
        # time.sleep(8)  # cov
        self.may_start_profiler()
        self.view_posts()
        time.sleep(5)
        self.may_stop_profiler()
