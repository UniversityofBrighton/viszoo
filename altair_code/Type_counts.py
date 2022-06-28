#!/usr/bin/env python
# coding: utf-8

# # Type charts
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


# In[5]:


# parsing columns into string so we don't lose information while grouping
NewTable['type_status'] = NewTable['type_status'].astype(str)
NewTable['first_author'] = NewTable['first_author'].astype(str)


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

# In[6]:


# importing customized color palettes
from src.MNViz_colors import *


# In[7]:


# p.s.: caudata is an error and should be removed. 
# cores_ordem = {
#     'Squamata': '#BF4417',
#     'Testudines': '#D9CB0B', 
#     'Crocodylia': '#284021'
# }

ordens = list(cores_ordem.keys())
cores = list(cores_ordem.values())


# small comment on the rationale behind the color palette (to see this, uncoment the content in this cell)
# <!-- **Paleta de Cores - Família:**
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
# **TOTAL: 50 cores** -->

# <br>
# 
# 
# ## Graphs
# 
# ---
# 
# ### Types (*per year*) per genus
# 
# x: Species1, cor: Type Status1, size: counts

# In[8]:


# type info is in this column
NewTable['type_status'].value_counts(dropna= False)


# In[9]:


# subsetting
teste = NewTable[['altitude','familia','ordem', 'ano_descricao', 'qualificador_atual', 'numero_catalogo', 
                  'genero_atual', 'especie_atual', 'subespecie_atual', 'type_status']].copy()

# grouping by type, year and order
temp = teste.groupby(['type_status','ano_descricao', 'ordem']).count()['familia'].reset_index().rename(columns={
    'familia':'counts'
})

# p.s.: Cótipo and Topótipo are not types
temp = temp[(temp['type_status'] != 'Cótipo') & (temp['type_status'] != 'Topótipo')]


# 243 info. de tipos

# ### Chart: Types per year
# 
# with color palette per order

# In[13]:


tipo = alt.Chart(temp, height=150, title='Types per year').mark_circle().encode(
    x = alt.X('ano_descricao:O', title='description year'),
    y = alt.Y('type_status:N', title= 'type',
              sort=alt.EncodingSortField('tipo', op='count', order='descending')),
    color= alt.Color('ordem', scale=alt.Scale(domain=ordens, range=cores), title='order'), 
    size= alt.Size('counts', scale=alt.Scale(range=[10,600])),
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    tooltip= [alt.Tooltip('type_status', title='type'),
              alt.Tooltip('ano_descricao', title='description year'),
              alt.Tooltip('counts', title='counts')]
)

tipo = tipo.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# tipo.save('./graphs/type/types_per_year.html')
# tipo


# <br>
# 
# ### Chart: types per year 
# 
# color palette per family

# In[36]:


# subsetting
teste = NewTable[['altitude','familia','ordem', 'ano_descricao', 'qualificador_atual', 'numero_catalogo', 
                  'genero_atual', 'especie_atual', 'subespecie_atual', 'type_status']].copy()

# grouping by type, year and order
temp = teste.groupby(['type_status','ano_descricao', 'familia']).count()['ordem'].reset_index().rename(columns={
    'ordem':'counts'
})

# p.s.: Cótipo and Topótipo are not types
temp = temp[(temp['type_status'] != 'Cótipo') & (temp['type_status'] != 'Topótipo')]


# In[66]:


# database
db = temp

# aux. variables
# families = [f for f in cores_familia.keys() if f in db['familia'].unique()]
# cores_temp = [cores_familia[f] for f in families]
x_labels = db.sort_values('ano_descricao')['ano_descricao'].unique()
# y labels sorted by sum
y_labels = db.groupby('type_status').sum().reset_index().sort_values('counts')['type_status'].unique()[::-1]
counts = db['counts'].unique()
counts = list(range(counts.min(), counts.max(), 20))

# selector
select_family = alt.selection_multi(fields=['familia'], bind='legend')

