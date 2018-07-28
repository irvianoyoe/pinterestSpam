#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

-----------------------------------------------------------------------------
 ._  o ._ _|_  _  ._ _   _ _|_        _  _  ._    _ |_   _   _ |  o ._   _
 |_) | | | |_ (/_ | (/_ _>  |_   |_| _> (/_ |    (_ | | (/_ (_ |< | | | (_|
 |                                                                       _|
-----------------------------------------------------------------------------

File ini berfungsi untuk checking user suspend kemudian disimpan di dalam file valid.txt
'''
__author__ = '_Irv'
__license__ = 'PRIVATE'
__copyright__ = 'Copyright 2017, _Irv'
__version__ = '1.0.0'

import os
import re
from lib import Pinterest

def check(filenya,user):
    datafile = file(filenya)
    found = False
    for line in datafile:
        if user in line:
            found = True
            break
    return found

def main():
    print '==============================='
    print '[+] pinterest User checking'
    print '[+] Copyright 2017, by _Irv'
    print '-------------------------------'
    pin = Pinterest()
    URL = 'https://www.pinterest.com/'
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_user = '{}/user.txt'.format(dir_path)
    file_valid = '{}/valid.txt'.format(dir_path)
    try:
        open(file_valid)
    except IOError:
        open(file_valid, 'w+')
    try:
        open(file_user)
    except Exception as e:
        print '[x] error %s' % e
        sys.exit(1)
    with open(file_user, 'r') as output_file:
        credentials = [x.strip().split(':') for x in output_file.readlines()]
    total_user = len(credentials)
    for i in range(0,total_user):
        email = credentials[i][0]
        login = credentials[i][0].split('@')
        username = login[0]
        if not check(file_valid,email):
            url = '{0}{1}'.format(URL,username)
            browser = pin.request(url)
            if re.search(r'pinterest://www\.pinterest\.com/'+username.lower(), str(browser)):
                print '[-] username: %s ' % username
                print '[-] email: %s'  % email
                print '[+] masih aktif!'
                try:
                    simpan_data = open(file_valid, "a")
                    simpan_data.write(email+'\n')
                    simpan_data.close
                    print '[+] berhasil disimpan pada file %s' % file_valid
                except:
                    print '[-] error file tidak bisa di simpan di dalam %s' % file_valid
            else:
                print '[-] email: %s'  % email
                print '[x] user sudah di hapus oleh pinterest!'
        else:
            print '[-] email %s' % email
            print '[-] sudah ada di databases'
            print '[-] silahkan lihat file %s' % file_valid


if __name__ == '__main__':
    main()
