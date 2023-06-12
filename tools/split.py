import argparse
import random
import math
from loguru import logger

def get_parser():
  parser = argparse.ArgumentParser()
  
  parser.add_argument('--seed', type=int, default=2023, help='Random seed')
  parser.add_argument('--input_path', type=str, required=True, help='Path to input label file')
  parser.add_argument('--train_path', type=str, required=True, help='Path to output train label file')
  parser.add_argument('--valid_path', type=str, required=True, help='Path to output valid label file')
  parser.add_argument('--valid_ratio', type=float, default=0.2, help='Proportion of valid set')
  
  return parser

if __name__ == '__main__':
  # Parse CLI args
  parser = get_parser()
  args = parser.parse_args()
  
  
  with open(args.input_path, 'r') as f:
    lines = [line.strip() for line in f.readlines()]
  logger.info('Read {} samples from {}'.format(len(lines), args.input_path))  
  
  # Shuffle samples
  random.seed(args.seed)
  random.shuffle(lines)
  
  # Split
  n_samples = len(lines)
  n_valid = math.ceil(args.valid_ratio * n_samples)
  
  logger.info('Write {} valid samples to {}'.format(n_valid, args.valid_path))  
  with open(args.valid_path, 'w') as f:
    f.write('\n'.join(lines[:n_valid]) + '\n')
  
  logger.info('Write {} train samples to {}'.format(n_samples - n_valid, args.train_path))  
  with open(args.train_path, 'w') as f:
    f.write('\n'.join(lines[n_valid:]) + '\n')
  
  logger.success('All done!')