import os
import yaml
import time
import requests
import argparse

from pathlib import Path
from loguru import logger
from PIL import Image
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_parser():
  parser = argparse.ArgumentParser()
  
  parser.add_argument('--config', type=str, default='tools/configs/crawl.yml')
  
  return parser

if __name__ == '__main__':
  # Get CLI args
  parser = get_parser()
  args = parser.parse_args()
  
  # Load configs
  with open(args.config, 'r') as f:
    crawl_configs = yaml.load(f, yaml.FullLoader)
  
  logger.info('Configs: ' + str(crawl_configs))
  
  # Prepare dataset
  root_dir = os.path.join(crawl_configs['dir'], crawl_configs['name'])
  image_dir = os.path.join(root_dir, 'images')
  Path(image_dir).mkdir(parents=True, exist_ok=True)
  label_path = os.path.join(root_dir, 'labels.txt')
  
  # Init driver
  options = Options()
  selenium_configs = crawl_configs['selenium']
  if selenium_configs['headless']:
    options.add_argument("headless")
  if selenium_configs['max_size']:
    options.add_argument("start-maximized")
  
  chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  
  # Crawl
  for src in crawl_configs['sources']:
    
    # Src info
    src_configs = crawl_configs['sources'][src]
    url = src_configs['url']
    _id = src_configs['id']
    amount = src_configs['amount']
    start = src_configs['start_index']
    
    logger.info('=== Crawling image from {} ==='.format(src))
    
    chrome.get(url)
    time.sleep(2)
    
    for i in range(start, amount):

      # Capture image
      element = chrome.find_element(By.ID, _id)
      im = Image.open(BytesIO(element.screenshot_as_png))
      im_name = '{}{}.png'.format(src, str(i).zfill(selenium_configs['n_zeros']))
      im_path = '{}/{}'.format(image_dir, im_name)
      im.save(im_path)
      
      # Label using API
      response = requests.post(
        crawl_configs['label_api'],
        files={
          'file': open(im_path, 'rb')
        }
      )
      label = response.content.decode('utf-8').replace('"', '')
      logger.info('Crawl {:>6}/{} from {} - Label: {:>6}'.format(i + 1, amount, src, label))
      
      # Write to file
      with open(label_path, 'a') as f:
        f.write('{}\t{}\n'.format(
          'images/{}'.format(im_name),
          label
        ))
      
      # Refresh driver
      chrome.refresh()
      time.sleep(selenium_configs['delta'])
      
      
      
      
      
  
    
  
  
  
  