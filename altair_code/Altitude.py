import datetime
import numpy as np
import pandas as pd

from collections import defaultdict

import altair as alt


from src.MNViz_colors import *

from itertools import compress

def altitude_alt(NewTable):

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

  temp = alt.Chart(db, title='Altitude per family').mark_circle().encode(
      x = alt.X('familia', type='nominal', title='Family', 
                sort= alt.EncodingSortField('altitude', op='max', order='ascending')),
      y = alt.Y('altitude', type='quantitative', title='Altitude (in meters)'),
      color= alt.Color('familia:N', title= 'Family', 
                    legend = None,
                    scale=alt.Scale(domain= list(cores_familia.keys()), 
                                    range= list(cores_familia.values()))),
      tooltip = alt.Tooltip(['numero_catalogo', 'genero_atual','especie_atual','subespecie_atual', 
                              'qualificador_atual', 'ano_coleta','altitude'])
  ).interactive()

  return temp

