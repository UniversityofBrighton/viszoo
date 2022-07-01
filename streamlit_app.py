import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import pandas as pd
import numpy as np
import os

from altair_code.Seasonality import count_alt
from altair_code.Altitude import altitude_alt
from altair_code.time_spacial import geographic_alt
from altair_code.Family_counts_per_year import family_count_alt
from altair_code.Counts_per_researcher import researchers_alt


if 'first_load' not in st.session_state:

  from src.MNViz_colors import *

  root_dir = os.path.dirname(os.path.abspath(__file__))
  build_dir = os.path.join(root_dir, "component"+os.sep+"familia_selector"+os.sep+"frontend"+os.sep+"build")

  st.session_state['familia_selector'] = components.declare_component(
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

  #options
  st.set_page_config(layout='wide')
  st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
              unsafe_allow_html=True)

  familias_name = list(cores_familia.keys())
  familias_color = list(cores_familia.values())
  list_familias = list()

  for index in range(len(familias_name)):
    fam = dict()
    fam["name"] = familias_name[index]
    fam["color"] = familias_color[index]
    fam["selected"] = True
    list_familias.append(fam)

  st.session_state['list_familias'] = list_familias

  st.session_state['first_load'] = "oui"

else:
  min_year = st.session_state['min_year']
  max_year = st.session_state['max_year']
  list_familias = st.session_state['list_familias']
  data = st.session_state['data']

  

def familia_selector(familias):
    component_value = st.session_state['familia_selector'](familias = familias, default=familias, key="familia_selector_widget")
    return component_value

#available graphs definition
graphs_time = dict()

graphs_time['researchers'] = researchers_alt
#graphs_time['counts'] = count_alt
graphs_time['family count'] = family_count_alt

graphs_space = dict()

graphs_space['altitude'] = altitude_alt
graphs_space['geographic'] = geographic_alt



st.sidebar.title('VISUALISATION TOOL')

create_chart_time = graphs_time[st.sidebar.selectbox(label='choose a time graph', options=list(graphs_time.keys()))]

time1, time2 = st.sidebar.slider(label='time selector', min_value= min_year, max_value= max_year, value=(min_year, max_year))

#familia container
#familia_container = st.sidebar.container()

with st.sidebar:
  st.title('familia selector')
  list_familias = familia_selector(list_familias)

bool_familias = list(map(lambda x: x['selected'],list_familias))


#chart creation
chart_time = create_chart_time(data, bool_familias, time1, time2)
chart_space1 = altitude_alt(data, bool_familias, time1, time2)
chart_space2 = geographic_alt(data, bool_familias, time1, time2)

#graphs layout
time_col1, = st.columns(1)
space_col1, space_col2 = st.columns((1,1))

#graphs drawing
time_col1.altair_chart(chart_time, True)

space_col1.altair_chart(chart_space1, True)
space_col2.altair_chart(chart_space2, True)



