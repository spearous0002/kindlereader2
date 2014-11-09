#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main.py
Created by Jiedan<lxb429@gmail.com> on 2010-11-08.
"""

__author__ = "Jiedan<lxb429@gmail.com>"
__version__ = "0.3.3"

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import socket
import logging
import ConfigParser

import gflags
from gflags import FLAGS

work_dir = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(work_dir, 'lib'))
from Tools import Tools
from Reader import Reader, Kindle
from RelatedServices import PocketService, AESService, FeedReadMarker


if __name__ == '__main__':
    gflags.DEFINE_boolean('debug', False,
                          'produces debugging output', short_name='d')
    gflags.DEFINE_string('send_mail', '',
                         '[mobi_path] just send a mobi already generated',
                         short_name='m')
    try:
        FLAGS(sys.argv)  # parse flags
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, sys.argv[0], FLAGS)
        sys.exit(1)

    if FLAGS.debug:
        log_lvl = logging.DEBUG
    else:
        log_lvl = logging.INFO
    logging.basicConfig(level=log_lvl,
                        format='%(asctime)s:%(msecs)03d %(filename)s  %(lineno)03d %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')
    socket.setdefaulttimeout(20)

    conf_file = os.path.join(work_dir, "config.ini")
    if not os.path.isfile(conf_file):
        logging.error("config file '%s' not found" % conf_file)
        sys.exit(1)

    config = ConfigParser.SafeConfigParser()

    config.read(conf_file)
    mail_enable = config.getboolean('general', 'mail_enable')
    magzine_format = config.get('general', 'kindle_format')

    service_host = config.get('third_party', 'service_host')
    aes_secret = config.get('third_party', 'aes_service_secret')

    pocket_service = None
    read_marker = None
    if service_host:
        read_marker = FeedReadMarker(service_host)
        if aes_secret:
            aes_service = AESService(aes_secret)
            pocket_service = PocketService(service_host, aes_service)

    data_dir = os.path.join(work_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if 0 != Kindle.check_kindle_gen():
        logging.error("do not find kindle book generator, exit...")

    st = time.time()
    logging.info("welcome, start ...")
    try:
        if FLAGS.send_mail:
            Tools.mail_magzine(FLAGS.send_mail, config)
            sys.exit(0)

        reader = Reader(work_dir=work_dir, config=config)
        updated_feeds = reader.check_feeds_update()
        mobi_file = Kindle.make_mobi(reader.user_info,
                                     updated_feeds,
                                     data_dir,
                                     magzine_format,
                                     pocket_service=pocket_service,
                                     read_marker=read_marker)
        if mobi_file and mail_enable:
            Tools.mail_magzine(mobi_file, config)

    except Exception:
        import traceback
        logging.error(traceback.format_exc())
        sys.exit(-1)

    logging.info("used time %.2fs" % (time.time()-st))
    logging.info("done.")
