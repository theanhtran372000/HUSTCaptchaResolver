# HUSTCaptchaResolver

**Captcha resolver for HUST (Hanoi University of Science and Technology).**

**Target:** to resolve captcha images on 2 websites
- [Website ctt-sis](https://ctt-sis.hust.edu.vn/)
- [Website dk-sis](https://dk-sis.hust.edu.vn/)

Below is the basic instruction throughout the project.

## 1. Configuration
- [Optional] Create and activate environments
```
# Create virtual environment
python -m venv <env-name>

# Activate environment
source <env-name>/bin/activate  # With Linux
.\<env-name>\Scripts\activate   # With Windows
```

- Install `torch` with `cuda`

```
pip install torch===1.11.0+cu115 torchvision===0.12.0 torchaudio===0.11.0 -f https://download.pytorch.org/whl/torch_stable.html
```

- Install requirements

```
pip install -r requirements.txt
```

## 2. Tools

- **Crawl:** Crawl datasets and raw labels. Dataset will be crawled from 2 websites `ctt-sis` and `dk-sis`. The amount and sources can be configured in `tools/configs/crawl.yml`.

```
bash scripts/crawl.sh
```

- **Relabel:** The labels are quite raw. Use the following pre-built `Streamlit` app to relabel data. App configuration is in `tools/configs/relabel.yml`
```
bash scripts/relabel.sh
```

- **Split:** Split dataset into train and valid set

```
bash scripts/split.sh
```

## 3. Train model
- Create `dataset` folder and put dataset inside. You can use your own dataset or use our pre-built dataset ([Google Drive](https://drive.google.com/file/d/17LNzf5BpRxdAXQEfR-_BEoUHCqejc7Qc/view?usp=sharing))
- Train model. Training configuration is at `configs/configs.yml`.
```
bash scripts/train.sh
```

## 4. Inference
- Pretrained model ([Google Drive](https://drive.google.com/file/d/191wgsZsZKi3Ep3kBKgpyzdwdSY1JPGQY/view?usp=sharing)) performance:
  - Full sequence accuracy: `99.27%`
  - Per character accuracy: `99.88%`
- Create directory `checkpoints` and put the pretrained weights inside
- Run inference
```
bash scripts/infer.sh
```
- Request format
  - Default port: `7000` (can be re-configure)
  - API: `/`
  - Request: `POST (form-data)`
  ```
  "file": <image file> # png, jpg or jpeg
  ```
  - Response format
  ```
  <result> # example: 38275
  ```

## 5. Docker
- Rebuild image and run
```
docker build -t <image-name> .
docker run -p <local-port>:<docker-port>/tcp <image-name>
```
- Or use my pre-built image
```
docker run -p <local-port>:7000/tcp theanhtran/hust-captcha-resolver
```