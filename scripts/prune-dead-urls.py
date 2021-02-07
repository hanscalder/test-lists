import argparse
import datetime
import os
import re
import sys
import csv
from glob import glob
from urllib.parse import urlparse
import socket

def main(lists_path):
    for csv_path in glob(os.path.join(lists_path, "*")):
        if os.path.basename(csv_path).startswith('00-') or os.path.basename(csv_path).startswith('official'):
            continue
        with open(csv_path, 'r') as in_file, \
             open(csv_path + '.tmp', 'w') as out_file:
            reader = csv.reader(in_file, delimiter=',')
            writer = csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow(next(reader))
            for idx, row in enumerate(reader):
                url = row[0]
                print(f"Processing URL {url}")
                domain = urlparse(url).netloc.split(':')[0]
                try:
                    socket.getaddrinfo(domain, 80)
                    writer.writerow(row)
                except socket.gaierror:
                    print(f"Invalid URL {url}")
        os.rename(csv_path + '.tmp', csv_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check if URLs in the test list are OK')
    parser.add_argument('lists_path', metavar='LISTS_PATH', help='path to the test list')
    args = parser.parse_args()
    main(args.lists_path)
