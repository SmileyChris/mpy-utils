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
    '--delay', default=80.0, type=float, help='delay between lines (ms)')
parser.add_argument(
    '--no-interrupt', action='store_false', default=True,
    help="don't send soft interrupt (control-C) before upload")
parser.add_argument(
    '--reset', action='store_true',
    help='send soft reset (control-D) after upload')
parser.add_argument(
    '--main', type=argparse.FileType('rb'),
    help='save file as main.py and reset')
parser.add_argument(
    'files', nargs='*', type=argparse.FileType('rb'))


class Comms(object):

    def __init__(self, args, interrupt=None):
        self.args = args
        if interrupt is None:
            self.interrupt = not args.no_interrupt
        else:
            self.interrupt = interrupt

    @property
    def port(self):
        if not hasattr(self, '_port'):
            self._port = serial.Serial(self.args.port, self.args.baud)
            if self.interrupt:
                self._port.write('\x03')
        return self._port

    def write(self, line, ending='\r'):
        self.port.write(line)
        if ending:
            self.port.write(ending)

    def close(self):
        if hasattr(self, '_port'):
            self._port.close()
            del self._port


def main():
    args = parser.parse_args()
    comms = Comms(args, interrupt=args.main or not args.no_interrupt)

    files = [(fh.name, fh) for fh in args.files]
    if args.main:
        files.append(('main.py', args.main))
    if not files:
        parser.print_help()
        return

    for name, fh in files:
        comms.write('_fh = open(%r, "w")' % name)
        comms.write('_fhw = lambda text: _fh.write(text) and None')

        while True:
            s = fh.read(60)
            if not s:
                break
            comms.write("_fhw(%r)" % s)
            time.sleep(args.delay/1000.0)

        comms.write('_fh.close()')
        fh.close()

    if args.reset or args.main:
        comms.write('\x04', ending=None)
    else:
        comms.write('del _fh')

    comms.close()


if __name__ == '__main__':
    main()
