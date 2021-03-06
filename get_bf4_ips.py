#!/usr/bin/env python
"""Writes a pfSense compatible alias IP List for known bf4 IP addresses

Usage:
python get_bf4_ips.py

Copyright (C) 2017 Patrick Montalbano

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
 any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from urllib.request import build_opener, HTTPCookieProcessor
from http.cookiejar import CookieJar
import http.client
from bs4 import BeautifulSoup
import ipaddress


def is_valid_ipv4(address):
    """Check if address is valid"""
    try:
        ipaddress.ip_network(address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            ipaddress.ip_network(address)
        except:
            return False
        return address.count('.') == 3
    except:  # not a valid address
        return False

    return True


def get_ipinfo():
    ip_list = []
    for page_idx in range(1, 20):
        url = "https://www.gametracker.com/search/bf4/?searchipp=50&searchpge={0}#search".format(page_idx)
        print(str("Reading from "+url))
        soup = None
        while True:
            try:
                cj = CookieJar()
                opener = build_opener(HTTPCookieProcessor(cj))
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                page = opener.open(url)
                soup = BeautifulSoup(page)
            except (IOError, http.client.HTTPException) as e:
                    print(e)
            break

        # Parse Valid networks to list
        for tr in soup.find_all('tr'):
            for span in tr.find_all('span')[0:1]:
                if is_valid_ipv4(span.text):
                    ip_list.append(span.text)
    return ip_list


if __name__ == "__main__":
    filename = 'bf4_ips.txt'
    file = open(filename, 'w')
    addresses = get_ipinfo()
    for n in addresses:
        file.write("%s\n" % n)
    file.close()
    count = str(len(addresses))
    print(str('Wrote ' + count + " ip addresses to " + filename))
