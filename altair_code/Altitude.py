import datetime
import numpy as np
import pandas as pd

from collections import defaultdict

import altair as alt


from src.MNViz_colors import *

from itertools import compress

def familyX_altitudeY(NewTable):

  alt.data_transformers.disable_max_rows()

  # subsetting
  teste = NewTable[['altitude','familia','ordem','subordem', 'ano_coleta', 'qualificador_atual', 'numero_catalogo', 
                    'genero_atual', 'especie_atual', 'subespecie_atual']].copy()

  # sorting
  teste = teste.sort_values(['altitude','familia'])

  # dropping na
  teste.dropna(subset=['altitude'], inplace=True)

  # making sure altitude is a floating point number
  teste['altitude'] = teste['altitude'].astype(float)

  # removing outlier
  teste = teste[teste['altitude'] < 7000].copy()

  # database
  db = teste[teste['familia'] != "#n/d"]

  # aux. variables
  ordens = list(cores_ordem.keys())
  cores = list(cores_ordem.values())

  #color_pal = alt.condition(alt.FieldOneOfPredicate("familia",new_fam), alt.Color('familia:N', title= 'Family', legend = None, scale=alt.Scale(domain= list(cores_familia.keys()), range= list(cores_familia.values()))), alt.value('lightgray'))

  temp = alt.Chart(db, title='Altitude per Family').mark_circle().encode(
      x = alt.X('familia', type='nominal', title='Family', 
                sort= alt.EncodingSortField('altitude', op='mean', order='ascending')),
      y = alt.Y('altitude', type='quantitative', title='Altitude (in meters)'),
      color= alt.Color('familia:N', title= 'Family', 
                    legend = None,
                    scale=alt.Scale(domain= list(cores_familia.keys()), 
                                    range= list(cores_familia.values()))),
      tooltip = [alt.Tooltip('numero_catalogo', title='number in catalogue'),
              alt.Tooltip('genero_atual', title='Genus'),
              alt.Tooltip('especie_atual', title='Species'),
              alt.Tooltip('subespecie_atual', title='Subspecies'),
              alt.Tooltip('qualificador_atual', title='qualifier'),
              alt.Tooltip('ano_coleta', title='year collected'),
              alt.Tooltip('altitude', title='altitude')],

  )

  return temp


def genusX_altitudeY(data):

  data = data[['altitude','especie_atual','genero_atual','ordem', 'subordem',
                 'familia', 'ano_coleta', 'qualificador_atual', 'numero_catalogo', 'subespecie_atual']]

  # dropping na
  data = data.dropna(subset=['altitude'])
  # making sure altitude is a floating point number
  data['altitude'] = data['altitude'].astype(float)
  # removing outlier
  data = data[data['altitude'] < 7000].copy()

  # ordering x-axis per mean altitude - OUTLIER: ordem nula
  graph = alt.Chart(data, title='Altitude per Genus',
                  width= 900, height=300).mark_circle().encode(
      x = alt.X('genero_atual', type='nominal', title='Genus',
              sort=alt.EncodingSortField('altitude', op="mean", order="ascending")),
      y = alt.Y('altitude:Q', title='Altitude (in meters)'),
      color = alt.Color('familia:N', title='Family',
                      legend=None,
                      scale= alt.Scale(domain=list(cores_familia.keys()), range= list(cores_familia.values()))),
      tooltip = alt.Tooltip(['numero_catalogo', 'genero_atual','especie_atual','subespecie_atual', 
                          'ordem', 'subordem',
                              'qualificador_atual', 'ano_coleta','altitude'])
  )

  graph = graph.configure_title(fontSize=16).configure_axis(
      labelFontSize=12,
      titleFontSize=12
  ).configure_legend(
      labelFontSize=12,
      titleFontSize=12
  )

  # g.save('./graphs/altitude/genus/altitude-per-genus.html')
  # g
  return graph

