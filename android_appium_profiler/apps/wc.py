import time

from .. import app_test


class App(app_test.AppTest):
    def __init__(self, **kwargs):
        super().__init__(
            'fr.free.nrw.commons', '.auth.LoginActivity', **kwargs)
        self.clear_cache()

    def warmup(self):
        for _ in range(4):
            self.swipe('left')
            time.sleep(1)
        self.find_element_by_res_id('finishTutorialButton').click()
        time.sleep(1)
        self.find_element_by_res_id('skip_login').click()
        time.sleep(1)
        self.driver.find_element_by_id('android:id/button1').click()
        time.sleep(5)

    def actions(self):
        self.may_start_profiler()
        for _ in range(4):
            self.swipe()
            time.sleep(2)
            self.find_element_by_res_id('categoryImageView').click()
            time.sleep(4)
            self.back()
            time.sleep(2)
        self.may_stop_profiler()
