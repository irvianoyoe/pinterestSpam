#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

 ____  __ __  __ ______  ____ ____   ____  __  ______
 || \\ || ||\ || | || | ||    || \\ ||    (( \ | || |
 ||_// || ||\\||   ||   ||==  ||_// ||==   \\    ||
 ||    || || \||   ||   ||___ || \\ ||___ \_))   ||

Copyright 2017, by _Irv


Pinterest Registration Tool
- pastikan selenium terinstall dengan benar
- pastikan driver selenium sesuai versi OS

pip install selenium
'''
import sys
import os
import re
import time
from random import randint
from platform import system
try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import NoSuchElementException
except:
    print '[-] Selenium driver belum di install'
    print '[-] Instalation:'
    print '[-] pip install selenium'
    sys.exit()

IS_WINDOWS = True if system() == 'Windows' else False
IS_LINUX = True if system() == "Linux" or system() == "Linux2" else False
IS_MAC = True if system() == "Darwin"  else False
if IS_LINUX:
    try:
        from pyvirtualdisplay import Display
    except:
        print '[-] pyvirtualdisplay belum di install'
        print '[-] Instalation:'
        print '[-] pip install pyvirtualdisplay'
        sys.exit(1)

class Browser(object):
    def SELENIUM(self):
        list_agent = [
                     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                     'Mozilla/5.0 (Windows NT X.Y; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2657.0 Safari/537.36,gzip(gfe),gzip(gfe)',
                     'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
                     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
                     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
                     'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
                     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0'
                     ]
        num_agent = len(list_agent)-1
        rand_agent = randint(0, num_agent)
        useragent_random = list_agent[rand_agent]
        user_agent = useragent_random
        # sesuikan dengan chromedriver path dan type os anda
        chromedriver_path = 'chromedriver.exe' if IS_WINDOWS else 'chromedriver'
        dir_path = os.path.dirname(os.path.abspath(__file__))
        chromedriver = dir_path+"/"+chromedriver_path
        os.environ["webdriver.chrome.driver"] = chromedriver
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--user-agent='+user_agent)
        prefs = {"profile.default_content_setting_values.geolocation" :2}
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chromeOptions.add_experimental_option("prefs",prefs)
        try:
            driver = webdriver.Chrome(chromedriver, chrome_options=chromeOptions)
        except:
            print '[-] Selenium tidak sesuai versi OS!'
            print '[-] Baca https://sites.google.com/a/chromium.org/chromedriver/home'
            driver = False
        return driver

def main():
    email = raw_input('Enter email: ')
    if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
        print 'Format Email tidak benar!'
        sys.exit(0)
    password = raw_input('Enter Password: ')
    if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,}$",password):
        print 'Password minimal harus 6 digit angka huruf dan karakter!'
        sys.exit(0)
    username = raw_input('Username: ')
    age = raw_input('Age: ')
    if not re.match(r"(\d+)",age):
        print 'Format umur harus angka!'
        sys.exit(0)

    sex = raw_input("[?] Silahkan masukan pilihan,  "
                  "(1) Male, (2) Female : ")
    if sex == "1":
        sex = '1'
    elif sex == "2":
         sex = '2'
    else:
        sex = False
        print '[!] Pilihan (1) atau (2) saja'
        sys.exit(1)
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_user = '{}/user.txt'.format(dir_path)
    try:
        open(file_user)
    except IOError:
        open(file_user, 'w+')
    try:
        if IS_LINUX:
            display = Display(visible=0, size=(800, 800))
            display.start()
        driver = Browser().SELENIUM()
        try:
            driver.get('https://www.pinterest.com/')
            driver.find_element_by_xpath("//fieldset[1]/input").send_keys(email)
            driver.find_element_by_xpath("//fieldset[2]/input").send_keys(password)
            driver.find_element_by_xpath("//button[@class='red SignupButton active']").click()
            driver.implicitly_wait(3)
            driver.find_element_by_xpath("//div/fieldset[1]/input").send_keys(username)
            driver.find_element_by_xpath("//div/fieldset[2]/input").send_keys(age)
            driver.find_element_by_xpath("//label[@class='Gender__tooltip']["+sex+"]/input").click()
            driver.find_element_by_xpath("//button[@class='red comeOnInButton active']").click()
            driver.implicitly_wait(5)
            driver.find_element_by_xpath("//h2[@class='_2WeKX']")
            print '[-] Registration completed!'
            Registration = True
        except:
            print '[-] Registration Failed!'
            Registration = False
    except:
        '[-] Selenium error!'
        driver = False
        display = False
    finally:
        if driver:
            driver.close()
        if IS_LINUX:
            if display:
                display.stop()
        if Registration:
            simpan_data = open(file_user, "a")
            simpan_data.write(email+':'+password+'\n')
            simpan_data.close
            print '[-] Simpan ID di %s' % file_user




if __name__ == '__main__':
    print'''
    -----------------------------------
    [+] Pinterest Registration Tool [+]
    [+]   Copyright 2017, by _Irv   [+]
    -----------------------------------
    - pastikan selenium freamwork python terinstall dengan benar
    - pastikan driver selenium sesuai versi OS
    '''
    main()
