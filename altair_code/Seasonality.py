#!/usr/bin/env python
# coding: utf-8

# # Seasonality
# 
# By **Franklin Oliveira**
# 
# -----
# 
# This notebook contains Python code to generate seasonality visualizations on the `repteis` database. Here you'll find some basic data treatment and adjustments that presented necessary to make adjustments for the graph. <font color='blue'>'Compilacao Livros Repteis - 2 a 10 - 2020_04_28.xls'</font>.

# In[1]:


import datetime
import numpy as np
import pandas as pd

from collections import defaultdict

# pacotes para visualização rápida
import seaborn as sns
import matplotlib.pyplot as plt

# pacote para visualização principal
import altair as alt

# habilitando renderizador para notebook
# alt.renderers.enable('notebook')
# alt.renderers.enable('default')


# desabilitando limite de linhas
alt.data_transformers.disable_max_rows()


# ## Importing data...

# In[2]:


NewTable = pd.read_csv('./data/treated_db.csv', sep=';', encoding='utf-8-sig', low_memory= False)


# <br>
# 
# <font size=5>**Color Palette per Order**</font>
# 
# <!-- <img src="./src/paleta_cores.jpeg" width='500px'> -->
# 
# <!-- Cores: 
# 
# - verde_escuro: #284021
# - verde_claro: #88BF11
# - amarelo: #D9CB0B
# - laranja: #D99311
# - laranja_escuro: #BF4417
# - marrom-_laro: #BF8D7A -->

# In[3]:


# p.s.: caudata is an error and should be removed. 
cores_ordem = {
    'Squamata': '#BF4417',
    'Testudines': '#D9CB0B', 
    'Crocodylia': '#284021'
}

ordens = list(cores_ordem.keys())
cores = list(cores_ordem.values())


# <br>
# 
# ## Graphs
# 
# ### Total counts over time
# 
# <font color='red' size='4'>Idea given by Ronaldo: add marginal histograms </font>

# In[4]:


# removing NaN
counts = NewTable.dropna(subset=['ano_coleta', 'mes_coleta'], how='all')

# grouping 
counts = counts.groupby(['ano_coleta', 'mes_coleta']).count()['class'].reset_index().rename(
                                                                            columns={'class':'counts'})

# making sure month and year cols are int 
counts['ano_coleta'] = counts['ano_coleta'].astype(int)
counts['mes_coleta'] = counts['mes_coleta'].astype(int)


# In[6]:


total = alt.Chart(counts, title='Total of collected specimens per month/year', width=1200,
         height=200).mark_rect().encode(
    y = alt.Y('mes_coleta', type='ordinal', title='Sampling Month',
              sort= alt.EncodingSortField('mes_coleta', order='descending')),
    x = alt.X('ano_coleta', type='ordinal', title='Sampling Year'),
    color= alt.Color('counts', title='Counts', scale= alt.Scale(scheme='yellowgreenblue')),
    tooltip = alt.Tooltip(['counts', 'ano_coleta', 'mes_coleta'])
)

total = total.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# total.save('./graphs/seasonality/season-total.html')
# total


# <br>
# 
# ### counts over time (per order)

# In[7]:


# droping NAN
counts = NewTable.dropna(subset=['ano_coleta', 'mes_coleta'], how='all')

# grouping per time and order
counts = counts.groupby(['ano_coleta', 'mes_coleta', 'ordem']).count()['class'].reset_index().rename(
                                                                            columns={'class':'counts'})

# making sure month and year cols are int
counts['ano_coleta'] = counts['ano_coleta'].astype(int)
counts['mes_coleta'] = counts['mes_coleta'].astype(int)

# scale for x axis
anos = counts['ano_coleta'].unique()


# In[12]:


temp = alt.Chart(counts[(~counts['ordem'].isna()) & (counts['ordem'] != 'Caudata')], 
                 title='Total of collected specimens per month/year',
             width=1200, height=200).mark_rect().encode(
        y = alt.Y('mes_coleta', type='ordinal', title='Collected Month',
                  sort= alt.EncodingSortField('mes_coleta', order='descending')),
        x = alt.X('ano_coleta', type='ordinal', title='Collected Year',
                 scale= alt.Scale(domain=anos)),
        color= alt.Color('counts', title='Counts'),
        tooltip = alt.Tooltip(['counts', 'ano_coleta', 'mes_coleta'])
)

temp.facet(row='ordem').resolve_scale(x='independent').resolve_legend('independent').configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
).save('./graphs/seasonality/order/season-faceted.html')

# temp.facet(row='ordem').resolve_scale(x='independent').resolve_legend('independent').configure_title(fontSize=16).configure_axis(
#     labelFontSize=12,
#     titleFontSize=12
# ).configure_legend(
#     labelFontSize=12,
#     titleFontSize=12
# )

# temp


# In[13]:


# unique range for color scale
min_ct = counts['counts'].min()
max_ct = counts['counts'].max()


# In[14]:


color_schemes = {
    'Squamata':'oranges',
    'Testudines':'yelloworangebrown',
    'Crocodylia':'greens'
}


# In[15]:


# independent graphs (per order)
for ordem in ordens:
    temp = alt.Chart(counts[counts['ordem'] == ordem], title=f'Total of collected {ordem} per month/year',
             width=1200, height=200).mark_rect().encode(
        y = alt.Y('mes_coleta', type='ordinal', title='Sampling Month',
                  sort= alt.EncodingSortField('mes_coleta', order='descending')),
        x = alt.X('ano_coleta', type='ordinal', title='Sampling Year',
                 scale= alt.Scale(domain=anos)),
        color= alt.Color('counts', title='Counts', scale=alt.Scale(domain=list(range(min_ct, max_ct)),
                                                                  scheme=color_schemes[ordem])),
        tooltip = alt.Tooltip(['counts', 'ano_coleta', 'mes_coleta'])
    )
    
    temp = temp.configure_title(fontSize=16).configure_axis(
                    labelFontSize=12,
                    titleFontSize=12
                ).configure_legend(
                    labelFontSize=12,
                    titleFontSize=12
                )
    
    temp.save(f'./graphs/seasonality/order/season-{ordem}.html')


# -----
# 
# **That's it!**
