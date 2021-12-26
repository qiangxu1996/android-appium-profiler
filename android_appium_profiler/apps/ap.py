import time
import logging

from .. import app_test

logger = logging.getLogger(__name__)


class App(app_test.AppTest):
    """
    Manually push AntennaPodBackup.db to /sdcard/Download before start
    """

    def __init__(self, **kwargs):
        kwargs.setdefault('cov_activity',
                          'de.danoeh.antennapod.activity.MainActivity')
        super().__init__('de.danoeh.antennapod.debug',
                         'de.danoeh.antennapod.activity.SplashActivity',
                         **kwargs)
        self.clear_cache()

    def play(self):
        def click_play():
            self.driver.find_element_by_id(self.package + ':id/butPlay').click()

        click_play()
        self.may_start_profiler()
        time.sleep(5)
        time.sleep(60)
        self.may_stop_profiler()
        click_play()

    def view_desc(self):
        self.driver.find_element_by_android_uiautomator(
            'new UiSelector()'
            f'.resourceId("{self.package}:id/subscriptions_grid")'
            '.childSelector(new UiSelector().index(0))'
        ).click()

        self.may_start_profiler()
        for i in range(4):
            time.sleep(10)
            episodes = self.driver.find_elements_by_id(
                self.package + ':id/txtvItemname')
            episodes[i].click()
            logger.debug('Click episode')

            time.sleep(15)
            self.back()
            logger.debug('Back')
        self.may_stop_profiler()

    def warmup(self):
        self.find_element_by_res_id('nav_settings').click()
        time.sleep(1)
        self.find_element_by_name('Storage').click()
        time.sleep(1)
        self.swipe()
        time.sleep(1)
        self.find_element_by_name('Database import/export').click()
        time.sleep(1)
        self.find_element_by_res_id('button_import').click()
        time.sleep(1)
        self.driver.find_element_by_id(
            # 'com.google.android.documentsui:id/item_root'
            'com.android.documentsui:id/item_root'
        ).click()
        time.sleep(1)
        self.driver.find_element_by_id('android:id/button1').click()
        time.sleep(3)
        self.driver.find_element_by_accessibility_id('Open menu').click()
        time.sleep(1)
        self.find_element_by_name('Subscriptions').click()

    def actions(self):
        time.sleep(2)
        self.may_start_profiler()
        time.sleep(1)
        for i in range(6):
            self.find_elements_by_res_id('imgvCover')[i].click()
            time.sleep(2)
            self.find_element_by_res_id('container').click()
            time.sleep(2)
            self.back()
            time.sleep(1)
            self.back()
            time.sleep(1)
        self.may_stop_profiler()
