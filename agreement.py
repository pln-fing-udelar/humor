#!/usr/bin/env python
import collections
import csv

import krippendorff_alpha


def main():
    annotators_humor = collections.defaultdict(dict)
    annotators_funniness = collections.defaultdict(dict)

    with open('annotations.csv') as file_:
        for tweet_id, annotator_id, tag in csv.reader(file_):
            if tag in ['1', '2', '3', '4', '5', 'x']:
                annotators_humor[annotator_id][tweet_id] = tag != 'x'
                if tag != 'x':
                    annotators_funniness[annotator_id][tweet_id] = float(tag)

    humor_alpha = krippendorff_alpha.krippendorff_alpha(annotators_humor.values(),
                                                        metric=krippendorff_alpha.nominal_metric,
                                                        convert_items=bool)
    funniness_alpha = krippendorff_alpha.krippendorff_alpha(annotators_funniness.values())

    print(f"alpha for humor: ${humor_alpha}")
    print(f"alpha for funniness: ${funniness_alpha}")


if __name__ == '__main__':
    main()
