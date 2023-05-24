import os
import sys
import yaml
import pprint
import argparse

from loguru import logger
import streamlit as st

def get_parser():
  parser = argparse.ArgumentParser()
  
  parser.add_argument('--config', type=str, default='tools/configs/relabel.yml', help='Path to config file')
  
  return parser

if __name__ == '__main__':
  # Parse CLI args
  parser = get_parser()
  args = parser.parse_args()
  
  # Load config
  with open(args.config, 'r') as f:
    configs = yaml.load(f, yaml.FullLoader)
  logger.info('Configs: \n' + pprint.pformat(configs))
    
  # Params
  label_path = os.path.join(configs['root_dir'], configs['label_file'])
  new_label_path = os.path.join(configs['root_dir'], configs['new_label_file'])
  with open(label_path, 'r') as f:
    data = [tuple(line.strip().split('\t')) for line in f.readlines()]
  logger.info('Load {} data samples with old labels'.format(len(data)))
  
  # Continue previous job
  if not os.path.exists(new_label_path):
    current_index = 0
  
  else:
    with open(new_label_path, 'r') as f:
      current_index = len(f.readlines())
  logger.info('Start from index {}'.format(current_index))
      
  # Create an streamlit app
  st.set_page_config(layout='wide')
  # Title
  st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)
  st.title('Relabeling window')
  st.markdown('---')
  
  # Sidebar
  # st.sidebar.title('Configuration')
  # st.sidebar.markdown('---')
  # # TODO: ...

  # Main section: display image
  st.subheader('Displaying image from index **:blue[{}]** to index **:blue[{}]**'.format(current_index, current_index + configs['img_per_page'] - 1))

  new_labels = []
  for i in range(current_index, current_index + configs['img_per_page']):  
    st.markdown('---')
    cols = st.columns([2, 5])
    image_path, label = data[i]
    image_path = os.path.join(configs['root_dir'], image_path)
    cols[0].image(image_path, use_column_width=True)
    cols[1].success('Index: {} \t Image path: {}'.format(i, image_path))
    label_text = cols[1].text_input(label='Label', key='Label {}'.format(i), value=label, max_chars=5)
    new_labels.append(label_text)
  
  # Button
  st.markdown('---')
  st.text("")
  buttons = st.columns(2)
  confirm_button = buttons[0].button('Click to confirm the labels', key='Confirm button')
  buttons[1].markdown("<a style='border: solid #aaa 1px; border-radius: 6px; text-decoration: none; color: #333; padding: 6px 20px;' href='#linkto_top'>Back to top</a>", unsafe_allow_html=True)
  
  if confirm_button:
    for i in range(current_index, current_index + configs['img_per_page']):
      
      image_path, label = data[i]
      with open(new_label_path, 'a') as f:
        f.write('{}\t{}\n'.format(
          image_path,
          new_labels[i - current_index]
        ))
      
      logger.info('Done from index {} to index {}'.format(
        current_index,
        current_index + configs['img_per_page']
      ))
    
    st.experimental_rerun()