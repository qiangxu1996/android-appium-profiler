import time
import logging
import os

import adb
from .. import app_test
from ..dummy_driver import TouchAction

logger = logging.getLogger(__name__)

IMG_TO_MV = 'IMG_1555.jpg'
ANDROID_PIC_DIR = '/sdcard/Pictures'
ANDROID_DL_DIR = '/sdcard/Download'


class App(app_test.AppTest):
    def __init__(self, **kwargs):
        extra_cap = kwargs.setdefault('extra_cap', {})
        extra_cap.setdefault('noReset', False)
        super().__init__('com.amaze.filemanager.debug',
                         'com.amaze.filemanager.activities.MainActivity',
                         **kwargs)
        self.grant_permissions(['WRITE_EXTERNAL_STORAGE'])
        self.res_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'res', 'amaze')

    def _tap_properties(self, el):
        rect = el.rect
        x = rect['x'] + 800
        y = rect['y'] + rect['height']
        TouchAction(self.driver).tap(x=x, y=y).perform()

    def actions(self):
        for img in os.listdir(self.res_dir):
            adb.push(os.path.join(self.res_dir, img), ANDROID_PIC_DIR, True)
        adb.shell(['mv', ANDROID_PIC_DIR + '/' + IMG_TO_MV, ANDROID_DL_DIR])

        # time.sleep(30)  # cov
        self.may_start_profiler()

        time.sleep(1)
        self.find_element_by_name('Download').click()
        time.sleep(2)
        img_to_mv = self.find_element_by_name(IMG_TO_MV)
        self._tap_properties(img_to_mv)
        time.sleep(1)
        self.find_element_by_name('Cut').click()
        time.sleep(1)
        self.back()
        time.sleep(2)
        self.swipe()
        self.find_element_by_name('Pictures').click()
        time.sleep(2)
        self.swipe('down')
        time.sleep(2)
        self.find_element_by_res_id('paste').click()

        time.sleep(2)
        img_to_del = self.find_element_by_res_id('firstline')
        self._tap_properties(img_to_del)
        time.sleep(1)
        self.find_element_by_name('Delete').click()
        time.sleep(1)
        self.find_element_by_res_id('md_buttonDefaultPositive').click()

        time.sleep(2)
        self.back()
        time.sleep(2)
        self.may_stop_profiler()
