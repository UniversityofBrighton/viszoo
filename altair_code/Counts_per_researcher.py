
import numpy as np
import pandas as pd

# visualization
import altair as alt

# importing customized color palettes
from src.MNViz_colors import *


def researchers_alt(NewTable, familia, time):

    # alt.renderers.enable('notebook')
    alt.renderers.enable('default')

    # disabling rows limit
    alt.data_transformers.disable_max_rows()


    ordens = list(cores_ordem.keys())
    cores = list(cores_ordem.values())

    teste1 = NewTable.groupby(['collector_full_name','ano_coleta', 'familia']).count()['class'].reset_index().rename(columns=
                                                                                                {'class':'counts'})
    teste1 = teste1.where(teste1['ano_coleta'] <= time)
    # ordenando
    teste1.sort_values(['ano_coleta', 'collector_full_name'], inplace=True)

    # summing contributions of each collector
    sorting = teste1.groupby('collector_full_name').sum()['counts'].reset_index().rename(
        columns={'counts':'sum'})

    sorting = sorting.sort_values('sum', ascending=False)

    # sorted names
    sort_list = sorting['collector_full_name'].unique()

    # database
    db = teste1[teste1['collector_full_name'].isin(sort_list[0:50])]

    # aux. variables & filtering out some families (that doesn't have determiner name or year)
    familias = [f for f in cores_familia.keys() if f in 
                teste1[teste1['collector_full_name'].isin(sort_list[50:900])]['familia'].unique()]
    cores_temp = [cores_familia[f] for f in familias]
    x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
    y_labels = sort_list[50:900]
    temp = db['counts'].unique()

    # selector
    select_family = alt.selection_multi(fields= ['familia'], bind='legend')

    if familia != 'all':
        color_pal = alt.condition(alt.datum.familia == familia, alt.value('red'), alt.value('lightgray'))
    else:
        color_pal = alt.Color('familia', type="nominal", title="Family", legend = None,
                        scale=alt.Scale(domain=familias, range=cores_temp))

    g2 = alt.Chart(db, title= 'Top 50',
                width=800, height=700).mark_circle().encode(
        x= alt.X('ano_coleta', type='ordinal', title='Sampling Year',
                scale= alt.Scale(domain= x_labels)),
        y= alt.Y('collector_full_name', type='nominal', title='Collector Name', 
    #              scale= alt.Scale(domain= y_labels),
                sort= sort_list[50:900]),
        order= alt.Order('counts', sort='descending'),  # smaller points in front
        color= color_pal,
        tooltip= alt.Tooltip(['collector_full_name', 'ano_coleta', 'counts', 'familia'])
    ).add_selection(select_family).transform_filter(select_family)

    g2 = g2.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return g2