tipo = alt.Chart(db, height=200,width=500, title='Types per year').mark_circle().encode(
    x = alt.X('ano_descricao:O', title='Description Year', 
              scale= alt.Scale(domain= x_labels)),
    y = alt.Y('type_status:N', title= 'Type',
              scale= alt.Scale(domain= y_labels),
              sort=alt.EncodingSortField('counts', op='sum', order='descending')),
    color= alt.Color('familia:N', title='Family', 
                     scale=alt.Scale(domain= list(cores_familia.keys()), 
                                     range=list(cores_familia.values())),
                    legend= alt.Legend(columns=3, symbolLimit=50, direction='vertical')), 
    size= alt.Size('counts', title='Counts', 
                   legend= alt.Legend(orient= 'right', direction= 'horizontal'),
                   scale=alt.Scale(domain= counts, range=[20,120])),
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    tooltip= [alt.Tooltip('familia', title='Family'),
              alt.Tooltip('type_status', title='Type'),
              alt.Tooltip('ano_descricao', title='Description Year'),
              alt.Tooltip('counts', title='Counts')]
).add_selection(select_family).transform_filter(select_family)

tipo = tipo.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# tipo.save('./graphs/type/types_per_year-wFamilies.html')
# tipo


# <br>
# 
# #### defining some parameters
# 
# **colors:**
# <ul>
#     <li style='color:#d62728;'><b> #d62728 </b> - red1 1</li>
#     <li style='color:#d62729;'><b> #d62729 </b> - red2 2</li>
#     <li style='color:#f58518;'><b> #f58518 </b> - orange 1</li>
#     <li style='color:#f58519;'><b> #f58519 </b> - orange2 2</li>
#     <li style='color:#d95f02;'><b> #d95f02 </b> - dark orange</li>
#     <li style='color:#4daf4a;'><b> #4daf4a </b> - green</li>
#     <li style='color:#8c6d31;'><b> #8c6d31 </b> - brown</li>
#     <li style='color:#79706e;'><b> #79706e </b> - blue</li>
#     <li style='color:#bab0ac;'><b> #bab0ac </b> - light blue</li>
#     <li style='color:#d8b5a5;'><b> #d8b5a5 </b> - beige</li>
#     <li style='color:#000000;'><b> #000000 </b> - black</li>
# </ul>

# In[67]:


NewTable['type_status'] = NewTable['type_status'].apply(lambda x:str(x))
types = NewTable['type_status'].apply(lambda x:str(x)).unique()


# In[74]:


# dictionary with type:color
type_color = {
#     'nan':'#000000',      # preto
    'Holótipo':'#d62728',  # vermelho 1
    'Síntipo':'#d62729',   # vermelho 2
    'Parátipo':'#4daf4a',  # verde
    'Topótipo':'#8c6d31',  # marrom
    'Lectótipo':'#f58518', # laranja 1
    '2005':'#79706e',      # azul  OBS: ERRO NA BASE!
}


# <br>
# 
# ## Chart: Sampling Year x Description Year for types

# In[77]:


# database
db = NewTable[NewTable['type_status'] != 'nan']

g1 = alt.Chart(db, title= 'Sampling year vs. Description year',width=500, height=500).mark_circle().encode(
    x = alt.X('ano_descricao:O', title='Description Year'),
    y = alt.Y('ano_coleta:O', title='Sampling Year', 
             sort= alt.EncodingSortField('ano_coleta', op='min', order='descending')),
    color = alt.Color('type_status:N', title='Type', 
                     scale= alt.Scale(domain= list(type_color.keys()), range= list(type_color.values()))),
    tooltip = alt.Tooltip(['numero_catalogo', 'familia', 'ordem', 'type_status', 
                           'ano_coleta', 'ano_descricao'])
)

g1 = g1.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# g1.save('./graphs/type/sampling_year-vs-description_year.html')
# g1


# ## Chart: types and non-types per author
# 
# <br>
# 
# ### grouping and counting

# In[93]:


temp = NewTable.groupby(['first_author', 'type_status', 'ano_descricao']).count()['class'].reset_index()
temp.rename(columns={'class':'counts'}, inplace=True)


# In[95]:


# database  (filtering out non-types)
db = temp[temp['type_status'] != 'nan']

# aux. variables
# families = [f for f in cores_familia.keys() if f in db['familia'].unique()]
# cores_temp = [cores_familia[f] for f in families]
x_labels = db.sort_values('ano_descricao')['ano_descricao'].unique()
y_labels = db.groupby('first_author').sum().reset_index().sort_values('counts')['first_author'].unique()[::-1]
counts = db['counts'].unique()
counts = list(range(counts.min(), counts.max(), 20))

