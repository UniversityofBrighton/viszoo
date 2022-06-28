#!/usr/bin/env python
# coding: utf-8

# # Counts per researcher
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
alt.renderers.enable('default')

# disabling rows limit
alt.data_transformers.disable_max_rows()


# ## Importing data...

# In[2]:


NewTable = pd.read_csv('./data/treated_db.csv', sep=';', encoding='utf-8-sig', low_memory= False)


# <br>
# 
# <font size=5>**Color Palette**</font>
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


# importing customized color palettes
from src.MNViz_colors import *


# In[4]:


# p.s.: Caudata is an error and should be removed
# cores_ordem = {
#     'Squamata': '#BF4417',
#     'Testudines': '#D9CB0B', 
#     'Crocodylia': '#284021'
# }

ordens = list(cores_ordem.keys())
cores = list(cores_ordem.values())


# **Paleta de Cores - Família:**
# 
# - grupo 1: 1 cor  (verde escuro)
# <ul>
#     <li style="color:#142611"><b>centroide 1</b></li>
# </ul>
# - grupo 2: 8 cores
# <ul>
#     <li style="color:#85D907"><b>centroide 2</b></li>
# </ul>
# 
# ['#d7ff81', '#bafd62', '#9feb3f', '#85d907', '#6cc700', '#52b700', '#35a600', '#0b9700', '#008800']
# 
# <font color="#d7ff81"><b>cor 1</b> (ficou fora)</font>
# <font color="#bafd62"><b>cor 2</b></font>
# <font color="#9feb3f"><b>cor 3</b></font>
# <font color="#85d907"><b>cor 4</b></font>
# <font color="#6cc700"><b>cor 5</b></font>
# <font color="#52b700"><b>cor 6</b></font>
# <font color="#35a600"><b>cor 7</b></font>
# <font color="#0b9700"><b>cor 8</b></font>
# <font color="#008800"><b>cor 9</b></font>
# 
# 
# - grupo 3: 2 cores
# #888C03
# <ul>
#     <li style="color:#22401E"><b>centroide 3 (puxando para tons frios mais claros)</b></li>
# </ul>
# 
# <font color="#99b6b2"><b>cor 1</b></font>
# <font color="#81a58b"><b>cor 2</b></font>
# 
# 
# - grupo 4: 1 cor  (amarelo)
# <ul>
#     <li style="color:#F2CB07"><b>centroide 4</b></li>
# </ul>
# 
# - grupo 5: 10 cores
# <ul>
#     <li style="color:#cb97d4"><b>centroide 5 (puxando para o roxo)</b></li>
# </ul>
# 
# ['#f8dcf9', '#ebc5ed', '#ddafe2', '#ce9ad6', '#bf86cc', '#af73c2', '#a160b8', '#924fae', '#833fa4'] #803da1
# 
# <font color="#f8dcf9"><b>cor 1</b></font>
# <font color="#ebc5ed"><b>cor 2</b></font>
# <font color="#ddafe2"><b>cor 3</b></font>
# <font color="#ce9ad6"><b>cor 4</b></font>
# <font color="#bf86cc"><b>cor 5</b></font>
# <font color="#af73c2"><b>cor 6</b></font>
# <font color="#a160b8"><b>cor 7</b></font>
# <font color="#924fae"><b>cor 8</b></font>
# <font color="#833fa4"><b>cor 9</b></font>
# <font color="#803da1"><b>cor 10</b></font>
# 
# 
# - grupo 6: 12 cores
# <ul>
#     <li style="color:#91F2E9"><b>centroide 6</b></li>
# </ul>
# 
# ['#c9fff9', '#b3eff2', '#9cdcea', '#83c9e2', '#68b7da', '#4aa6d2', '#2096ca', '#0087c1', '#0079b7']
# 
# ['#cee5d8', '#b3d2d1', '#9bbfc9', '#83adc2', '#6d9bba', '#568ab2', '#3e7baa', '#226ca2', '#005e98']
# 
# 
# <font color="#c9fff9"><b>cor 1</b></font>
# <font color="#b3eff2"><b>cor 2</b></font>
# <font color="#9cdcea"><b>cor 3</b></font>
# <font color="#83c9e2"><b>cor 4</b></font>
# <font color="#68b7da"><b>cor 5</b></font>
# <font color="#4aa6d2"><b>cor 6</b></font>
# <font color="#2096ca"><b>cor 7</b></font>
# <font color="#0087c1"><b>cor 8</b></font>
# <font color="#0079b7"><b>cor 9</b></font>
# <font color="#3e7baa"><b>cor 10</b></font>
# <font color="#226ca2"><b>cor 11</b></font>
# <font color="#005e98"><b>cor 12</b></font>
# 
# 
# - grupo 7: 3 cores
# <ul>
#     <li style="color:#8C1A0F"><b>centroide 7 (puxando para o marrom)</b></li>
# </ul>
# 
# ['#fde5bf', '#efd09f', '#e1bb82', '#d3a767', '#c6934d', '#b98033', '#ac6f18', '#9e5e00', '#914e00']
# 
# <font color="#ac6f18"><b>cor 1</b></font>
# <font color="#9e5e00"><b>cor 2</b></font>
# <font color="#914e00"><b>cor 3</b></font>
# 
# 
# - grupo 8: 13 cores
# <ul>
#     <li style="color:#D9430D"><b>centroide 8</b></li>
# </ul>
# 
# ['#ffce9f', '#ffb683', '#ff9f69', '#ff8851', '#f5723b', '#e75b25', '#d9430d', '#cb2800', '#bc0000']
# 
# ['#ff8f68', '#ff7e56', '#ff6b40', '#ee5829', '#d9430d', '#c62f00', '#b41b00', '#a40300', '#930000']
# 
# <font color="#ffce9f"><b>cor 1</b></font>
# <font color="#ffb683"><b>cor 2</b></font>
# <font color="#ff9f69"><b>cor 3</b></font>
# <font color="#ff8851"><b>cor 4</b></font>
# <font color="#f5723b"><b>cor 5</b></font>
# <font color="#e75b25"><b>cor 6</b></font>
# <font color="#d9430d"><b>cor 7</b></font>
# <font color="#cb2800"><b>cor 8</b></font>
# <font color="#bc0000"><b>cor 9</b></font>
# <font color="#c62f00"><b>cor 10</b></font>
# <font color="#b41b00"><b>cor 11</b></font>
# <font color="#a40300"><b>cor 12</b></font>
# <font color="#930000"><b>cor 13</b></font>
# 
# <br>
# 
# **TOTAL: 50 cores**

