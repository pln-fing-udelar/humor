import fileinput


def read_tweets_from_input():
    return [eval(line) for line in fileinput.input()]
