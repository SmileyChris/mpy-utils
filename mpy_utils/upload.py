#!/usr/bin/env python
import serial
import time
import argparse

parser = argparse.ArgumentParser(
    description="Upload files to a device using only the REPL"
)
parser.add_argument(
    '--port', default='/dev/ttyUSB0', help='serial port device')
parser.add_argument(
    '--baud', default=115200, type=int, help='port speed in baud')
parser.add_argument(
    '--delay', default=100.0, type=float, help='delay between lines (ms)')
parser.add_argument(
    '--interrupt', action='store_true',
    help='send soft interrupt (control-C) before upload')
parser.add_argument(
    '--reset', action='store_true',
    help='send soft reset (control-D) after upload')
parser.add_argument(
    'files', nargs='*', type=argparse.FileType('rb'))


def main():
    args = parser.parse_args()
    if not args.files:
        parser.print_help()
        return
    port = serial.Serial(args.port, args.baud)

    if args.interrupt:
        port.write('\x03')

    for fh in args.files:
        port.write('_fh = open(%r, "w")\r' % fh.name)

        while True:
            s = fh.read(50)
            if not s:
                break
            port.write("_fh.write(%r)\r" % s)
            time.sleep(args.delay/1000.0)

        port.write('_fh.close()\r')
        fh.close()

    if args.reset:
        port.write('\x04')

    port.close()


if __name__ == '__main__':
    main()
