#!/usr/bin/env python3
import os
import shutil
import time
import sys
import datetime as dt

def estimate_size(s):
    if s.endswith('G'):
        return float(s[:-1]) * 1024 * 1024 * 1024
    if s.endswith('GB'):
        return float(s[:-2]) * 1024 * 1024 * 1024
    if s.endswith('M'):
        return float(s[:-1]) * 1024 * 1024
    if s.endswith('MB'):
        return float(s[:-2]) * 1024 * 1024
    if s.endswith('K'):
        return float(s[:-1]) * 1024
    if s.endswith('KB'):
        return float(s[:-2]) * 1024
    return s

def format_size(s):
    if s.endswith('G'):
        return float(s[:-1]) / 1024 / 1024 / 1024
    if s.endswith('GB'):
        return float(s[:-2]) / 1024 / 1024 / 1024
    if s.endswith('M'):
        return float(s[:-1]) / 1024 / 1024
    if s.endswith('MB'):
        return float(s[:-2]) / 1024 / 1024
    if s.endswith('K'):
        return float(s[:-1]) / 1024
    if s.endswith('KB'):
        return float(s[:-2]) / 1024
    return s

def time_left(es, b, a):
    sec = (es - b) / a
    td = dt.timedelta(seconds=sec)
    left = ''
    if td.days > 0:
        left += '{}days '.format(td.days)
    if td.seconds // 3600 > 0:
        left += '{}h '.format(td.seconds // 3600)
    if (td.seconds // 60) % 60 > 0:
        left += '{}min '.format((td.seconds // 60) % 60)
    left += '{}s'.format(td.seconds % 60)

    return left + ' to finish'

def main(args):
    if len(args) == 0:
        print('provide a file name please')
        sys.exit(1)
    if len(args) < 2:
        print('provide an estimate of size please')
        sys.exit(1)

    # track this file
    fn = args[0]
    # estimated size given
    es = estimate_size(args[1])
    # seconds to wait between reading
    st = float(args[2]) if len(args) > 2 else 1
    # how many reads for averaging speed
    buffer_size = 10
    # last read file size in bytes
    last = os.path.getsize(fn)

    # buffer
    changes = [0] * buffer_size
    buff_count = 0
    init_count = 0

    if not os.path.exists(fn):
        print('{} does not exist'.format(fn))
        sys.exit(2)
    try:
        while True:
            # rolling buffer
            buff_count = (buff_count + 1) % buffer_size
            b = os.path.getsize(fn)
            # how far are we in percentage
            proc = b / es
            # diff in bytest between reads
            changes[buff_count] = b - last
            last = b
            # change per second
            average = sum(changes) / buffer_size / st
            init_count += 1
            try:
                # estimate time left
                left = time_left(es, b, average) if init_count > buffer_size else "estimating... " + str(buffer_size - init_count)
            except ZeroDivisionError:
                print("\n --- finished --- ")
                sys.exit(0)

            # status message
            print('\r{:.2f}GB ({:.2%}) {:.2f}MB/s -> {}'.format(format_size(str(b) + 'GB'), proc, format_size(str(average) + 'MB'), left), end='')
            time.sleep(st)

    except KeyboardInterrupt:
        print("\nAborted by user")

main(sys.argv[1:])
