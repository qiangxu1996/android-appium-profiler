import logging
import time

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait

from .. import app_test

logger = logging.getLogger(__name__)

FILES_APP = 'com.android.documentsui'


class App(app_test.AppTest):
    def __init__(self, **kwargs):
        super().__init__('org.sufficientlysecure.keychain.debug',
                         'org.sufficientlysecure.keychain.ui.MainActivity',
                         **kwargs)

    def warmup(self):
        self.find_element_by_res_id('create_key_create_key_button').click()
        time.sleep(1)
        self.find_element_by_res_id('create_key_next_button').click()
        time.sleep(1)
        self.find_element_by_res_id('create_key_email')\
            .send_keys('dsnltest19@gmail.com')
        time.sleep(1)
        self.find_element_by_res_id('create_key_next_button').click()
        time.sleep(1)
        self.find_element_by_res_id('create_key_next_button').click()
        WebDriverWait(self.driver, 30)\
            .until(lambda x: x.find_element_by_accessibility_id("Open"))

    def actions(self):
        self.driver.find_element_by_accessibility_id('Open').click()
        time.sleep(1)
        self.find_elements_by_res_id('material_drawer_name')[1].click()
        time.sleep(1)
        self.may_start_profiler()
        time.sleep(1)
        self.find_element_by_res_id('encrypt_files').click()
        time.sleep(1)
        self.find_element_by_name('Encrypt to').send_keys('d')
        time.sleep(1)
        self.find_element_by_res_id('key_list_item_data').click()
        time.sleep(1)
        self.find_element_by_res_id('file_list_entry_add').click()
        time.sleep(1)
        # self.driver.find_element_by_id('item_root', FILES_APP).click()
        self.find_element_by_res_id('thumbnail', FILES_APP).click()
        time.sleep(1)
        self.find_element_by_res_id('encrypt_save').click()
        time.sleep(1)
        self.find_element_by_res_id('button1', 'android').click()
        time.sleep(10)
        self.back()
        time.sleep(1)
        self.find_element_by_res_id('decrypt_files').click()
        time.sleep(1)
        self.find_element_by_res_id('thumbnail', FILES_APP).click()
        time.sleep(10)
        self.back()
        time.sleep(1)
        self.may_stop_profiler()

    def cleanup(self):
        self.driver.terminate_app(FILES_APP)
        self.driver.activate_app(FILES_APP)
        time.sleep(2)
        self.driver.find_element_by_accessibility_id('Show roots').click()
        time.sleep(1)
        self.find_element_by_name('Downloads').click()
        time.sleep(1)
        e = self.find_element_by_res_id('title', 'android')
        if e.text == '1.pgp':
            TouchAction(self.driver).long_press(e).perform()
            self.find_element_by_res_id('action_menu_delete', FILES_APP).click()
            time.sleep(1)
            self.find_element_by_res_id('button1', 'android').click()
            time.sleep(5)
