import socket
import time

from .. import app_test


class App(app_test.AppTest):
    """
    Start the Vagrant virtual machine on the same machine
    you run the script, before running the test
    """

    def __init__(self, **kwargs):
        super().__init__(
            'org.connectbot.debug', 'org.connectbot.HostListActivity', **kwargs)
        self.clear_cache()
        ip = socket.getaddrinfo(socket.getfqdn(), None)[0][4][0]
        self.nickname = f'vagrant@{ip}:2030'

    def warmup(self):
        self.find_element_by_res_id('add_host_button').click()
        time.sleep(1)
        self.find_element_by_res_id('quickconnect_field')\
            .send_keys(self.nickname)
        time.sleep(1)
        self.find_element_by_res_id('save').click()
        time.sleep(1)
        self.find_element_by_name(self.nickname).click()
        time.sleep(3)
        self.find_element_by_res_id('console_prompt_yes').click()
        time.sleep(3)
        self.back()
        time.sleep(1)

    def actions(self):
        self.find_element_by_name(self.nickname).click()
        time.sleep(3)
        self.find_element_by_res_id('console_password').send_keys('vagrant')
        self.press_keycode('\n')
        time.sleep(2)
        self.press_keycode('cd /vagrant/Python/arithmetic_analysis\n')
        time.sleep(1)
        self.may_start_profiler()
        files = ['bisection.py', 'gaussian_elimination.py',
                 'in_static_equilibrium.py', 'intersection.py',
                 'lu_decomposition.py', 'newton_forward_interpolation.py']
        for f in files:
            self.press_keycode(f'vi {f}\n')
            time.sleep(3)
            self.press_keycode(':q\n')
            time.sleep(2)
        self.may_stop_profiler()
