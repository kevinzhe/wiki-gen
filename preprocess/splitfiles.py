#!/usr/bin/env python3

import os
import sys


def log(msg):
    print(msg, file=sys.stderr)

def dump(lines, out_path, dump_count):
    path_to_write = '{base}{sep}wiki-parsed-{count}'.format(
                            base = out_path,
                            sep = os.sep,
                            count = dump_count)
    with open(path_to_write, 'w') as f:
        for line in lines:
            f.write(line + '\n')
    log('{count} lines written to {path}'.format(count = len(lines), path = path_to_write))

def main(xml_path, output_dir_path):
    with open(xml_path) as corpus:
        cache = []
        line_count = 0
        dump_count = 0
        lines_per_file = 600000
        for read_line in corpus:
            line_count += 1
            cache.append(read_line)
            if line_count > articles_per_file:
                dump(cache, output_dir_path, dump_count)
                dump_count += 1
                line_count = 0
                cache = []
        log('Done!')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        log('Usage: {} [path_to_xml] [output dir]'.format(sys.argv[0])
    if not os.path.isfile(sys.argv[1]):
        log('{} is not a file'.format(sys.argv[1]))
    if not os.path.isdir(sys.argv[2]):
        log('{} is not a directory'.format(sys.argv[2]))
    main(sys.argv[1], sys.argv[2])
