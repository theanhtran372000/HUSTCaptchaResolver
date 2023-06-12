import yaml
import argparse
import pprint

from PIL import Image
from loguru import logger

from flask import Flask, request
from flask_cors import CORS

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

SUPPPORTED_EXTENSIONS = ['png', 'jpg', 'jpeg']

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def get_parser():
  
  parser = argparse.ArgumentParser()
  
  parser.add_argument('--config_path', type=str, required=True, help='Path to config file')
  parser.add_argument('--port', type=int, default=8000, help='Port to listen')
  
  return parser


@app.route('/', methods=['POST'])
def predict():
  
  if 'file' not in request.files:
    return 'Key "file" not found!', 400
  
  # Get image from request
  file = request.files['file']
  ext = file.filename.split('.')[-1]
  logger.info('Recieve file {}'.format(file))
  
  if ext not in SUPPPORTED_EXTENSIONS:
    logger.error("{} not supported!".format(ext))
    return "Extension {} not supported!".format(ext), 400
  
  # Load input image
  image = Image.open(file)  
  
  # Get model output
  result = predictor.predict(image)
  logger.success('Predictor result: {}'.format(result))
  
  return result, 200

if __name__ == '__main__':
  # Parse CLI args
  parser = get_parser()
  args = parser.parse_args()
  
  # Load config
  with open(args.config_path, 'r') as f:
    configs = yaml.load(f, yaml.FullLoader)['infer']
  logger.info('Configs: \n' + pprint.pformat(configs))
  
  # Config model
  with open(configs['config'], 'r') as f:  
    model_configs = Cfg(yaml.load(f, yaml.FullLoader))
    model_configs['weights'] = configs['weights']
    model_configs['device'] = configs['device']
    model_configs['cnn']['pretrained'] = False
  logger.info('Model configs: \n' + pprint.pformat(model_configs))
  
  # Create predictor
  logger.info('Init model')
  predictor = Predictor(model_configs)
  
  # Run app
  logger.success('Model is running at port {}'.format(args.port))
  app.run(host='0.0.0.0', port=args.port, threaded=True)
  
  
  