# <br>
# 
# 
# ## Graphs
# 
# ---
# ### Creating chart: counts per determiner per year

# In[5]:


teste = NewTable.groupby(['determinator_full_name','ano_determinacao']).count()['class'].reset_index().rename(columns=
                                                                                            {'class':'counts'})


# In[6]:


g1 = alt.Chart(teste, title= 'Counts per determiner',width=800, height=2200).mark_circle().encode(
    x= alt.X('ano_determinacao', type='ordinal', title='Determined Year'),
    y= alt.Y('determinator_full_name', type='nominal', title='Determiner Name', 
            sort=alt.EncodingSortField('counts', op="count", order='descending')),
    size= alt.Size('counts', scale=alt.Scale(range=[15, 500])),  # range ajusta tamanho do circulo
    tooltip= alt.Tooltip(['determinator_full_name', 'ano_determinacao', 'counts'])
)

g1 = g1.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# g1.save('./graphs/determiner/counts_per_determiner.html')
# g1


# <br>
# 
# <font color='red' size='5'>same chart, including families while grouping</font>
# 
# **p.s.:** Note that the counts will change as we're rearranging by one more field
# 
# ### counts per year (rearranged by sum)

# In[7]:


teste1 = NewTable.groupby(['determinator_full_name','ano_determinacao', 'familia']).count()['class'].reset_index().rename(columns=
                                                                                            {'class':'counts'})


# In[8]:


# database
db = teste1

