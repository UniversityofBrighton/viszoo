from importlib_metadata import version
import streamlit as st

from reptiles_app import reptile_app
from crustacea_app import crustacea_app

#options
st.set_page_config(layout='wide')
st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
          unsafe_allow_html=True)

st.title('VisZoo Tool')

app_versions = [
  'reptiles',
  'crustacea'
]

if 'app_version' not in st.session_state:
  
  app_version = st.selectbox(label='choose app version', options=app_versions)
  version_chosen = st.button(label='validate choice')
  if version_chosen:
    st.session_state['app_version'] = app_version
    st.experimental_rerun()

elif st.session_state['app_version'] == 'crustacea':
  crustacea_app()
elif st.session_state['app_version'] == 'reptiles':
  reptile_app()