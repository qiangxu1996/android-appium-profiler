import sys
from os import path

import pexpect

if __name__ == '__main__':
    wd = path.abspath(path.dirname(__file__))
    kpcli = path.join(wd, 'kpcli-3.4.pl')
    args = ['--kdb', path.join(wd, 'keepass.kdbx'),
            '--pwfile', path.join(wd, 'pwfile.txt'),
            '--command']
    for i in range(120):
        args.append(f'new keepass/entry{i}')
        child = pexpect.spawn(kpcli, args)
        child.logfile = sys.stdout.buffer
        args.pop()
        child.expect('Username: ')
        child.sendline('dsnl')
        child.expect('Password: ')
        child.sendline('g')
        child.expect('URL: ')
        child.sendline(f'example{i}.com')
        child.expect('Tags: ')
        child.sendline()
        child.expect('Strings:.*')
        child.sendline()
        child.expect('| ')
        child.sendline()
        child.expect('Database was modified.*')
        child.send('y')
        child.wait()
