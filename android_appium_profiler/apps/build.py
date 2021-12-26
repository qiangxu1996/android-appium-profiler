import logging
import time

from .. import app_test

logger = logging.getLogger(__name__)


class App(app_test.AppTest):
    def __init__(self, **kwargs):
        super().__init__('de.storchp.fdroidbuildstatus', '.MainActivity', **kwargs)

    def warmup(self):
        time.sleep(3)

    def actions(self):
        self.may_start_profiler()
        time.sleep(1)
        for _ in range(5):
            self.find_element_by_res_id('app_name').click()
            time.sleep(3)
            self.back()
            time.sleep(1)
            self.swipe()
            time.sleep(1)
        self.may_stop_profiler()