# aux. variables & filtering out some families (that doesn't have determiner name or year)
# familias = [f for f in cores_familia.keys() if f in teste1['familia'].unique()]
# cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_determinacao')['ano_determinacao'].unique()
temp = db.groupby('determinator_full_name').sum().reset_index().sort_values('counts', ascending=False)
y_labels = temp['determinator_full_name'].unique()
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 100))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')


g2 = alt.Chart(db, title= 'Counts per determiner (sorted by sum)', 
               width=800, height=2200).mark_circle().encode(
    x= alt.X('ano_determinacao:O', title='Determination Year',
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('determinator_full_name:N', title='Determiner Name', 
             scale= alt.Scale(domain= y_labels),
             sort=alt.EncodingSortField('counts', op="sum", order='descending')),
    size= alt.Size('counts:Q', title= 'Counts', 
                   legend= alt.Legend(orient= 'right', direction= 'horizontal', tickCount=4),
                   scale=alt.Scale(domain= counts, range=[20, 120], zero=True)),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain=list(cores_familia.keys()), 
                                     range=list(cores_familia.values()))),
    tooltip= alt.Tooltip(['determinator_full_name', 'ano_determinacao', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/determiner/counts_per_determiner-wFamilies.html')
# g2


# <br>
# 
# <font color='red'>**same chart, now rearranging by the first year the determiner shows up on the database**</font>

# In[9]:


# ordenando
teste1.sort_values(['ano_determinacao', 'determinator_full_name'], inplace=True)

# salvando ordem das entradas
sorting = list(teste1['determinator_full_name'].unique())


# In[10]:


# database
db = teste1

# aux. variables & filtering out some families (that doesn't have determiner name or year)
# familias = [f for f in cores_familia.keys() if f in teste1['familia'].unique()]
# cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_determinacao')['ano_determinacao'].unique()
y_labels = db.sort_values('ano_determinacao')['determinator_full_name'].unique()
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 100))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')

g2 = alt.Chart(teste1, title= 'Counts per determiner (rearranged by first year of appearance)', 
               width=800, height=1400).mark_circle().encode(
    x= alt.X('ano_determinacao', type='ordinal', title='Determination Year',
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('determinator_full_name', type='nominal', title='Determiner Name', 
             scale= alt.Scale(domain= y_labels),
             sort=sorting),
    size= alt.Size('counts', type="quantitative", title= 'Counts',
                   legend= alt.Legend(orient= 'right', direction= 'horizontal', tickCount= 4),
                   scale=alt.Scale(domain= counts, range=[20, 120], zero= True)),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain= list(cores_familia.keys()), 
                                     range=list(cores_familia.values()))),
    tooltip= alt.Tooltip(['determinator_full_name', 'ano_determinacao', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/determiner/counts_per_determiner-rearranged.html')
# g2


# <br>
# 
# ### Chart: most expressive determiners (top 50)

# In[11]:


# summing contributions of each researcher
sorting = teste1.groupby('determinator_full_name').sum()['counts'].reset_index().rename(
    columns={'counts':'sum'})

sorting = sorting.sort_values('sum', ascending=False)

# Sorted names
sort_list = sorting['determinator_full_name'].unique()

# sorting.head()


# In[12]:


# database
db = teste1[teste1['determinator_full_name'].isin(sort_list[:50])]

# aux. variables & filtering out some families (that doesn't have determiner name or year)
familias = [f for f in cores_familia.keys() if f in 
               teste1[teste1['determinator_full_name'].isin(sort_list[:50])]['familia'].unique()]
cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_determinacao')['ano_determinacao'].unique()
y_labels = sort_list[:50]
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 100))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')

