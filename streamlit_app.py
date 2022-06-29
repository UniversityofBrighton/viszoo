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
graphs_time['counts'] = count_alt
graphs_time['counts2'] = family_count_alt

graphs_space = dict()

graphs_space['altitude'] = altitude_alt
graphs_space['geographic'] = geographic_alt

col1, col2 = st.columns((3,1))

my_expander = st.sidebar.expander(label='change graph')
with my_expander:
  create_chart_time = graphs_time[st.selectbox(label='graph 1', options=list(graphs_time.keys()))]
  create_chart_space = graphs_space[st.selectbox(label='graph 2', options=list(graphs_space.keys()))]

familias = list(cores_familia.keys())
familias.append('all')
familia = st.sidebar.selectbox(label='familia selector', options=familias, index=len(familias)-1)

time = st.sidebar.slider(label='time selector', min_value= min_year, max_value= max_year, value=max_year)


chart_time = create_chart_time(NewTable, familia, time)
chart_space = create_chart_space(NewTable, familia, time)

col1.altair_chart(chart_time, True)
col1.altair_chart(chart_space, True)

st.title('VISUALISATION TOOL')



