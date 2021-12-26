import logging
import time

from .. import app_test

logger = logging.getLogger(__name__)


class App(app_test.AppTest):
    def __init__(self, **kwargs):
        extra_cap = kwargs.setdefault('extra_cap', {})
        extra_cap.setdefault('noReset', False)
        super().__init__('org.woheller69.weather', '.activities.SplashActivity', **kwargs)

    def actions(self):
        self.may_start_profiler()
        time.sleep(1)
        for city in 'Tokyo', 'Delhi', 'Seoul', 'Shanghai', 'São Paulo':
            self.driver.find_element_by_accessibility_id(city).click()
            time.sleep(3)
            self.swipe()
            time.sleep(1)
            self.swipe()
            time.sleep(1)
        self.may_stop_profiler()