# chart
g2 = alt.Chart(db, title= 'Counts per determiner (Top 50)', width=700, height=700).mark_circle().encode(
    x= alt.X('ano_determinacao', type='ordinal', title='Determination Year',
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('determinator_full_name', type='nominal', title='Determiner Name',
             scale= alt.Scale(domain= y_labels),
             sort=sort_list),
    size= alt.Size('counts', type="quantitative", title= 'Counts',
                   legend= alt.Legend(orient= 'right', direction='horizontal', tickCount= 4),
                   scale=alt.Scale(domain= counts, range=[20, 120], zero=True)),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain=familias, range=cores_temp)),
    tooltip= alt.Tooltip(['determinator_full_name', 'ano_determinacao', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/determiner/counts_per_determiner-top_50.html')
# g2


# <font color='red'>same chart, but rearranging by the first year of appearance on  database</font>

# In[14]:


# database
db = teste1[teste1['determinator_full_name'].isin(sort_list[:50])]

# aux. variables & filtering out some families (that doesn't have determiner name or year)
familias = [f for f in cores_familia.keys() if f in 
               teste1[teste1['determinator_full_name'].isin(sort_list[:50])]['familia'].unique()]
cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_determinacao')['ano_determinacao'].unique()
y_labels = db.sort_values('ano_determinacao')['determinator_full_name'].unique()
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 100))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')

# chart
g2 = alt.Chart(db, title= 'Counts per determiner (Top 50 - rearranged by first year of appearance)', width=700, height=700).mark_circle().encode(
    x= alt.X('ano_determinacao', type='ordinal', title='Determination Year',
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('determinator_full_name', type='nominal', title='Determiner Name',
             scale= alt.Scale(domain= y_labels),
             sort=sort_list),
    size= alt.Size('counts', type="quantitative", title= 'Counts',
                   legend= alt.Legend(orient= 'right', direction='horizontal', tickCount= 4),
                   scale=alt.Scale(domain= counts, range=[20, 120], zero=True)),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain=familias, range=cores_temp)),
    tooltip= alt.Tooltip(['determinator_full_name', 'ano_determinacao', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/determiner/counts_per_determiner-top_50-rearranged.html')
# g2


# **less frequent determiners**

# In[15]:


# database
db = teste1[teste1['determinator_full_name'].isin(sort_list[50:])]

# aux. variables & filtering out some families (that doesn't have determiner name or year)
familias = [f for f in cores_familia.keys() if f in 
               teste1[teste1['determinator_full_name'].isin(sort_list[:50])]['familia'].unique()]
cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_determinacao')['ano_determinacao'].unique()
y_labels = sort_list[50:]
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 1))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')

g2 = alt.Chart(db, title= 'Counts per determiner (below Top 50)', width=800, height=600).mark_circle().encode(
    x= alt.X('ano_determinacao', type='ordinal', title='Determined Year',
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('determinator_full_name', type='nominal', title='Determiner Name', 
            sort=sort_list),
    size= alt.Size('counts', type="quantitative", title= 'Counts',
                   legend= alt.Legend(orient= 'right', direction= 'horizontal', tickCount= 4),
                   scale=alt.Scale(domain= counts, range=[20, 40], zero=True)),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain=familias, range=cores_temp)),
    tooltip= alt.Tooltip(['determinator_full_name', 'ano_determinacao', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/determiner/counts_per_determiner-less_freq.html')
# g2


# <br>
# 
# ### Creating chart: counts per collector per year
# 
# <font color='red' size='5'> Collectors name is sensitive data. Do not publish it without curator's permission </font>

# In[16]:


teste = NewTable.groupby(['collector_full_name','ano_coleta']).count()['class'].reset_index().rename(columns=
                                                                                            {'class':'counts'})


# In[17]:


g1 = alt.Chart(teste, title='Counts per collector', width=800, height=2200).mark_circle().encode(
    x= alt.X('ano_coleta', type='ordinal', title='Collected Year'),
    y= alt.Y('collector_full_name', type='nominal', title='Collector Name', 
            sort=alt.EncodingSortField('counts', op="count", order='descending')),
    size= alt.Size('counts', scale=alt.Scale(range=[15, 500])),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    tooltip= alt.Tooltip(['collector_full_name', 'ano_coleta', 'counts'])
)

g1 = g1.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# g1.save('./graphs/collector/counts_per_collector.html')
# g1


# <font color='red' size='5'>mesmo gráfico, ordenando também pela ordem</font>
# 
# **OBS:** Note que
# 
# - as contagens mudam (porque estamos ordenando por um fator a mais)
# - há pontos sobrepostos (semelhante ao que tinhamos para a base crustaceas - para um mesmo ano, um mesmo pesquisador descobriu animais de ordens/familias diferentes)

# In[18]:


teste1 = NewTable.groupby(['collector_full_name','ano_coleta', 'familia']).count()['class'].reset_index().rename(columns=
                                                                                            {'class':'counts'})


# In[19]:


# database
db = teste1

# aux. variables & filtering out some families (that doesn't have colelctor name or year)
# familias = [f for f in cores_familia.keys() if f in teste1['familia'].unique()]
# cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
temp = db.groupby('collector_full_name').sum().reset_index().sort_values('counts', ascending=False)
y_labels = temp['collector_full_name'].unique()
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 50))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')


