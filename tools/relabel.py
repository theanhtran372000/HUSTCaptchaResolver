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
  error_path = os.path.join(configs['root_dir'], 'errors.txt')
  
  with open(label_path, 'r') as f:
    data = [tuple(line.strip().split('\t')) for line in f.readlines()]
  logger.info('Load {} data samples with old labels'.format(len(data)))
  
  if os.path.exists(error_path):
    with open(error_path, 'r') as f:
      error_cnt = int(f.read().strip())
  else:
    error_cnt = 0
  
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

  start_index = current_index
  end_index = current_index + configs['img_per_page'] if current_index + configs['img_per_page'] <= len(data) else len(data)
  
  if start_index < end_index:
  
    # Main section: display image
    st.subheader('Displaying image from index **:blue[{}]** to index **:blue[{}]**'.format(start_index, end_index))
    st.error('Error count: **{}**'.format(error_cnt))
    
    new_labels = []
    old_labels = []
    
    for i, (image_path, label) in enumerate(data[start_index : end_index]):  
      st.markdown('---')
      cols = st.columns([2, 5])
      image_path = os.path.join(configs['root_dir'], image_path)
      cols[0].image(image_path, use_column_width=True)
      cols[1].success('Index: {} \t Image path: {}'.format(i + start_index, image_path))
      old_labels.append(label)
      
      label_text = cols[1].text_input(label='Label', key='Label {}'.format(i), value=label, max_chars=5)
      new_labels.append(label_text)
    
    # Button
    st.markdown('---')
    st.text("")
    buttons = st.columns(2)
    confirm_button = buttons[0].button('Click to confirm the labels', key='Confirm button')
    buttons[1].markdown("<a style='border: solid #aaa 1px; border-radius: 6px; text-decoration: none; color: #333; padding: 6px 20px;' href='#linkto_top'>Back to top</a>", unsafe_allow_html=True)
    
    if confirm_button:
      for i in range(start_index, end_index):
        
        image_path, label = data[i]
        with open(new_label_path, 'a') as f:
          f.write('{}\t{}\n'.format(
            image_path,
            new_labels[i - start_index]
          ))
          
        with open(error_path, 'w') as f:
          cnt = 0
          for i in range(end_index - start_index):
            if new_labels[i] != old_labels[i]:
              cnt += 1
              
          f.write(str(cnt + error_cnt))
          logger.info('Find {} wrong labels!'.format(cnt))
        
        logger.info('Done from index {} to index {}'.format(
          start_index,
          end_index
        ))
      
      st.experimental_rerun()
  
  else:
    st.success('All samples are relabeled!')