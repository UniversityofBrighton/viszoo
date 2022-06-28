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

from collections import defaultdict

# quick visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Waffle Charts
# from pywaffle import Waffle 
# docs: https://pywaffle.readthedocs.io/en/latest/examples/block_shape_distance_location_and_direction.html

# visualization
import altair as alt

# enabling notebook renderer
# alt.renderers.enable('notebook')
# alt.renderers.enable('default')

# disabling rows limit
alt.data_transformers.disable_max_rows()


# ## Importing data...

# In[2]:


NewTable = pd.read_csv('./data/treated_db.csv', sep=';', encoding='utf-8-sig', low_memory= False)


# <br>
# 
# <font size=5>**Color Pallete**</font>
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

# In[4]:


# importing customized color palettes
from src.MNViz_colors import *


# In[5]:


# input do especialista: Caudata é um erro da base
# cores_ordem = {
#     'Squamata': '#BF4417',
#     'Testudines': '#D9CB0B', 
#     'Crocodylia': '#284021',
# }

ordens = list(cores_ordem.keys())
cores = list(cores_ordem.values())


# <br>
# 
# 
# ## Graphs
# 
# ---
# ### Creating chart: counts per order per year

# In[6]:


orders = NewTable.groupby(['ano_coleta','ordem']).count()['class'].reset_index().rename(columns={'class':'counts'})

orders.sort_values(['ano_coleta','ordem'], inplace=True)  # ordering


# In[7]:


# dropping remaining NaN's
orders = orders.dropna(subset=['ordem'])


# In[12]:


g1 = alt.Chart(orders[orders['ordem'] != 'Caudata'],
               width=800, height=300, title='Number of collected specimens per order each year').mark_circle(
                                                                                color='green').encode(
    x= alt.X('ano_coleta', type='ordinal', title='Year'),
    y= alt.Y('ordem', type='nominal', title='Order',
            sort= alt.EncodingSortField(field='count', op='max', order='descending')),
    size = alt.Size('counts', scale=alt.Scale(range=[10,600])),
    color = alt.Color('ordem', scale= alt.Scale(domain=ordens, range=cores)),
    tooltip= alt.Tooltip(['ano_coleta', 'counts'])
)

g1 = g1.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving graph
# g1.save('./graphs/orders_per_year.html')
# g1


# ### number of reptiles per family per year

# In[13]:


teste = NewTable.groupby(['familia','ano_coleta']).count()['class'].reset_index().rename(
                                                                                    columns={'class':'counts'})

teste['ano_coleta'] = teste['ano_coleta'].astype(int)


# <br>
# 
# **graph:** family per year
# 
# <font color='red' size=5>From this point, we're using the family color palette</font>

# In[19]:


g1 = alt.Chart(teste,
               width=800, height=400, title='Number of collected animals of each family per year').mark_circle(
                                                                                size=60).encode(
    x= alt.X('ano_coleta', type='ordinal', title='Sampling Year'),
    y= alt.Y('familia', type='nominal', title='Family',
            sort= alt.EncodingSortField(field='counts', op='count', order='descending')),
    size= alt.Size('counts', title='Counts'),
    tooltip = alt.Tooltip(['familia', 'ano_coleta', 'counts'])
)

g1 = g1.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# g1.save('./graphs/families_per_year.html')
# g1


# ### Families per year (colored by order)

# In[20]:


teste = NewTable.groupby(['familia','ordem','ano_coleta']).count()['class'].reset_index().rename(
                                                                                    columns={'class':'counts'})

teste['ano_coleta'] = teste['ano_coleta'].astype(int)


# In[25]:


g1 = alt.Chart(teste, width=800, height=400, title='Number of collected specimens of each family per year'
              ).mark_circle(size=60).encode(
    x= alt.X('ano_coleta', type='ordinal', title='Sampling Year'),
    y= alt.Y('familia', type='nominal', title='Family',
            sort= alt.EncodingSortField(field='counts', op='count', order='descending')),
    size= alt.Size('counts', title='Count'),
    color = alt.Color('ordem', title= 'Order',scale= alt.Scale(domain=ordens, range=cores)),
    tooltip = alt.Tooltip(['familia', 'ano_coleta', 'counts'])
)

g1 = g1.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# g1.save('./graphs/families_per_year-by_order.html')
# g1


# <br>
# 
# ### Families per year (colored by family)

# In[26]:


teste = NewTable.groupby(['familia','ano_coleta']).count()['class'].reset_index().rename(
                                                                                    columns={'class':'counts'})

teste['ano_coleta'] = teste['ano_coleta'].astype(int)


# In[30]:


g1 = alt.Chart(teste,
               width=800, height=500, title='Number of collected specimens of each family per year').mark_circle(
                                                                                size=60).encode(
    x= alt.X('ano_coleta', type='ordinal', title='Collected Year'),
    y= alt.Y('familia', type='nominal', title='Family',
            sort= alt.EncodingSortField(field='counts', op='count', order='descending')),
    size= alt.Size('counts', title='Counts',
                   legend= alt.Legend(orient= 'right', direction= 'horizontal')),
    color = alt.Color('familia', title= 'Family',
                      legend= alt.Legend(columns=2, symbolLimit=50),
                      scale= alt.Scale(domain= list(cores_familia.keys()), range=list(cores_familia.values()))),
    tooltip = alt.Tooltip(['familia', 'ano_coleta', 'counts'])
)

g1 = g1.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# g1.save('./graphs/families_per_year_colorful.html')
# g1


# <br>
# 
# **The end!**
# 
# -----
