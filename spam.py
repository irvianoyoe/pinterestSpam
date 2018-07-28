#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
----------------------------------------------
 ___   _   _          __   ___    __    _
| |_) | | | |\ |     ( (` | |_)  / /\  | |\/|
|_|   |_| |_| \|     _)_) |_|   /_/--\ |_|  |

'Copyright 2017, by _Irv'
----------------------------------------------

Format file user.txt
username:password
Format pada file post.txt
URL link pic
Description
Site
Boardname

PinSpam adalah program Pinterest spamming
Keterangan:
File user berisi username dan password login
File post berisi komponen post seperti
link post(berupa link image jpg png etc), Description, site dan boardname
File sudah berisi user yg sukses melakukan Pin
File log berisi total berapa kali program berjalan

'''
__author__ = '_Irv'
__license__ = 'PRIVATE'
__copyright__ = 'Copyright 2017, _Irv'
__version__ = '1.0.0'

import re
import sys
import os
import time
import os
from lib import Pinterest


def run():
    datafile = open(file_log, 'r')
    return datafile.read()

def prosses(n):
    proses = open(file_log, "wb")
    proses.write(str(n))
    proses.close
    return

def save(item):
    simpan_data = open(file_sudah, "a")
    simpan_data.write(item+'\n')
    simpan_data.close
    return

def check(user):
    datafile = file(file_sudah)
    found = False
    for line in datafile:
        if user in line:
            found = True
            break
    return found

def userlist():
    with open(file_user, 'r') as output_file:
        credentials = [x.strip().split(':') for x in output_file.readlines()]
        return credentials

def postdata():
    with open(file_post, 'r') as output_file:
        results_str = output_file.readlines()
        return [line.rstrip('\n') for line in results_str]

def main(pin):
    running = run()
    if not running:
        rand = 0
    else:
        rand = int(running)

    if rand >= len(userlist()):
        print '[-] Semua User sudah selesai melakukan PIN'
        n = 0
        prosses(n)
        return

    username = userlist()[rand][0]
    password = userlist()[rand][1]

    post = postdata()
    postN = len(post)-1

    if postN == 3:
        media = post[0].strip()
        description = post[1].strip()
        posturl = post[2].strip()
        boardName = post[3].strip()
    else:
        print '[-] Properti post Kurang'
        return


    sudah = check(username)
    if not sudah:
        print '[-] Login: %s' % username
        try:
            logged = pin.login(username,password)
        except:
            print '[-] Login Error!!'
            b = rand+1
            prosses(b)
            return



        if logged:
            try:
                Newboard = pin.buatBoard(boardName)
                print '[-] Nama Board %s Berhasil Di Buat!' % boardName
            except:
                print '[-] Nama Board %s Sudah Ada!' % boardName
                b = rand+1
                prosses(b)
                pass

            try:
                boards = pin.lihatBoards()
                boards_id = boards[boardName]['id']
            except:
                print "Board id tidak ditemukan system error"
                return

            if boards_id:
                print '[-] Board ID: %s' % boards_id
                print '[-] URL PIN: %s' % media
                print '[-] URL POST: %s' % posturl
                print '[-] Description: %s' % description
                try:
                    save_pin = pin.buatPin(boards_id,posturl,media,description)
                    print '[-] PIN Created: %s' % save_pin
                except:
                    print '[-] Pin Created: Error!'
                    return
                if save_pin:
                    save(str(username))
                    b = rand+1
                    prosses(b)
    else:
        print '[-] Username %s sudah pernah melakukan PIN!' % username
        b = rand+1
        prosses(b)
        return




if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_sudah = '{}/sudah'.format(dir_path)
    file_log = '{}/log'.format(dir_path)
    file_user = '{}/user.txt'.format(dir_path)
    file_post = '{}/post.txt'.format(dir_path)
    try:
        open(file_sudah)
    except IOError:
        open(file_sudah, 'w+')
    try:
        open(file_log)
    except IOError:
        open(file_log, 'w+')
    try:
        open(file_user)
    except IOError:
        open(file_user, 'w+')
    try:
        open(file_post)
    except IOError:
        open(file_post, 'w+')

    print'''

    =============================================
     ___   _   _          __   ___    __    _
    | |_) | | | |\ |     ( (` | |_)  / /\  | |\/|
    |_|   |_| |_| \|     _)_) |_|   /_/--\ |_|  |
    Copyright 2017, by _Irv
    =============================================
     Format File {0}
     username:password
     Format File {1}
     URL link pic
     Description
     Site
     Boardname
        '''.format(file_user,file_post)
    pin = Pinterest()
    main(pin)
