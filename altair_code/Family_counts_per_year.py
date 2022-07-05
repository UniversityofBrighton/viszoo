# graph structures by **Franklin Oliveira**

import numpy as np
import pandas as pd

# visualization
import altair as alt
from src.MNViz_colors import *

def timeX_family_countY(NewTable):

    alt.renderers.enable('default')
    alt.data_transformers.disable_max_rows()

    teste = NewTable.groupby(['familia','ano_coleta']).count()['class'].reset_index().rename(
                                                                                        columns={'class':'counts'})

    teste = teste.dropna(subset=['ano_coleta'])
    teste['familia'] = teste['familia'].astype(str)
    teste['ano_coleta'] = teste['ano_coleta'].astype(int)

    sort_list = teste.sort_values('ano_coleta')['ano_coleta'].unique()
    time_min = sort_list.min()
    time_max = sort_list.max()

    graph = alt.Chart(teste,
                width=500, height=500, title='Number of collected specimens of each family per year').mark_circle(
                                                                                    size=60).encode(
        x= alt.X('ano_coleta', title='Collected Year', scale=alt.Scale(domain=[time_min, time_max])),
        y= alt.Y('familia', type='nominal', title='Family {} {}'.format(time_min, time_max),
                sort= alt.EncodingSortField(field='ano_coleta', op='min', order='ascending')),
        size= alt.Size('counts', title='Counts',
                    legend= None, scale=alt.Scale(range=[15,100])),
        color = alt.Color('familia:O', title= 'Family',
                        legend= None, scale= alt.Scale(domain= list(cores_familia.keys()), range=list(cores_familia.values()))),
        tooltip = alt.Tooltip(['familia', 'ano_coleta', 'counts'])
    )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph

def timeX_family_countTypeY(NewTable: pd.DataFrame):

    alt.renderers.enable('default')
    alt.data_transformers.disable_max_rows()

    NewTable = NewTable.dropna(subset=['type_status'])
    teste = NewTable.groupby(['familia','ano_coleta','type_status']).count()['class'].reset_index().rename(
                                                                                        columns={'class':'counts'})

    teste = teste.dropna(subset=['ano_coleta'])
    teste['familia'] = teste['familia'].astype(str)
    teste['ano_coleta'] = teste['ano_coleta'].astype(int)

    teste = teste.sort_values(['ano_coleta'])

    sort_list = teste['ano_coleta'].unique()
    time_min = sort_list.min()
    time_max = sort_list.max()


    #color_pal = alt.condition(alt.FieldOneOfPredicate("familia",new_fam), alt.Color('familia:O', title= 'Family',
    #                    legend= None, scale= alt.Scale(domain= list(cores_familia.keys()), range=list(cores_familia.values())))#, alt.value('lightgray'))

    graph = alt.Chart(teste, height=500, width=250, title='Types per Family').mark_point(filled=False).encode(
    x = alt.X('ano_coleta:Q', title='Description Year', 
              scale= alt.Scale(domain=[time_min, time_max])),
    y = alt.Y('familia:N', title= 'Family', sort= alt.EncodingSortField('ano_coleta', op='min', order='ascending')),
    color= alt.Color('familia:N', title='Family', legend=None,
                    scale= alt.Scale(domain= list(cores_familia.keys()), 
                                     range= list(cores_familia.values()))), 
    size= alt.Size('counts', title='Counts', legend= None,
                   scale=alt.Scale(range=[30,500])),
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    shape= alt.Shape('type_status:N', title='Type', legend= None), 
    tooltip= [alt.Tooltip('familia', title='family'),
              alt.Tooltip('type_status', title='type'),
              alt.Tooltip('ano_coleta:T', title='description year'),
              alt.Tooltip('counts', title='counts')]
)

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph


def timeX_genus_countTypeY(NewTable: pd.DataFrame):

        # database
    db = NewTable.groupby(['ano_coleta', 'genero_atual', 'type_status', 'familia']).count()['class'].reset_index().rename(columns={'class':'counts'})

    sort_list = db.sort_values('ano_coleta')['ano_coleta'].unique()
    time_min = sort_list.min()
    time_max = sort_list.max()

    graph = alt.Chart(db, height=500, width= 400, title='Types per Genus').mark_point(filled=False).encode(
        x = alt.X('ano_coleta:Q', title='Description Year',
                scale= alt.Scale(domain=[time_min, time_max])),
        y = alt.Y('genero_atual:N', title= 'Genus', sort=alt.EncodingSortField('ano_coleta',op='min',order='ascending')),
    #               sort=genus_order),
        color= alt.Color('familia:N', title='Family',
                        legend=None,
                        scale= alt.Scale(domain= list(cores_familia.keys()), range=list(cores_familia.values()))), 
        size= alt.Size('counts', title='Counts',
                    legend= None,
                    scale=alt.Scale(range=[30,500])),
        order= alt.Order('counts', sort='descending'),  # smaller points in front
        shape= alt.Shape('type_status:N', title='Type',
                        legend=None), 
        tooltip= [alt.Tooltip('familia', title='family'),
                alt.Tooltip('type_status', title='type'),
                alt.Tooltip('ano_coleta', title='description year'),
                alt.Tooltip('counts', title='counts')]
    )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph

def timeX_order_countY(NewTable):

    alt.renderers.enable('default')
    alt.data_transformers.disable_max_rows()

    teste = NewTable.groupby(['ordem','ano_coleta']).count()['class'].reset_index().rename(
                                                                                        columns={'class':'counts'})

    teste = teste.dropna(subset=['ano_coleta'])
    teste['ordem'] = teste['ordem'].astype(str)
    teste['ano_coleta'] = teste['ano_coleta'].astype(int)

    sort_list = teste.sort_values('ano_coleta')['ano_coleta'].unique()
    time_min = sort_list.min()
    time_max = sort_list.max()

    graph = alt.Chart(teste,
                width=500, height=500, title='Number of collected specimens of each family per year').mark_circle(
                                                                                    size=60).encode(
        x= alt.X('ano_coleta', title='Collected Year', scale=alt.Scale(domain=[time_min, time_max])),
        y= alt.Y('ordem', type='nominal', title='Family',
                sort= alt.EncodingSortField(field='ano_coleta', op='min', order='ascending')),
        size= alt.Size('counts', title='Counts',
                    legend= None, scale=alt.Scale(range=[15,100])),
        color = alt.Color('ordem:O', title= 'Family',
                        legend= None, scale= alt.Scale(domain= list(cores_ordem.keys()), range=list(cores_ordem.values()))),
        tooltip = alt.Tooltip(['ordem', 'ano_coleta', 'counts'])
    )

    graph = graph.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return graph
