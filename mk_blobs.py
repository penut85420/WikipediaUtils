import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import os
import re
import argparse
import penut.io as pio

from penut.utils import TimeCost
from ckiptagger import WS, data_utils

def main(inn, out, do_seg, model_path, batch_sent):
    title_patterns = get_title_patterns()

    if do_seg:
        with TimeCost('WS Model Loading'):
            ws = load_ws(model_path)

    with TimeCost('Data Loading'):
        data = pio.load(inn)
        total = len(data)

    sents = []
    with open(out, 'w', encoding='UTF-8') as fout:
        for i, page in enumerate(data):
            print_progress(i, total)

            if not re.search(title_patterns, page['title'], re.I) and page['text'] != None:
                para = mk_para(page)

                if do_seg:
                    sents.append(para)
                    if len(sents) >= batch_sent:
                        batch_seg(ws, fout, sents)
                        sents = []
                else:
                    fout.write(para)

        batch_seg(ws, fout, sents)

def get_title_patterns():
    title_patterns = [
        'mediawiki:', 'wikipedia:', 'category:',
        'template:', '(消歧義)', 'portal:', 'draft:',
        'topic:', 'help:', 'file:', '模塊:', '列表', '年表'
    ]
    title_patterns = ')|('.join(map(re.escape, title_patterns))
    title_patterns = f'({title_patterns})'

    return title_patterns

def load_ws(model_path):
    if not os.path.exists(model_path):
        os.makedirs(model_path)
        data_utils.downlaod_data_gdown(model_path)
    model_path = os.path.join(model_path, 'data')

    return WS(model_path, disable_cuda=False)

def print_progress(i, total):
    progress = i / total * 100
    print(end=f'{progress:6.2f}% {i}/{total}\r')

def mk_para(page):
    return f"{page['title']}，{page['text']}\n\n"

def batch_seg(ws, fout, sents):
    with TimeCost(f'{sum(map(len, sents))} Segmentation'):
        para = seg(ws, sents)
        fout.write(para)

def seg(ws, sents):
    segs = ws(sents)
    rtn = ''.join([' '.join(sent) for sent in segs])

    return rtn

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-m', '--model-path', default='./ckip_models')
    parser.add_argument('-s', '--do-seg', action='store_true')
    parser.add_argument('-b', '--batch-size', default=16)
    args = parser.parse_args()

    with TimeCost('Making Blobs'):
        main(args.input, args.output, args.do_seg, args.model_path, args.batch_size)
