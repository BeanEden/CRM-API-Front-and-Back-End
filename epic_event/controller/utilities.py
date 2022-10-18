"""Utilities logging and miscellanous"""
import os
import datetime


def logging(request, login = True):
    """writing logging"""
    status = ""
    if login == True:
        status = "connecting"
    else:
        status = "logging_out"
    user = request.user
    log_entry = {'user': user, 'datetime': datetime, 'status': status}
    with open('readme.txt', 'w') as f:
        f.write(str(log_entry))


def error_log(request, text):
    """error logging function"""
    log_entry = {'user': request.user,
                 'datetime': str(datetime.datetime.now()),
                 'error': text,
                 'url': request.url}
    with open('error_log.txt', 'a') as f:
        f.write(str(log_entry))
    return log_entry
