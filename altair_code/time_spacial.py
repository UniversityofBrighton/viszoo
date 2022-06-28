import numpy as np
import pandas as pd

# visualization
import altair as alt

# importing customized color palettes
from src.MNViz_colors import *

import streamlit as st

def geographic_alt(familia):
    # disabling rows limit
    alt.data_transformers.disable_max_rows()


    # ## Importing data...

    NewTable = pd.read_csv('./data/treated_db.csv', sep=';', encoding='utf-8-sig', low_memory=False)




    ordens = list(cores_ordem.keys())
    cores = list(cores_ordem.values())

    # corrects a typo (Améica do Sul)
    NewTable['continente'] = NewTable['continente'].apply(lambda x: 'América do Sul' if x=='Améica do Sul' else x)


    # looking good...
    NewTable['continente'].value_counts()


    from vega_datasets import data

    source = alt.topo_feature(data.world_110m.url, 'countries')

    world = alt.Chart(source).mark_geoshape(
        fill='white',
        stroke='gray'
    ).project('naturalEarth1')

# world

    # database
    db = NewTable.copy()
    db['type_status'] = db['type_status'].astype(str)  # parsing into string to make selector work
    tipos = db['type_status'].unique()

    # seletores
    select_order = alt.selection_multi(fields=['familia'], bind='legend')
    select_type = alt.selection_multi(fields=['type_status'], bind='legend')

    if familia != 'all':
        color_pal = alt.condition(alt.datum.familia == familia, alt.value('red'), alt.value('lightgray'))
    else:
        color_pal = alt.Color('familia:N', title='Family', 
                        legend=None, 
                        scale= alt.Scale(domain= list(cores_familia.keys()), range= list(cores_familia.values())))

    teste = alt.Chart(db).mark_point(filled=True).encode(
        longitude = alt.X('long:Q', title='Longitude'),
        latitude = alt.Y('lat:Q', title='Latitude'),
        color= color_pal,
        shape = alt.Shape('type_status:N', title='Type', scale= alt.Scale(domain=tipos), 
                        legend=None),
        tooltip = alt.Tooltip(['lat','long','pais','regiao','estado_ou_provincia',
                            'ano_coleta','mes_coleta', 'genero_atual','ordem', 'familia', 'type_status'])
    ).project(type='naturalEarth1').add_selection(select_order, 
                                select_type).transform_filter(select_order).transform_filter(select_type)

    temp = (world + teste).configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return temp