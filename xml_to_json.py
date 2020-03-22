import os
import argparse
import penut.io as pio
import xml.etree.cElementTree as ET

from wiki import remove_wikitext

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    fn, ext = os.path.splitext(args.output)
    out_pretty = f'{fn}_pretty{ext}'

    xml_to_json(args.input_dir, args.output, out_pretty)

def xml_to_json(inn_dir, out1, out2):
    pageset = []
    for fp in walk_dir(inn_dir):
        print(fp, end='\r')
        root = ET.parse(fp).getroot()
        for page in root.findall('page'):
            title = page.find('title').text
            pid = page.find('id').text
            text = page.find('revision').find('text').text
            text = remove_wikitext(text)
            page = {'title': title, 'id': pid, 'text': text}
            pageset.append(page)
    pio.dump_json(pageset, f'{out1}', indent=None)
    pio.dump_json(pageset, f'{out2}', indent=2)

def walk_dir(inn):
    for dir_path, _, file_list in os.walk(inn):
        for file_name in file_list:
            full_path = os.path.join(dir_path, file_name)
            yield full_path

if __name__ == "__main__":
    main()
