import argparse
import penut.io as pio
from penut.utils import TimeCost
from ZhConverter.zhhanz_conv import ZhhanzMan

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    translate(args.input, args.output)

def translate(inn, out):
    zm = ZhhanzMan()
    with TimeCost('Loading'):
        data = pio.load(inn)
    total = len(data)

    for i, page in enumerate(data):
        print(end=f'{i}/{total}\r')
        for key in page:
            if page[key] != None:
                page[key] = zm.s2t(page[key])

    pio.dump(out)

if __name__ == "__main__":
    with TimeCost('Translate into Traditional Chinese'):
        main()
