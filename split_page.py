import os
import argparse
from penut.utils import TimeCost

fid = 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    split(args.inn, args.out)

def split(inn, out):
    record = False
    max_size = 4 * 1024 * 1024
    os.makedirs(out, exist_ok=True)

    fout = newfile()

    print(f' {fid:04d}', end='\r')
    with open(inn, 'r', encoding='UTF-8') as f:
        for line in f:
            if line.strip().startswith('<page>'):
                record = True
            elif line.strip().startswith('</page>'):
                fout.write(line)
                record = False
                if fout.tell() >= max_size:
                    endfile(fout)
                    print(f' {fid:04d}', end='\r')
                    fout = newfile()
            if record:
                fout.write(line)
    endfile(fout)

def newfile():
    global fid
    fid += 1
    fpath = os.path.join(out, f'page{fid:04d}.xml')
    fout = open(fpath, 'w', encoding='UTF-8')
    fout.write('<pageset>\n')
    return fout

def endfile(fout):
    fout.write('</pageset>')
    fout.close()

if __name__ == "__main__":
    with TimeCost('Split Wiki Dump into Pages'):
        main()
