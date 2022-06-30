from locale import ALT_DIGITS
from altair_code.Family_counts_per_year import family_count_alt
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

from altair_code.Seasonality import count_alt
from altair_code.Altitude import altitude_alt
from altair_code.time_spacial import geographic_alt
from altair_code.Counts_per_researcher import researchers_alt
from src.MNViz_colors import *
#options
st.set_page_config(layout='wide')
st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
             unsafe_allow_html=True)

#loading charts

NewTable = pd.read_csv('./data/treated_db.csv', sep=';', encoding='utf-8-sig', low_memory= False)
years = np.unique(NewTable['ano_coleta'].to_numpy())
years = np.array(years, dtype='int')

years = years[(years <= 2800) & (years > 1700)]

min_year = int(min(years))
max_year = int(max(years))

graphs_time = dict()

graphs_time['researchers'] = researchers_alt
#graphs_time['counts'] = count_alt
graphs_time['family count'] = family_count_alt

graphs_space = dict()

graphs_space['altitude'] = altitude_alt
graphs_space['geographic'] = geographic_alt

time_col1, = st.columns(1)

st.sidebar.title('VISUALISATION TOOL')

create_chart_time = graphs_time[st.sidebar.selectbox(label='choose a time graph', options=list(graphs_time.keys()))]
#create_chart_space = graphs_space[st.sidebar.selectbox(label='graph 2', options=list(graphs_space.keys()))]

familias = list(cores_familia.keys())
familias_color = cores_familia
selected_familias = list()

time1, time2 = st.sidebar.slider(label='time selector', min_value= min_year, max_value= max_year, value=(min_year, max_year))

familia_container = st.sidebar.container()

familia_container.title('familia selector')

for fam in familias:
  familia_container.markdown('<div style="background-color: {}; border-radius:15px; display:inline-block; vertical-align:middle; height:10px; width:10px;"></div><div style="display:inline-block; padding-left:15px;">  {}</div>'.format(cores_familia[fam],fam), unsafe_allow_html=True)
  selected_familias.append(familia_container.checkbox(label="", value=True, key='check_{}'.format(fam)))


chart_time = create_chart_time(NewTable, selected_familias, time1, time2)
chart_space1 = altitude_alt(NewTable, selected_familias, time1, time2)
chart_space2 = geographic_alt(NewTable, selected_familias, time1, time2)

time_col1.altair_chart(chart_time, True)

space_col1, space_col2 = st.columns((1,1))

space_col1.altair_chart(chart_space1, True)

space_col2.altair_chart(chart_space2, True)



