from locale import ALT_DIGITS
import streamlit as st
import altair as alt

from altair_code.Altitude import altitude_alt
from altair_code.time_spacial import geographic_alt
from src.MNViz_colors import *
#options
st.set_page_config(layout='wide')
st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
             unsafe_allow_html=True)

#loading charts

precol1, precol2 = st.columns(2)

precol1.title('VISUALISATION TOOL')

my_expander = precol2.expander(label='change graph')
with my_expander:
  st.button('graph1')
  st.button('graph2')

col1, col2, col3 = st.columns((1,4,2))

familias = list(cores_familia.keys())
familias.append('all')
familia = col3.selectbox(label='choose',options=familias, index=len(familias)-1)


chart1 = altitude_alt(familia)
world_chart = geographic_alt(familia)

col2.altair_chart(chart1, True)

col2.altair_chart(world_chart, True)



