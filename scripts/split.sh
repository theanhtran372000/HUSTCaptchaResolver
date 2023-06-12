#!/bin/bash
python tools/split.py \
  --input_path=dataset/hustcaptcha/new_labels.txt \
  --train_path=dataset/hustcaptcha/train_labels.txt \
  --valid_path=dataset/hustcaptcha/valid_labels.txt \
  --valid_ratio=0.1