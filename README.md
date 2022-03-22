# dhv_crawler

check for an item in the [DHV Marketplace](https://www.dhv.de/db3/gebrauchtmarkt/anzeigen/) and get an email with the found items.

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

result will be either: 'item ...' not found or an email will be sent using the given mail settings containing deteil about the discovered items.

## automation

simply use crontab for automation
