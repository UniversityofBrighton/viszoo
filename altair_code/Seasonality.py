
import numpy as np
import pandas as pd

# pacote para visualização principal
import altair as alt

def count_alt(NewTable, familia, time):

    # desabilitando limite de linhas
    alt.data_transformers.disable_max_rows()


    # droping NAN
    counts = NewTable.dropna(subset=['ano_coleta', 'mes_coleta'], how='all')
    counts = counts.where(counts['ano_coleta'] <= time)
    # grouping per time and order
    counts = counts.groupby(['ano_coleta', 'mes_coleta', 'ordem']).count()['class'].reset_index().rename(
                                                                                columns={'class':'counts'})

    # making sure month and year cols are int
    counts['ano_coleta'] = counts['ano_coleta'].astype(int)
    counts['mes_coleta'] = counts['mes_coleta'].astype(int)

    # scale for x axis
    anos = counts['ano_coleta'].unique()


    # In[12]:

    if familia != 'all':
            color_pal = alt.condition(alt.datum.familia == familia, alt.value('red'), alt.value('lightgray'))
    else:
        color_pal = alt.Color('counts', title='Counts', legend=None)

    temp = alt.Chart(counts[(~counts['ordem'].isna()) & (counts['ordem'] != 'Caudata')], 
                    title='Total of collected specimens per month/year',
                width=1200, height=200).mark_rect().encode(
            y = alt.Y('mes_coleta', type='ordinal', title='Collected Month',
                    sort= alt.EncodingSortField('mes_coleta', order='descending')),
            x = alt.X('ano_coleta', type='ordinal', title='Collected Year',
                    scale= alt.Scale(domain=anos)),
            color= color_pal,
            tooltip = alt.Tooltip(['counts', 'ano_coleta', 'mes_coleta'])
    )

    temp.facet(row='ordem').resolve_scale(x='independent').resolve_legend('independent').configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return temp