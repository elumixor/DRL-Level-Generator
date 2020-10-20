import argparse

parser = argparse.ArgumentParser(description="Tests Arguments values")
parser.add_argument('--test_key')
args = vars(parser.parse_args())
print(args['test_key'])
