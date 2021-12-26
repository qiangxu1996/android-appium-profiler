import logging
import socket
import time

import adb
from .. import app_test

logger = logging.getLogger(__name__)


class App(app_test.AppTest):
    """
    Start the Vagrant virtual machine on the same machine running the script,
    before running the test
    """
    def __init__(self, **kwargs):
        super().__init__(
            'com.tachibana.downloader', '.ui.main.MainActivity', **kwargs)
        self.grant_permissions(
            ['READ_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STORAGE'])
        ip = socket.getaddrinfo(socket.getfqdn(), None)[0][4][0]
        self._download_link = f'{ip}:8080/100MB.bin'

    def actions(self):
        adb.shell(['rm', '/sdcard/Download/100MB.bin'], check=False)
        self.may_start_profiler()
        time.sleep(1)
        self.find_element_by_res_id('add_fab').click()
        time.sleep(1)
        self.find_element_by_res_id('link').send_keys(self._download_link)
        self.find_element_by_res_id('button1', 'android').click()
        time.sleep(2)
        self.find_element_by_res_id('button2', 'android').click()
        time.sleep(22)
        self.driver.find_element_by_accessibility_id('Completed').click()
        time.sleep(1)
        status = self.find_element_by_res_id('status')
        if '100 MB' not in status.text:
            raise ValueError('Download file size is', status.text)
        time.sleep(1)
        self.may_stop_profiler()
