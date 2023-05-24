import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("headless")
options.add_argument("start-maximized")
chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
chrome.get("https://dk-sis.hust.edu.vn/Users/Login.aspx")

time.sleep(2)

# Capture element
from PIL import Image
from io import BytesIO

for i in range(100):
  print('Crawl {}th image!'.format(i + 1))
  element = chrome.find_element(By.ID, 'ccCaptcha_IMG')
  im = Image.open(BytesIO(element.screenshot_as_png))
  im.save('save/test/{}.png'.format(i + 1))
  chrome.refresh()
  time.sleep(1)

chrome.quit()