g2 = alt.Chart(teste1, title= 'Counts per collector (sorted by sum)',
               width=800, height=1200).mark_circle().encode(
    x= alt.X('ano_coleta', type='ordinal', title='Sampling Year',
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('collector_full_name', type='nominal', title='Collector Name', 
#              scale= alt.Scale(domain= y_labels),
             sort=alt.EncodingSortField('counts', op="sum", order='descending')),
    size= alt.Size('counts', type="quantitative", title= 'Counts',
                   legend= alt.Legend(orient= 'right', direction= 'horizontal', tickCount= 4),
                   scale=alt.Scale(domain= counts,range=[20, 120])),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain=list(cores_familia.keys()), 
                                     range=list(cores_familia.values()))),
    tooltip= alt.Tooltip(['collector_full_name', 'ano_coleta', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/collector/counts_per_collector-wFamilies.html')
# g2


# <br>
# 
# <font color='red'>**same chart, rearranging by the first year the collector shows up in the database**</font>

# In[20]:


# ordenando
teste1.sort_values(['ano_coleta', 'collector_full_name'], inplace=True)

# salvando ordem das entradas
sorting = list(teste1['collector_full_name'].unique())


# In[21]:


# database
db = teste1

# aux. variables & filtering out some families (that doesn't have determiner name or year)
# familias = [f for f in cores_familia.keys() if f in teste1['familia'].unique()]
# cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
y_labels = db.sort_values('ano_coleta')['collector_full_name'].unique()
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 50))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')

g2 = alt.Chart(teste1, title= 'Counts per collector (rearranged by first year of appearance)',
               width=800, height=1200).mark_circle().encode(
    x= alt.X('ano_coleta', type='ordinal', title='Sampling Year', 
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('collector_full_name', type='nominal', title='Collector Name', 
            sort=alt.EncodingSortField('ano_coleta', op="min", order='ascending')),
    size= alt.Size('counts', type="quantitative", title= 'Counts',
                   legend= alt.Legend(orient= 'right', direction= 'horizontal'),
                   scale=alt.Scale( domain= counts, range=[20, 120], zero= False)),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain= list(cores_familia.keys()), 
                                     range= list(cores_familia.values()))),
    tooltip= alt.Tooltip(['collector_full_name', 'ano_coleta', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/collector/counts_per_collector-rearranged.html')
# g2


# <br>
# 
# ### Chart: most expressive collectors (top 50)

# In[22]:


# summing contributions of each collector
sorting = teste1.groupby('collector_full_name').sum()['counts'].reset_index().rename(
    columns={'counts':'sum'})

sorting = sorting.sort_values('sum', ascending=False)

# sorted names
sort_list = sorting['collector_full_name'].unique()

# sorting.head()


# In[23]:


# database
db = teste1[teste1['collector_full_name'].isin(sort_list[:50])]

# aux. variables & filtering out some families (that doesn't have determiner name or year)
familias = [f for f in cores_familia.keys() if f in 
               teste1[teste1['collector_full_name'].isin(sort_list[:50])]['familia'].unique()]
cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
y_labels = sort_list[:50]
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 50))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')

# filtering out some families (not in TOP 50 determiners)



