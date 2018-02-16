#!/usr/bin/env python
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default='es', help="language of the tweets to extract (default: es)")
    args = parser.parse_args()

    pass
