import subprocess
import socket
import sys
from urllib.request import Request, urlopen
import re
import time
import json
from prettytable import PrettyTable


def get_ips_in_traceroute(hostname):
    tracert_ips = []
    traceroute = subprocess.Popen(["tracert", '-w', '100', hostname], stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
    for line in iter(traceroute.stdout.readline, ""):
        if line:
            ip = re.search('(\d+\.){3}\d+', line.decode('utf8', errors='ignore').strip())
            if not ip:
                continue
            tracert_ips.append(ip.group())
            print(ip.group())
        else:
            break
    return tracert_ips

def get_as_info_by_ip(ip):
    asm_base = 'https://api.iptoasn.com/v1/as/ip/'
    req = Request(asm_base + ip,
        headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    return json.loads(page.read())


if __name__ == '__main__':
    try:
        hostname = sys.argv[1]
    except IndexError:
        raise ValueError(f"PLEASE ENTER HOST NAME:\n>> {sys.argv[0].split('/')[-1]} 'www.yourhost.com'")
    ips = get_ips_in_traceroute(hostname)
    table = PrettyTable()
    table.field_names = ['№', 'IP', 'AS NUMBER', 'COUNTRY']
    for i in range(1, len(ips) + 1):
        sys.stdout.write(f'processing ip No {i}\n')
        sys.stdout.flush()
        current_ip = ips[i - 1]
        time.sleep(1)
        reply = get_as_info_by_ip(current_ip)
        try:
            table.add_row([i, current_ip, reply['as_number'], reply['as_country_code']])
        except KeyError:
            table.add_row([i, current_ip, '*', '*'])
    print(table)