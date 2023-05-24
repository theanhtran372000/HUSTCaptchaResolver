# HUSTCaptchaResolver

Captcha resolver for Hanoi University of Science and Technology

## 1. Configuration

- Install torch with cuda

```
pip install torch===1.11.0+cu115 torchvision===0.12.0 torchaudio===0.11.0 -f https://download.pytorch.org/whl/torch_stable.html
```

- Install requirements

```
pip install -r requirements.txt
```

## 2. Tools

- Crawl datasets

```
bash scripts/crawl.py
```

- Split dataset into train and valid set

```
bash scripts/split.py
```
