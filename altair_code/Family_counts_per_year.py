#!/usr/bin/env python
# coding: utf-8

# # Family counts per year
# 
# By **Franklin Oliveira**
# 
# -----
# This notebook contains all code necessary to make the "type" charts from `repteis` database. Here you'll find some basic data treatment and charts' code. 
# 
# Database: <font color='blue'>'Compilacao Livros Repteis - 2 a 10 - 2020_04_28.xls'</font>.

# In[1]:


import datetime
import numpy as np
import pandas as pd

# visualization
import altair as alt
from src.MNViz_colors import *
from itertools import compress

def family_count_alt(NewTable, familia, time1, time2):

    alt.data_transformers.disable_max_rows()

    orders = NewTable.groupby(['ano_coleta','ordem']).count()['class'].reset_index().rename(columns={'class':'counts'})

    orders.sort_values(['ano_coleta','ordem'], inplace=True)  # ordering

    # dropping remaining NaN's
    orders = orders.dropna(subset=['ordem'])

    teste = NewTable.groupby(['familia','ano_coleta']).count()['class'].reset_index().rename(
                                                                                        columns={'class':'counts'})

    teste['ano_coleta'] = teste['ano_coleta'].astype(int)
    teste = teste.where((teste['ano_coleta'] <= time2) & (teste['ano_coleta'] >= time1))

    familias = list(cores_familia.keys())
    new_fam = list(compress(familias, familia))

    color_pal = alt.condition(alt.FieldOneOfPredicate("familia",new_fam), alt.Color('familia', title= 'Family',
                        legend= None,
                        scale= alt.Scale(domain= list(cores_familia.keys()), range=list(cores_familia.values()))), alt.value('lightgray'))


    g1 = alt.Chart(teste,
                width=800, height=500, title='Number of collected specimens of each family per year').mark_circle(
                                                                                    size=60).encode(
        x= alt.X('ano_coleta', title='Collected Year'),
        y= alt.Y('familia', type='nominal', title='Family',
                sort= alt.EncodingSortField(field='counts', op='count', order='descending')),
        size= alt.Size('counts', title='Counts',
                    legend= None),
        color = color_pal,
        tooltip = alt.Tooltip(['familia', 'ano_coleta', 'counts'])
    )

    g1 = g1.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return g1