g2 = alt.Chart(db, title= 'Counts per collector (Top 50)',
               width=800, height=700).mark_circle().encode(
    x= alt.X('ano_coleta', type='ordinal', title='Sampling Year',
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('collector_full_name', type='nominal', title='Collector Name', 
             scale= alt.Scale(domain= y_labels),
             sort= sort_list[:50]),
    size= alt.Size('counts', type="quantitative", title= 'Counts',
                   legend= alt.Legend(orient= 'right', direction= 'horizontal'),
                   scale=alt.Scale(domain= counts, range=[20, 120])),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain=familias, range=cores_temp)),
    tooltip= alt.Tooltip(['collector_full_name', 'ano_coleta', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/collector/counts_per_collector-top_50.html')
# g2


# <font color='red'> same chart, but rearranging by the first year of appearance on the database </font>

# In[24]:


# summing contributions of each collector
sorting = teste1.groupby('collector_full_name').sum()['counts'].reset_index().rename(
    columns={'counts':'sum'})

sorting = sorting.sort_values('sum', ascending=False)

# sorted names
sort_list = sorting['collector_full_name'].unique()

# sorting.head()


# In[26]:


# database
db = teste1[teste1['collector_full_name'].isin(sort_list[:50])]

# aux. variables & filtering out some families (that doesn't have determiner name or year)
familias = [f for f in cores_familia.keys() if f in 
               teste1[teste1['collector_full_name'].isin(sort_list[:50])]['familia'].unique()]
cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
y_labels = db.sort_values('ano_coleta')['collector_full_name'].unique()
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 50))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')

# filtering out some families (not in TOP 50 determiners)



g2 = alt.Chart(db, title= 'Counts per collector (Top 50 - rearranged by first year of appearance)',
               width=800, height=700).mark_circle().encode(
    x= alt.X('ano_coleta', type='ordinal', title='Sampling Year',
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('collector_full_name', type='nominal', title='Collector Name', 
             scale= alt.Scale(domain= y_labels),
             sort= sort_list[:50]),
    size= alt.Size('counts', type="quantitative", title= 'Counts',
                   legend= alt.Legend(orient= 'right', direction= 'horizontal'),
                   scale=alt.Scale(domain= counts, range=[20, 120])),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain=familias, range=cores_temp)),
    tooltip= alt.Tooltip(['collector_full_name', 'ano_coleta', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/collector/counts_per_collector-top_50-rearranged.html')
# g2


# less expressive collectors

# In[40]:


# database
db = teste1[teste1['collector_full_name'].isin(sort_list[50:900])]

# aux. variables & filtering out some families (that doesn't have determiner name or year)
familias = [f for f in cores_familia.keys() if f in 
               teste1[teste1['collector_full_name'].isin(sort_list[50:900])]['familia'].unique()]
cores_temp = [cores_familia[f] for f in familias]
x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
y_labels = sort_list[50:900]
temp = db['counts'].unique()
counts = list(range(temp.min(), temp.max(), 10))

# selector
select_family = alt.selection_multi(fields= ['familia'], bind='legend')


g2 = alt.Chart(db, title= 'Counts per collector (below Top 50)',
               width=800, height=700).mark_circle().encode(
    x= alt.X('ano_coleta', type='ordinal', title='Sampling Year',
             scale= alt.Scale(domain= x_labels)),
    y= alt.Y('collector_full_name', type='nominal', title='Collector Name', 
#              scale= alt.Scale(domain= y_labels),
             sort= sort_list[50:900]),
#         sort= alt.EncodingSortField(field= 'counts', op='sum', order='descending')),# sorts again with sel.
    size= alt.Size('counts', type="quantitative",
                   legend= alt.Legend(orient= 'right', direction= 'horizontal'),
                   scale=alt.Scale(domain= counts, range=[20, 120])),  # range ajusta tamanho do circulo
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    color= alt.Color('familia', type="nominal", title="Family", 
                     legend= alt.Legend(columns=2, symbolLimit=50),
                     scale=alt.Scale(domain=familias, range=cores_temp)),
    tooltip= alt.Tooltip(['collector_full_name', 'ano_coleta', 'counts', 'familia'])
).add_selection(select_family).transform_filter(select_family)

g2 = g2.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving chart
# g2.save('./graphs/collector/counts_per_collector-less_freq.html')
# g2


# <br>
# 
# **The end!**
# 
# -----
