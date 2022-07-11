import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import os
from data_utils import *
from graph_dict import get_graph_dicts
from src.MNViz_colors import *
from components_utils import load_components, get_selectors, get_filters_out

from data_treatment import *
from altair_code.Seasonality import *
from altair_code.Altitude import *
from altair_code.time_spacial import *
from altair_code.Family_counts_per_year import *
from altair_code.Counts_per_researcher import *
from altair_code.Type_counts import *

def core_app(app_version):

  if 'file_uploaded' not in st.session_state:
    
    file_ext = get_file_extension(app_version)

    # this is the first thing to show up when the app loads
    file = st.file_uploader(label='upload your file', type=[file_ext], accept_multiple_files=False)
    if file != None:
      st.session_state['file'] = file
      st.session_state['file_uploaded'] = 'oui'
      st.experimental_rerun()

  else:

    if 'data_loaded' not in st.session_state:

      # this sections plays when you just uploaded your data


      #loading the pandas dataframe from the excel file provided
      if app_version == 'reptiles':
        data = excel_to_dataframe_reptiles(st.session_state['file'])
      elif app_version == 'crustaceas':
        data = excel_to_dataframe_crustacea(st.session_state["file"])
      elif app_version == 'GBIF':
        data = GBIF_tsv_to_dataframe(st.session_state["file"])
      st.session_state['data'] = data

      family_selector, type_selector = load_components()
      st.session_state['family_selector'] = family_selector
      st.session_state['type_selector'] = type_selector


      colors = create_color_palettes(data, app_version)
      st.session_state['families'], st.session_state['orders'] = colors
      st.session_state['selectors_components'] = get_selectors(data, app_version, colors)

      #getting years for the slider
      years = np.unique(st.session_state['data']['year_collected'].to_numpy())
      years = np.array(years, dtype='int')

      years = years[(years <= 2800) & (years > 1700)]

      st.session_state['min_year'] = int(min(years))
      st.session_state['max_year'] = int(max(years))

      st.session_state["graphs_time"], st.session_state["graphs_space"] = get_graph_dicts(app_version)

      # the data is now loaded and the app is ready to work
      st.session_state['data_loaded'] = "oui"

      # this plays whenever the app is refreshed and the data has already been loaded,
      # I put a lot of variables in session_state so that it does not have to compute them again

    min_year = st.session_state['min_year']
    max_year = st.session_state['max_year']

    data = st.session_state['data']
    
    graphs_time = st.session_state["graphs_time"]
    graphs_space = st.session_state["graphs_space"]

    family_selector = st.session_state['family_selector']
    type_selector = st.session_state['type_selector']

    families = st.session_state['families']
    orders = st.session_state['orders']

    selectors_components = st.session_state['selectors_components']
    

    # declarations
    default_min_year = 1930
  

    # placing selectors in the sidebar
    selectors = st.sidebar.container()
    with selectors:
      st.title('family and type filters')
      list_filter_out = get_filters_out(selectors_components)

    # main layout definition
    title_col, _ = st.columns((4,1))
    space_col1, space_col2 = st.columns((1,1))
    select1, select2, select3 = st.columns((4,2,2))
    time_col1, = st.columns(1)


    # main selectors : a slider and two graph selectors
    with select1:
      time1, time2 = st.slider(label='time selector', min_value= min_year, max_value= max_year, value=(default_min_year, max_year))
    with select2:
      create_chart_time = graphs_time[st.selectbox(label='choose a time graph', options=list(graphs_time.keys()))]
    with select3:
      create_chart_space = graphs_space[st.selectbox(label='choose a spatial graph', options=list(graphs_space.keys()))]

    # filtering data according to all selectors
    filtered_data = filter_data(data, list_filter_out, time1, time2)

    # creating the charts using the filtered data
    chart_time = create_chart_time(filtered_data, app_version, (families, orders))
    chart_space1 = geographic_alt(filtered_data, app_version, (families, orders))
    chart_space2 = create_chart_space(filtered_data, app_version, (families, orders))

    # drawing the graphs using the streamlit dedicated altair API
    time_col1.altair_chart(chart_time, True)
    space_col1.altair_chart(chart_space1, True)
    space_col2.altair_chart(chart_space2, True)
    # all done