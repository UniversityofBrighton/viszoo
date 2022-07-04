import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import pandas as pd
import numpy as np
import os
from data_utils import *

from altair_code.Seasonality import count_alt
from altair_code.Altitude import altitude_alt
from altair_code.time_spacial import geographic_alt
from altair_code.Family_counts_per_year import family_count_alt
from altair_code.Counts_per_researcher import researchers_alt


if 'first_load' not in st.session_state:

  # loading families informations and color
  from src.MNViz_colors import *
  families_name = list(cores_familia.keys())
  families_color = list(cores_familia.values())
  list_families = list()

  for index in range(len(families_name)):
      fam = dict()
      fam["name"] = families_name[index]
      fam["color"] = families_color[index]
      fam["selected"] = True
      list_families.append(fam)

  st.session_state['list_families'] = list_families

  # loading my components
  root_dir = os.path.dirname(os.path.abspath(__file__))
  build_dir = os.path.join(root_dir, "components"+os.sep+"family_selector_component"+os.sep+"family_selector"+os.sep+"frontend"+os.sep+"build")

  st.session_state['family_selector'] = components.declare_component(
    "familia_selector",
    path=build_dir,
  )

  #loading the pandas csv
  data = pd.read_csv('./data/treated_db.csv', sep=';', encoding='utf-8-sig', low_memory= False)
  st.session_state['data'] = data

  #getting years for the slider
  years = np.unique(data['ano_coleta'].to_numpy())
  years = np.array(years, dtype='int')

  years = years[(years <= 2800) & (years > 1700)]

  min_year = int(min(years))
  max_year = int(max(years))

  st.session_state['min_year'] = min_year
  st.session_state['max_year'] = max_year

  st.session_state['first_load'] = "oui"

else:
  min_year = st.session_state['min_year']
  max_year = st.session_state['max_year']
  list_families = st.session_state['list_families']
  data = st.session_state['data']


# declarations
default_min_year = 1930


#options
st.set_page_config(layout='wide')
st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
          unsafe_allow_html=True)
  

def family_selector(families):
    component_value = st.session_state['family_selector'](familias = families, default=families, key="family_selector_widget")
    return component_value

#available graphs definition
graphs_time = dict()

graphs_time['researchers'] = researchers_alt
graphs_time['family count'] = family_count_alt

graphs_space = dict()

graphs_space['altitude'] = altitude_alt
graphs_space['geographic'] = geographic_alt


if 'file_uploaded' not in st.session_state:
  # handling file upload
  with st.sidebar:
    file = st.file_uploader(label='upload a file', type=['csv'], accept_multiple_files=False)
    if file != None:
      data = pd.read_csv(file, sep=';', encoding='utf-8-sig', low_memory= False)
      st.session_state['file_uploaded'] = 'oui'


selectors = st.sidebar.container()
with selectors:
  st.title('familia selector')
  list_families = family_selector(list_families)

families_filter = list(map(lambda x: x['selected'],list_families))
families_filter_out = list()
for fam in list_families:
  if not(fam['selected']):
    families_filter_out.append(fam['name'])


#main layout
title_col, _ = st.columns((4,1))
space_col1, space_col2 = st.columns((1,1))
select1, select2 = st.columns(2)
time_col1, = st.columns(1)

with title_col:
  st.title('VISUALISATION TOOL')


# selectors in main
with select1:
  time1, time2 = st.slider(label='time selector', min_value= min_year, max_value= max_year, value=(default_min_year, max_year))
with select2:
  create_chart_time = graphs_time[st.selectbox(label='choose a time graph', options=list(graphs_time.keys()))]


#chart creation
filtered_data = filter_data(data, families_filter_out, time1, time2)

chart_time = create_chart_time(filtered_data, (time1,time2))
chart_space1 = geographic_alt(filtered_data)
chart_space2 = altitude_alt(filtered_data)

#graphs drawing
time_col1.altair_chart(chart_time, True)

space_col1.altair_chart(chart_space1, True)
space_col2.altair_chart(chart_space2, True)



