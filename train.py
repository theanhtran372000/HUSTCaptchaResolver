import time
import yaml
import argparse

import pprint
from loguru import logger

from vietocr.tool.config import Cfg
from vietocr.model.trainer import Trainer

def get_parser():
  parser = argparse.ArgumentParser()
  
  parser.add_argument('--config', type=str, default='configs/configs.yml', help='Path to config file')
  
  return  parser

if __name__ == '__main__':
  parser = get_parser()
  args = parser.parse_args()
  
  with open(args.config, 'r') as f:
    configs = yaml.load(f, yaml.FullLoader)['train']
  logger.info('Configs: \n' + pprint.pformat(configs))
  
  # Config training
  train_configs = Cfg.load_config_from_name('vgg_transformer')
  dataset_params = {
      'name': configs['dataset']['name'],
      'data_root': configs['dataset']['data_root'],
      'train_annotation': configs['dataset']['train_anno'],
      'valid_annotation': configs['dataset']['valid_anno']
  }

  trainer_params = {
    'print_every': configs['trainer']['print_every'],
    'valid_every': configs['trainer']['valid_every'],
    'iters': configs['trainer']['iters'],
    'export': configs['trainer']['export'],
    'metrics': configs['trainer']['metrics'],
    'batch_size': configs['trainer']['batch_size']
  }

  train_configs['trainer'].update(trainer_params)
  train_configs['dataset'].update(dataset_params)
  train_configs['device'] = configs['device']
  train_configs['vocab'] = configs['vocab']
  train_configs['optimizer']['max_lr'] = configs['optimizer']['max_lr']
  train_configs['dataloader']['num_workers'] = configs['dataset']['num_workers']
  
  logger.info('Train configs: \n' + pprint.pformat(train_configs))
  
  # Init trainer
  trainer = Trainer(train_configs, pretrained=configs['trainer']['pretrained'])
  trainer.config.save(configs['save_config_to'])
  
  # Train
  logger.info('Start training ...')
  start = time.time()
  trainer.train()
  logger.success('Done after {:.2f}s'.format(time.time() - start))