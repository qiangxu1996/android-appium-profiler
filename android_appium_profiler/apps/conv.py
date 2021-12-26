import random
import string
import time

from .. import app_test


class App(app_test.AppTest):
    """
    Manually push the .ceb file to /sdcard/Conversations/Backup before start
    """

    def __init__(self, **kwargs):
        extra_cap = kwargs.setdefault('extra_cap', {})
        extra_cap.setdefault('autoGrantPermissions', True)
        kwargs.setdefault('cov_activity', '.ui.ConversationsActivity')
        super().__init__(
            'eu.siacs.conversations', '.ui.ConversationActivity', **kwargs)
        self.grant_permissions(['READ_CONTACTS'])
        self.clear_cache()

    @staticmethod
    def _rand_sentence(length: int):
        return ''.join((random.choice(string.ascii_lowercase + ' ')
                        for _ in range(length)))

    def warmup(self):
        self.driver.find_element_by_accessibility_id('More options').click()
        time.sleep(1)
        self.find_element_by_name('Restore backup').click()
        time.sleep(1)
        self.find_element_by_res_id('account_jid').click()
        time.sleep(1)
        self.find_element_by_res_id('account_password').send_keys('10qpalzm,.')
        time.sleep(1)
        self.driver.find_element_by_id('android:id/button1').click()
        time.sleep(4)
        self.find_element_by_res_id('conversation_name').click()
        time.sleep(1)
        self.find_element_by_res_id('snackbar_action').click()
        time.sleep(4)
        self.back()

    def actions(self):
        # clicking too early have no effect, even the entry is there
        time.sleep(4)
        self.find_element_by_res_id('conversation_name').click()
        time.sleep(4)
        # time.sleep(40)  # cov
        self.may_start_profiler()
        for _ in range(10):
            text = self._rand_sentence(20)
            self.find_element_by_res_id('textinput').send_keys(text)
            time.sleep(1)
            self.find_element_by_res_id('textSendButton').click()
            time.sleep(1)
        time.sleep(4)
        self.may_stop_profiler()