# selector
select_type = alt.selection_multi(fields=['type_status'], bind= 'legend')

g1 = alt.Chart(db, title='Types per Author', 
               height=300, width=400).mark_circle().encode(
    x = alt.X('ano_descricao:O', title='Description Year', 
              scale= alt.Scale(domain= x_labels)),
    y = alt.Y('first_author:N', title='Author', 
              scale= alt.Scale(domain= y_labels)),  # AJUSTAR DEPOIS
#              sort= sort_determiners),
    color = alt.Color('type_status:N', title='Type', 
                     scale = alt.Scale(domain=list(type_color.keys()), range= list(type_color.values()))), 
    size = alt.Size('counts:Q', title= 'Counts',
                    scale= alt.Scale(domain= counts, range=[20,60])), 
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    tooltip = alt.Tooltip(['first_author', 'type_status', 'ano_descricao', 'counts'])
).add_selection(select_type).transform_filter(select_type)

g1 = g1.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving graph
# g1.save('./graphs/type/types_per_author.html')
# g1


# <br>
# 
# ## types per collector
# 
# -----
# 
# ### grouping and counting

# In[120]:


counts = NewTable.groupby(['collector_full_name', 'type_status', 'ano_coleta']).count()['class'].reset_index()
counts.rename(columns={'class':'counts'}, inplace=True)
counts.sort_values('counts', inplace=True, ascending=False)


# In[121]:


sort_determiners = list(counts[counts['type_status'] != 'nan'].groupby(['collector_full_name']).min()['ano_coleta'].reset_index(
).sort_values('ano_coleta')['collector_full_name'])


# In[134]:


# database
db = counts[counts['type_status'] != 'nan']

# aux. variables
x_labels = db.sort_values('ano_coleta')['ano_coleta'].unique()
y_labels = db.sort_values('ano_coleta')['collector_full_name'].unique()
ct = db['counts'].unique()
ct = list(range(ct.min(), ct.max(), 10))

# selector
select_type = alt.selection_multi(fields= ['type_status'], bind='legend')

g1 = alt.Chart(db, title='Types per collector', 
               height=700, width=400).mark_circle().encode(
    x = alt.X('ano_coleta:O', title='Sampling Year', 
              scale= alt.Scale(domain= x_labels)),
    y = alt.Y('collector_full_name:N', title='Collector', 
             sort= sort_determiners, 
             scale= alt.Scale(domain= y_labels)),
    color = alt.Color('type_status:N', title='Type', 
                     scale = alt.Scale(domain=list(type_color.keys()), range= list(type_color.values()))), 
    size = alt.Size('counts:Q', title= 'Counts', 
                    legend= alt.Legend(orient= 'right', direction='horizontal', tickCount=4),
                    scale= alt.Scale(domain= ct, range= [20, 60], zero=True)), 
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    tooltip = alt.Tooltip(['collector_full_name', 'type_status', 'ano_coleta', 'counts'])
).add_selection(select_type).transform_filter(select_type)

g1 = g1.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# saving graph
# g1.save('./graphs/type/types_per_collector.html')
# g1


# <br>
# 
# ## Types per family

# In[137]:


# grouping by type, year and order
temp = NewTable.groupby(['type_status','ano_descricao', 'familia', 'ordem']).count()['class'].reset_index().rename(columns={
    'class':'counts'
})

temp = temp[temp['type_status'] != 'nan'].copy()


# In[158]:


# database
db = temp

# aux. variables
families = [f for f in cores_familia.keys() if f in db['familia'].unique()]
cores_temp = [cores_familia[f] for f in families]
x_labels = db.sort_values('ano_descricao')['ano_descricao'].unique()
y_labels = db.groupby('familia').sum().reset_index().sort_values('counts')['familia'].unique()[::-1]
ct = db['counts'].unique()
ct = list(range(ct.min(), ct.max(), 20))
tp = db['type_status'].unique()

# selectors
select_family = alt.selection_multi(fields= ['familia'], bind='legend')
select_type = alt.selection_multi(fields= ['type_status'], bind='legend')

