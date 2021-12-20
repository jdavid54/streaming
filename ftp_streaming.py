#!/usr/bin/python
# -*- coding: utf-8 -*-

from ftp_cmd  import *
import os  #https://docs.python.org/3/library/os.html
#help()
      
#local working directory
os.chdir('html')

# credentials ftp 
host = ''
user = ''
pwd  = ''
#host, user, pwd = 'pagesperso-xxxx.fr','user','pwd'
upload(host, user, pwd)

