#!/usr/bin/env python3

import os
import datetime
import argparse
import smtplib
import requests
import re
from bs4 import BeautifulSoup

import conf as conf

url = "https://www.dhv.de/db3/gebrauchtmarkt/anzeigen?suchbegriff=omega&rubrik=0&preismin=&preismax=&anbietertyp=0&land=0&plz=&itemsperpage=100"
params = {
    'suchbegriff': '',
    'rubrik': 0,
    'preismin': '',
    'preismax': '',
    'anbietertyp': 0,
    'land': 0,
    'plz': '',
    'itemsperpage': 100
}


"""
config file; place it as conf.py
"""
#    host = 'localhost'
#    port =  587
#    tls =  True
#    username = ''
#    password = ''
#    sender = 'ABC <mymail>'
#    to = 'XYZ <mymail>'

def send_email( subject, content ):
    """ Send a simple, stupid, text, UTF-8 mail in Python """

    for ill in [ "\n", "\r" ]:
        subject = subject.replace(ill, ' ')

    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Disposition': 'inline',
        'Content-Transfer-Encoding': '8bit',
        'From': conf.sender,
        'To': conf.to,
        'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
        'X-Mailer': 'python',
        'Subject': subject
    }

    # create the message
    msg = ''
    for key, value in headers.items():
        msg += "%s: %s\n" % (key, value)

    # add contents
    msg += "\n%s\n"  % (content)

    s = smtplib.SMTP(conf.host, conf.port)

    if conf.tls:
        s.ehlo()
        s.starttls()
        s.ehlo()

    if conf.username and conf.password:
        s.login(conf.username, conf.password)

    print ("sending %s to %s" % (subject, headers['To']))
    s.sendmail(headers['From'], headers['To'], msg.encode("utf8"))
    s.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple DHV Market Crawler')

    '''arguments'''
    parser.add_argument('item', type=str, help='item to look for')
    args = parser.parse_args()

    params['suchbegriff'] = args.item

    i = 0
    r = requests.models.Response()
    while r.status_code not in (200, 422) and i < 10:
        r = requests.get(url, params=params)
        i+=1

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        all_offers = soup.find_all('div', class_='gm_offer')
        
        if len(all_offers) > 0:
            message_post = ""
            idx = 0
            for item in all_offers:
                title = item.find('a', class_='dtl').get_text()
                if 'suche' in title.lower() or 'looking' in title.lower(): continue
                idx += 1
                item_text = f"{idx} {title}\n"
                item_text += f"{item.find(class_='gm_price').get_text()} {item.find(class_='gm_price_type').get_text()}\n"  
                item_text += f"https://www.dhv.de{item.find('a', class_='gm_offer_btn dtl')['href']}\n"  
                item_desc = item.find(class_='gm_offer_description').get_text()
                item_desc = re.sub(r'^$\n', '', item_desc, flags=re.MULTILINE).replace('\n','') 
                item_text += " ".join(item_desc.split())
                item_text += "\n\n"

                message_post += item_text

            if idx > 0:
                subject = f"CRAWLER {args.item} found {idx} times \n\n"
                send_email(subject, message_post)
        else:
            print(f"{args.item} not found.")
    else:
        print(f"request ended with status code {r.status_code}")

