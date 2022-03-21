# dhv_crawler

simplify periodically checking for an item on the dhv marketplace 

## usage

create a config file named conf.py with the following content

    host = 'localhost'
    port =  587
    tls =  True
    username = ''
    password = ''
    sender = 'ABC <mymail>'
    to = 'XYZ <mymail>'

simply call

./dhv_crawler.py 'item i am looking for'

Result will be either: 'item ...' not found or an email will be sent using the given mail settings containing deteil about the discovered items.

## automation

Simply use crontab for automation
