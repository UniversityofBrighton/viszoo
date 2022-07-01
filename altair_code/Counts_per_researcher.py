
import numpy as np
import pandas as pd

# visualization
import altair as alt

# importing customized color palettes
from src.MNViz_colors import *
from itertools import compress


def researchers_alt(NewTable, familia, time1, time2):

    # alt.renderers.enable('notebook')
    alt.renderers.enable('default')

    # disabling rows limit
    alt.data_transformers.disable_max_rows()

    teste1 = NewTable.groupby(['collector_full_name','ano_coleta', 'familia']).count()['class'].reset_index().rename(columns=
                                                                                                {'class':'counts'})
    teste1 = teste1.where((teste1['ano_coleta'] <= time2) & (teste1['ano_coleta'] >= time1))
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

    familias = list(cores_familia.keys())
    new_fam = list(compress(familias, familia))

    color_pal = alt.condition(alt.FieldOneOfPredicate("familia",new_fam), alt.Color('familia', type="nominal", title="Family", legend = None,
                    scale=alt.Scale(domain=familias, range=list(cores_familia.values()))), alt.value('lightgray'))

    g2 = alt.Chart(db, title= 'Top 50',
                width=800, height=700).mark_circle().encode(
        x= alt.X('ano_coleta', title='Sampling Year', scale=alt.Scale(domain=(time1,time2))),
        y= alt.Y('collector_full_name', type='nominal', title='Collector Name', 
    #              scale= alt.Scale(domain= y_labels),
                sort= sort_list[0:50]),
        order= alt.Order('counts', sort='descending'),  # smaller points in front
        color= color_pal,
        tooltip= alt.Tooltip(['collector_full_name', 'ano_coleta', 'counts', 'familia'])
    ).interactive()

    g2 = g2.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return g2
