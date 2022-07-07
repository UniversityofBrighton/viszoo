
import numpy as np
import pandas as pd

# visualization
import altair as alt

# importing customized color palettes
from src.MNViz_colors import *


def timeX_collectorY_top50(data:pd.DataFrame):

    # disabling rows limit
    alt.data_transformers.disable_max_rows()

    inter_data = data.groupby(['collector_full_name','ano_coleta', 'familia']).count()['class'].reset_index().rename(columns=
                                                                                {'class':'counts'})
    # getting range
    time_domain = inter_data.sort_values(['ano_coleta'])['ano_coleta'].unique()
    time_max = time_domain.max()
    time_min = time_domain.min()

    # summing and sorting contributions of each collector
    sumed_collector = inter_data.groupby('collector_full_name').sum()['counts'].reset_index().rename(
        columns={'counts':'sum'})
    sorted_collector = sumed_collector.sort_values('sum', ascending=False)

    # sorted names
    sort_list = sorted_collector['collector_full_name'].unique()

    # database
    data_vis = inter_data.where(inter_data['collector_full_name'].isin(sort_list[0:50]))

    counts = data_vis['counts']

    #color_pal = alt.condition(alt.FieldOneOfPredicate("familia",new_fam), alt.Color('familia', type="nominal", title="Family", legend = None,
    #                scale=alt.Scale(domain=familias, range=list(cores_familia.values()))), alt.value('lightgray'))


    graph = alt.Chart(data_vis, title= 'collection Registers by Top 50 collectors',
                width=800, height=700).mark_circle().encode(
        x= alt.X('ano_coleta', title='Sampling Year', scale=alt.Scale(domain=[time_min, time_max])),
        y= alt.Y('collector_full_name', type='nominal', title='Collector Name',
                sort= sort_list[0:50]),
        size= alt.Size('counts', title='Counts', scale= alt.Scale(range=[20,200]),
                    legend= None),
        order= alt.Order('counts', sort='descending'),  # smaller points in front
        color= alt.Color('familia', type="nominal", title="Family", legend = None,
                    scale=alt.Scale(domain= list(cores_familia.keys()), range=list(cores_familia.values()))),
        tooltip= alt.Tooltip(['collector_full_name', 'ano_coleta', 'counts', 'familia'])
    )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph

def timeX_collectorY(data):

    teste = data.groupby(['collector_full_name','ano_coleta','familia']).count()['class'].reset_index().rename(columns=
                                                                                            {'class':'counts'})


    sort_list = teste.sort_values('ano_coleta')['ano_coleta'].unique()
    time_min = sort_list.min()
    time_max = sort_list.max()

    graph = alt.Chart(teste, title='collection Registers by collector', width=800, height=10000).mark_circle().encode(
    x= alt.X('ano_coleta', title='Collected Year', scale=alt.Scale(domain=[time_min,time_max])),
    y= alt.Y('collector_full_name', type='nominal', title='Collector Name', 
            sort=alt.EncodingSortField('ano_coleta', op="min", order='ascending')),
    size= alt.Size('counts', scale=alt.Scale(range=[20, 350]), legend=None),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color = alt.Color('familia', type="nominal", title="Family", legend = None,
                    scale=alt.Scale(domain= list(cores_familia.keys()), range=list(cores_familia.values()))),
    tooltip= [alt.Tooltip('collector_full_name', title='collector name'),
            alt.Tooltip('ano_coleta', title='year collected'),
            alt.Tooltip('counts', title='count'),
            alt.Tooltip('familia',title='family')],
    )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph


def timeX_determinerY(data):

    teste = data.groupby(['determinator_full_name','ano_coleta','familia']).count()['class'].reset_index().rename(columns=
                                                                                            {'class':'counts'})


    sort_list = teste.sort_values('ano_coleta')['ano_coleta'].unique()
    time_min = sort_list.min()
    time_max = sort_list.max()

    graph = alt.Chart(teste, title='description Registers by determiner', width=800, height=2000).mark_circle().encode(
    x= alt.X('ano_coleta', title='Collected Year', scale=alt.Scale(domain=[time_min,time_max])),
    y= alt.Y('determinator_full_name', type='nominal', title='Determiner Name', 
            sort=alt.EncodingSortField('ano_coleta', op="min", order='ascending')),
    size= alt.Size('counts', scale=alt.Scale(range=[20, 350]), legend=None),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color = alt.Color('familia', type="nominal", title="Family", legend = None,
                    scale=alt.Scale(domain= list(cores_familia.keys()), range=list(cores_familia.values()))),
    tooltip= alt.Tooltip(['determinator_full_name', 'ano_coleta', 'counts']),
    )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph

def timeX_determinerY_top50(data):

    # disabling rows limit
    alt.data_transformers.disable_max_rows()

    inter_data = data.groupby(['determinator_full_name','ano_coleta', 'familia']).count()['class'].reset_index().rename(columns=
                                                                                {'class':'counts'})
    # getting range
    time_domain = inter_data.sort_values(['ano_coleta'])['ano_coleta'].unique()
    time_max = time_domain.max()
    time_min = time_domain.min()

    # summing and sorting contributions of each collector
    sumed_collector = inter_data.groupby('determinator_full_name').sum()['counts'].reset_index().rename(
        columns={'counts':'sum'})
    sorted_collector = sumed_collector.sort_values('sum', ascending=False)

    # sorted names
    sort_list = sorted_collector['determinator_full_name'].unique()

    # database
    data_vis = inter_data.where(inter_data['determinator_full_name'].isin(sort_list[0:50]))

    counts = data_vis['counts']

    #color_pal = alt.condition(alt.FieldOneOfPredicate("familia",new_fam), alt.Color('familia', type="nominal", title="Family", legend = None,
    #                scale=alt.Scale(domain=familias, range=list(cores_familia.values()))), alt.value('lightgray'))


    graph = alt.Chart(data_vis, title= 'description Registers by Top 50 determiners',
                width=800, height=700).mark_circle().encode(
        x= alt.X('ano_coleta', title='Sampling Year', scale=alt.Scale(domain=[time_min, time_max])),
        y= alt.Y('determinator_full_name', type='nominal', title='Determiner Name',
                sort= sort_list[0:50]),
        size= alt.Size('counts', title='Counts', scale= alt.Scale(range=[20,200]),
                    legend= None),
        order= alt.Order('counts', sort='descending'),  # smaller points in front
        color= alt.Color('familia', type="nominal", title="Family", legend = None,
                    scale=alt.Scale(domain= list(cores_familia.keys()), range=list(cores_familia.values()))),
        tooltip= alt.Tooltip(['determinator_full_name', 'ano_coleta', 'counts', 'familia'])
    )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph
