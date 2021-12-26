import logging

from appium import webdriver
from appium.webdriver.common import touch_action
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class DummyList(dict):
    def __init__(self, original: list):
        super().__init__()
        self._original = original

    def __missing__(self, key):
        return self._original[0]


class DummyDriver(webdriver.Remote):
    DUMMY_APP_PACKAGE = 'edu.purdue.dsnl.dummy'
    DUMMY_APP_ACTIVITY = '.MainActivity'
    _DUMMY_ID = DUMMY_APP_PACKAGE + ':id/dummy'
    _DUMMY_ANDROID_UIAUTOMATOR = f'new UiSelector().text("dummy")'
    _DUMMY_ACCESSIBILITY_ID = 'dummy'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dummy = False
        self._rect = None

    def find_element(self, by=By.ID, value=None):
        value = self._may_dummy_value(by, value)
        return super().find_element(by, value)

    def find_elements(self, by=By.ID, value=None):
        value = self._may_dummy_value(by, value)
        elements = super().find_elements(by, value)
        if self._dummy:
            return DummyList(elements)
        else:
            return elements

    def get_window_rect(self):
        if not self._rect:
            self._rect = super().get_window_rect()
        return self._rect

    def dummy(self, dummy: bool):
        self._dummy = dummy

    def is_dummy(self):
        return self._dummy

    def _may_dummy_value(self, by, value):
        if self._dummy:
            return self._dummy_value(by, value)
        else:
            return value

    @staticmethod
    def _dummy_value(by, value):
        if by == By.ID:
            return DummyDriver._DUMMY_ID
        elif by == By.ANDROID_UIAUTOMATOR:
            return DummyDriver._DUMMY_ANDROID_UIAUTOMATOR
        elif by == By.ACCESSIBILITY_ID:
            return DummyDriver._DUMMY_ACCESSIBILITY_ID
        else:
            logger.warning(f'{by} {value} is not replaced with dummy value')
            return value


class TouchAction(touch_action.TouchAction):
    def __init__(self, driver):
        super().__init__(driver)
        self._dummy = driver.is_dummy()

    def tap(self, element=None, x=None, y=None, count=1):
        if self._dummy:
            rect = self._driver.get_window_rect()
            x = rect['width'] // 2
            y = rect['height'] // 2
        return super().tap(element, x, y, count)
