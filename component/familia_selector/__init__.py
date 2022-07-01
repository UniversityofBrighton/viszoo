import streamlit.components.v1 as components
import streamlit as st

_my_component = components.declare_component(
    "my_component",
    url="http://localhost:3001"
)

familias = list()

for i in range(87):
    newDict = dict()
    newDict["color"] = "#5270B0"
    newDict["name"] = 'familia {}'.format(i+1)
    newDict["selected"] = True
    familias.append(newDict)

families = _my_component(name='COMPONENT', familias=familias)

for fam in families:
    if fam["selected"]:
        st.write(fam["name"])