tipo = alt.Chart(db, height=400, width=400, title='Types per Family').mark_point(filled=False).encode(
    x = alt.X('ano_descricao:O', title='Description Year', 
              scale= alt.Scale(domain= x_labels)),
    y = alt.Y('familia:N', title= 'Family', 
              scale= alt.Scale(domain= y_labels)), 
#               sort= family_order),
    color= alt.Color('familia:N', title='Family',
                     legend= alt.Legend(columns=2, symbolLimit= 50),
                    scale= alt.Scale(domain= families, 
                                     range= cores_temp)), 
    size= alt.Size('counts', title='Counts',
                   legend= alt.Legend(orient= 'right', direction= 'horizontal'),
                   scale=alt.Scale(domain= ct, range=[20,120])),
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    shape= alt.Shape('type_status:N', title='Type', 
                     legend= alt.Legend(columns=3),
                     scale= alt.Scale(domain= tp)), 
    tooltip= [alt.Tooltip('familia', title='family'),
              alt.Tooltip('type_status', title='type'),
              alt.Tooltip('ano_descricao', title='description year'),
              alt.Tooltip('counts', title='counts')]
).add_selection(select_family, select_type).transform_filter(select_family).transform_filter(select_type)

tipo = tipo.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# tipo.save('./graphs/type/types_per_family.html')
# tipo


# <br>
# 
# ## Types per Genus 
# 
# same graph as above, with gender on Y axis and colored by type

# In[160]:


# grouping by type, year and order
temp = NewTable.groupby(['type_status','ano_descricao', 'genero_atual', 'familia']).count()['class'].reset_index().rename(columns={
    'class':'counts'
})

# p.s.: Cótipo and Topótipo are not types
temp = temp[(temp['type_status'] != 'nan')]


# In[161]:


# AJUSTAR DEPOIS: preciso que a coluna ano_descricao esteja limpa para conseguir odenar!
# genus_order = list(temp.groupby(['genero_atual']).min()['ano_coleta'].reset_index().sort_values('ano_coleta')['genero_atual'])


# In[185]:


# database
db = temp

# aux. variables
families = [f for f in cores_familia.keys() if f in db['familia'].unique()]
cores_temp = [cores_familia[f] for f in families]
x_labels = db.sort_values('ano_descricao')['ano_descricao'].unique()
y_labels = db.groupby('genero_atual').sum().reset_index().sort_values('counts')['genero_atual'].unique()[::-1]
ct = db['counts'].unique()
ct = list(range(ct.min(), ct.max(), 20))
tp = db['type_status'].unique()

# selectors
select_family = alt.selection_multi(fields= ['familia'], bind='legend')
select_type = alt.selection_multi(fields= ['type_status'], bind='legend')

tipo = alt.Chart(temp, height=400, width= 400, title='Types per Genus').mark_point(filled=False).encode(
    x = alt.X('ano_descricao:O', title='Description Year',
              scale= alt.Scale(domain= x_labels)),
    y = alt.Y('genero_atual:N', title= 'Genus',
              scale= alt.Scale(domain= y_labels)),
#               sort=genus_order),
    color= alt.Color('familia:N', title='Family',
                     legend= alt.Legend(columns=2, symbolLimit=50),
                    scale= alt.Scale(domain=families, range= cores_temp)), 
    size= alt.Size('counts', title='Counts',
                   legend= alt.Legend(orient= 'right', direction= 'horizontal'),
                   scale=alt.Scale(domain= ct, range=[20,120])),
    order= alt.Order('counts', sort='descending'),  # smaller points in front
    shape= alt.Shape('type_status:N', title='Type',
                    legend= alt.Legend(columns=3),
                    scale= alt.Scale(domain= tp)), 
    tooltip= [alt.Tooltip('familia', title='family'),
              alt.Tooltip('type_status', title='type'),
              alt.Tooltip('ano_descricao', title='description year'),
              alt.Tooltip('counts', title='counts')]
).add_selection(select_family, select_type).transform_filter(select_family).transform_filter(select_type)

tipo = tipo.configure_title(fontSize=16).configure_axis(
    labelFontSize=12,
    titleFontSize=12
).configure_legend(
    labelFontSize=12,
    titleFontSize=12
)

# tipo.save('./graphs/type/types_per_genus.html')
# tipo


# <br>
# 
# **The end!**
# 
# -----
