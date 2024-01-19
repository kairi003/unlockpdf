#!/usr/bin/env python3

import sys
import argparse
from getpass import getpass
from pathlib import Path
from typing import Optional
from pypdf import PdfReader, PdfWriter
from pypdf.errors import FileNotDecryptedError


def unlock(input_file: Path, output_file: Path, password: Optional[str] =None):
    with input_file.open('rb') as input_file, output_file.open('wb') as output_file:
        reader = PdfReader(input_file)
        if reader.is_encrypted:
            if not password:
                password = getpass()
            reader.decrypt(password)
        else:
            print(f'Warning: {input_file} is not encrypted', file=sys.stderr)
            return
        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
        writer.write(output_file)


def main():
    parser = argparse.ArgumentParser(description='Unlock PDF files')
    parser.add_argument('input', metavar='INPUT', type=Path, nargs='+',
                        help='input file')
    parser.add_argument('-o', '--output', metavar='OUTPUT', type=Path,
                        default=None,
                        help='output file')
    parser.add_argument('-p', '--password', metavar='PASSWORD', type=str,
                        default=None,
                        help='password')
    args = parser.parse_args()
    if args.output:
        if len(args.input) > 1:
            parser.error(
                'argument -o/--output: not allowed with multiple inputs')
        try:
            unlock(args.input[0], args.output, args.password)
        except FileNotDecryptedError:
            print(f'Error: {args.input[0]} is not encrypted', file=sys.stderr)
    else:
        if len(args.input) > 1:
            parser.error('argument -o/--output: required with multiple inputs')
        for input_file in args.input:
            output_file = input_file.with_suffix('.unlocked.pdf')
            try:
                unlock(input_file, output_file, args.password)
            except FileNotDecryptedError:
                print(f'Error: {input_file} is not encrypted', file=sys.stderr)


if __name__ == '__main__':
    main()
