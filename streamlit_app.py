from importlib_metadata import version
import streamlit as st

from core_app import core_app
from crustaceas_app import crustacea_app
from GBIF_app import GBIF_app

#options
st.set_page_config(layout='wide')
st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
          unsafe_allow_html=True)

st.title('VisZoo Tool')

app_versions = [
  'reptiles',
  'crustaceas',
  'GBIF'
]

if 'app_version' not in st.session_state:
  
  app_version = st.selectbox(label='choose app version', options=app_versions)
  version_chosen = st.button(label='validate choice')
  if version_chosen:
    st.session_state['app_version'] = app_version
    st.experimental_rerun()

else:
  core_app(st.session_state["app_version"])