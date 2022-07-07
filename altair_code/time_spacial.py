import numpy as np
import pandas as pd

# visualization
import altair as alt

# importing customized color palettes
from src.MNViz_colors import *

import streamlit as st

def geographic_alt(NewTable: pd.DataFrame):

    # corrects a typo (Améica do Sul)
    NewTable['continente'] = NewTable['continente'].apply(lambda x: 'América do Sul' if x=='Améica do Sul' else x)


    from vega_datasets import data

    source = alt.topo_feature(data.world_110m.url, 'countries')

    world = alt.Chart(source).mark_geoshape(
        fill='white',
        stroke='gray'
    ).project('naturalEarth1')

    tipos = NewTable['type_status'].astype(str).unique()

    #color_pal = alt.condition(alt.FieldOneOfPredicate("familia",new_fam),alt.Color('familia:N', title='Family', 
    #                    legend=None, 
    #                    scale= alt.Scale(domain= list(cores_familia.keys()), range= list(cores_familia.values()))),
    #                    alt.value('lightgray'))

    teste = alt.Chart(NewTable).mark_point(filled=True).encode(
        longitude = alt.X('long:Q', title='Longitude'),
        latitude = alt.Y('lat:Q', title='Latitude'),
        color= alt.Color('familia:N', title='Family', 
                        legend=None, 
                        scale= alt.Scale(domain= list(cores_familia.keys()), range= list(cores_familia.values()))),
        shape = alt.Shape('type_status:N', title='Type', scale= alt.Scale(domain=tipos), 
                        legend=None),
        tooltip = alt.Tooltip(['lat','long','pais','regiao','estado_ou_provincia',
                            'ano_coleta','mes_coleta', 'genero_atual','ordem', 'familia', 'type_status'])
    ).project(type='naturalEarth1')


    temp = (world + teste).configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )

    return temp

def timeX_family_continentY(data):

    teste = data.groupby(['ano_coleta','continente', 'familia']).count()['class'].reset_index().rename(columns={
    'class':'counts'
    })

    # database
    db = teste

    db = db.dropna(subset=['ano_coleta'])
    db['ano_coleta'] = db['ano_coleta'].astype(int)
    db[['continente','familia']] = db[['continente','familia']].astype(str)

    # auxiliar variables for encoding fields
    x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
    xmin = x_labels.min()
    xmax = x_labels.max()
    y_labels = db['continente'].unique()
    counts = db['counts'].unique()
    counts = list(range(min(counts), max(counts), 100))

    interval = alt.selection_interval()

    graph = alt.Chart(db, title='Registers Family by Continent', height=300, width=1400).mark_circle().encode(
        x= alt.X('ano_coleta', title='Sampling Year', 
                scale= alt.Scale(domain= [xmin,xmax])),
        y= alt.Y('continente:N', title='Continent', 
                scale= alt.Scale(domain= y_labels),
                sort=alt.EncodingSortField('counts', op="count", order='descending')), 
        size=alt.Size('counts', title='Counts',
                    legend= None,
                    scale= alt.Scale(domain= counts, range=[20,120])), 
        order= alt.Order('counts', sort='descending'),  # smaller points in front
    #     color= alt.Color('ordem', scale=alt.Scale(domain=ordens, range=cores)),  # old palette per order
        color= alt.Color('familia',title= 'Family', 
                        legend= None,
                        scale= alt.Scale(domain= list(cores_familia.keys()), range= list(cores_familia.values()))),
        tooltip= alt.Tooltip(['continente','ano_coleta','familia','counts'])
    ).properties(
            selection=interval
        )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph

def timeX_family_countryY(data):

    teste = data.groupby(['ano_coleta','pais', 'familia']).count()['class'].reset_index().rename(columns={
    'class':'counts'
    })

    # database
    db = teste

    # auxiliar variables for encoding fields
    x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
    xmin = x_labels.min()
    xmax = x_labels.max()
    y_labels = db['pais'].unique()
    counts = db['counts'].unique()
    counts = list(range(min(counts), max(counts), 100))

    graph = alt.Chart(db, title='Registers Family by Country', height=500, width=1400).mark_circle().encode(
        x= alt.X('ano_coleta', title='Sampling Year', 
                scale= alt.Scale(domain= [xmin,xmax])),
        y= alt.Y('pais:N', title='country', 
                scale= alt.Scale(domain= y_labels),
                sort=alt.EncodingSortField('counts', op="count", order='descending')), 
        size=alt.Size('counts', title='Counts',
                    legend= None,
                    scale= alt.Scale(domain= counts, range=[20,120])), 
        order= alt.Order('counts', sort='descending'),  # smaller points in front
    #     color= alt.Color('ordem', scale=alt.Scale(domain=ordens, range=cores)),  # old palette per order
        color= alt.Color('familia',title= 'Family', 
                        legend= None,
                        scale= alt.Scale(domain= list(cores_familia.keys()), range= list(cores_familia.values()))),
        tooltip= alt.Tooltip(['pais','ano_coleta','familia','counts'])
    )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph

def timeX_family_statesY(data):

    teste = data.groupby(['ano_coleta','estado_ou_provincia', 'familia']).count()['class'].reset_index().rename(columns={
    'class':'counts'
    })

    # database
    db = teste

    # auxiliar variables for encoding fields
    x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
    xmin = x_labels.min()
    xmax = x_labels.max()
    y_labels = db['estado_ou_provincia'].unique()
    counts = db['counts'].unique()
    counts = list(range(min(counts), max(counts), 100))

    graph = alt.Chart(db, title='Registers Family by Brazilian States', height=1500, width=1400).mark_circle().encode(
        x= alt.X('ano_coleta', title='Sampling Year', 
                scale= alt.Scale(domain= [xmin,xmax])),
        y= alt.Y('estado_ou_provincia:N', title='states', 
                scale= alt.Scale(domain= y_labels),
                sort=alt.EncodingSortField('counts', op="count", order='descending')), 
        size=alt.Size('counts', title='Counts',
                    legend= None,
                    scale= alt.Scale(domain= counts, range=[20,120])), 
        order= alt.Order('counts', sort='descending'),  # smaller points in front
    #     color= alt.Color('ordem', scale=alt.Scale(domain=ordens, range=cores)),  # old palette per order
        color= alt.Color('familia',title= 'Family', 
                        legend= None,
                        scale= alt.Scale(domain= list(cores_familia.keys()), range= list(cores_familia.values()))),
        tooltip= alt.Tooltip(['estado_ou_provincia','ano_coleta','familia','counts'])
    )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph