
import numpy as np
import pandas as pd

# pacote para visualização principal
import altair as alt
from src.MNViz_colors import *

from itertools import compress

def timeX_monthY(data):

    # desabilitando limite de linhas
    alt.data_transformers.disable_max_rows()



    # droping NAN
    counts = data.dropna(subset=['ano_coleta', 'mes_coleta'], how='all')
    # grouping per time and order
    counts = counts.groupby(['ano_coleta', 'mes_coleta']).count()['class'].reset_index().rename(
                                                                                columns={'class':'counts'})

    # making sure month and year cols are int
    counts['ano_coleta'] = counts['ano_coleta'].astype(int)
    counts['mes_coleta'] = counts['mes_coleta'].astype(int)

    total = alt.Chart(counts, title='Total of collected specimens per month/year', width=1200, height=200).mark_rect().encode(
            y = alt.Y('mes_coleta', type='ordinal', title='Collected Month',
                    sort= alt.EncodingSortField('mes_coleta', order='descending')),
            x = alt.X('ano_coleta:O', title='Collected Year',),
            color= alt.Color('counts', title='Counts', scale=alt.Scale(scheme="yellowgreenblue"),legend=None),
            tooltip = alt.Tooltip(['counts', 'ano_coleta', 'mes_coleta'])
    )

    total.configure_title(fontSize=16).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ).configure_legend(
        labelFontSize=12,
        titleFontSize=12
    )

    return total