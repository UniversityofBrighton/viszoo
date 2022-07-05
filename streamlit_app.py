import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import pandas as pd
import numpy as np
import os
from data_utils import *

from altair_code.Seasonality import *
from altair_code.Altitude import *
from altair_code.time_spacial import *
from altair_code.Family_counts_per_year import *
from altair_code.Counts_per_researcher import *
from altair_code.Type_counts import *



#options
st.set_page_config(layout='wide')
st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
          unsafe_allow_html=True)

st.title('VisZoo Tool')

if 'file_uploaded' not in st.session_state:

  file = st.file_uploader(label='upload your file', type=['csv'], accept_multiple_files=False)
  if file != None:
    st.session_state['file'] = file
    st.session_state['file_uploaded'] = 'oui'
    st.experimental_rerun()

else:

  if 'data_loaded' not in st.session_state:

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
    build_dir_family = os.path.join(root_dir, "components"+os.sep+"family_selector_component"+os.sep+"family_selector"+os.sep+"frontend"+os.sep+"build")

    st.session_state['family_selector'] = components.declare_component(
      "family_selector",
      path=build_dir_family,
    )

    build_dir_type = os.path.join(root_dir, "components"+os.sep+"type_selector_component"+os.sep+"type_selector"+os.sep+"frontend"+os.sep+"build")

    st.session_state['type_selector'] = components.declare_component(
      "type_selector",
      path=build_dir_type,
    )

    #loading the pandas csv
    data = pd.read_csv(st.session_state['file'], sep=';', encoding='utf-8-sig', low_memory= False)
    st.session_state['data'] = data

    # handling types
    type_names = data['type_status'].unique()
    type_shapes = ['circle','square','triangle','square','square','square','square']
    list_types = list()
    for index in range(len(type_names)):
      new_type = dict()
      if str(type_names[index]) == 'nan':
        new_type['name'] = 'no type'
      else:
        new_type['name'] = str(type_names[index])
      new_type['shape'] = type_shapes[index]
      new_type['selected'] = True
      list_types.append(new_type)
    
    st.session_state['list_types'] = list_types

    #getting years for the slider
    years = np.unique(st.session_state['data']['ano_coleta'].to_numpy())
    years = np.array(years, dtype='int')

    years = years[(years <= 2800) & (years > 1700)]

    min_year = int(min(years))
    max_year = int(max(years))

    st.session_state['min_year'] = min_year
    st.session_state['max_year'] = max_year

    st.session_state['data_loaded'] = "oui"

  else:
    min_year = st.session_state['min_year']
    max_year = st.session_state['max_year']
    list_families = st.session_state['list_families']
    data = st.session_state['data']
    list_types = st.session_state['list_types']

  

  # declarations
  default_min_year = 1930
    

  def family_selector(families):
      component_value = st.session_state['family_selector'](familias = families, default=families, key="family_selector_widget")
      return component_value

  def type_selector(types):
    component_value = st.session_state['type_selector'](types = types, default = types, key="type_selector_widget")
    return component_value

  #available graphs definition
  graphs_time = dict()

  graphs_time['top 50 collector by species collected'] = timeX_collectorY_top50
  graphs_time['top 50 determiner by species determined'] = timeX_determinerY_top50
  graphs_time['collector by species collected'] = timeX_collectorY
  graphs_time['determiner by species determined'] = timeX_determinerY
  graphs_time['family count'] = timeX_family_countY
  graphs_time['family types count'] = timeX_family_countTypeY
  graphs_time['genus types count'] = timeX_genus_countTypeY
  graphs_time['collector types count'] = timeX_collector_countTypeY
  graphs_time['order count'] = timeX_order_countY
  graphs_time['type count'] = timeX_countTypeY
  graphs_time['families per continent'] = timeX_family_continentY
  graphs_time['families per country'] = timeX_family_countryY
  graphs_time['families per brazilian states'] = timeX_family_statesY
  graphs_time['seasonality'] = timeX_monthY


  graphs_space = dict()

  graphs_space['altitude per family'] = familyX_altitudeY
  graphs_space['altitude per genus'] = genusX_altitudeY
  graphs_space['geographic representation'] = geographic_alt


  selectors = st.sidebar.container()
  with selectors:
    st.title('family and type filters')
    list_families = family_selector(list_families)
    list_types = type_selector(list_types)

  families_filter = list(map(lambda x: x['selected'],list_families))
  families_filter_out = list()
  for fam in list_families:
    if not(fam['selected']):
      families_filter_out.append(fam['name'])

  type_filter_out = list()
  for typ in list_types:
    if not(typ['selected']):
      if typ['name'] == "nan":
        type_filter_out.append(np.nan)
      else:
        type_filter_out.append(typ['name'])


  #main layout
  title_col, _ = st.columns((4,1))
  space_col1, space_col2 = st.columns((1,1))
  select1, select2, select3 = st.columns((4,2,2))
  time_col1, = st.columns(1)


  # selectors in main
  with select1:
    time1, time2 = st.slider(label='time selector', min_value= min_year, max_value= max_year, value=(default_min_year, max_year))
  with select2:
    create_chart_time = graphs_time[st.selectbox(label='choose a time graph', options=list(graphs_time.keys()))]
  with select3:
    create_chart_space = graphs_space[st.selectbox(label='choose a spatial graph', options=list(graphs_space.keys()))]

  #chart creation
  filtered_data = filter_data(data, families_filter_out, type_filter_out, time1, time2)

  chart_time = create_chart_time(filtered_data)
  chart_space1 = geographic_alt(filtered_data)
  chart_space2 = create_chart_space(filtered_data)

  #graphs drawing
  time_col1.altair_chart(chart_time, True)

  space_col1.altair_chart(chart_space1, True)
  space_col2.altair_chart(chart_space2, True)
