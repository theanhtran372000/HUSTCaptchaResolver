FROM python:3.8-slim-bullseye

COPY configs /app/configs
COPY checkpoints /app/checkpoints
COPY infer.py /app

WORKDIR /app

RUN pip install vietocr PyYAML pillow loguru Flask flask_cors
RUN pip install torch torchvision

EXPOSE 7000

CMD python infer.py --config_path=configs/configs.yml --port=7000