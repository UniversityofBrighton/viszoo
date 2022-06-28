#!/usr/bin/env python
# coding: utf-8

# # Data Treatment (Repteis Database)
# 
# In this notebook I'm doing all the data treatments and adjustments necessary to produce high quality visualizations. 
# 
# This notebook has an output <font color='blue'>treated_db.csv</font> with a subset of the original database properly treated.
# 
# -----
# 
# Specifically, for the `repteis` database, the file we'll read is <font color='blue'>Compilacao Livros Repteis - 2 a 10 - 2020_04_28.xls</font>
# 
# <font color='red'>**p.s.:** the idea is to transform all the code in this notebook into a `.py` file with a CLI interface to parse a file and produce a treated csv file right away. </font>
# 
# is it feasible? as we're selecting plenty different columns... maybe selecting them from a .txt file might be a good solution

# <br>
# 
# <font size='5'>**Equivalência de colunas:** Repteis e Crustaceas</font>
# 
# **Nome diferente:** <br>
# - Species1: Especie_ent ou Especie_atual
# - Species Author1: ?
# - Type Status1: Type Status 1
# - Qualifier1: Qualificador_ent Qualificador_atual
# - Determiner First Name1: DeterminatorFirstName1
# - Determiner Middle1: DeterminatorMiddleInitial1
# - Determiner Last Name1: DeterminatorLastName1
# - Determined Date1: DataDaDeterminacao

# ## Imports

# In[1]:


import datetime
import unidecode
import numpy as np
import pandas as pd

from collections import defaultdict

# quick visualizations for data analytics
import seaborn as sns
import matplotlib.pyplot as plt

# proprietary functions in ./src/MNViz.py
from src.MNViz import *


# ## Importing data

# In[2]:


# excel = pd.ExcelFile('./data/Compilacao Livros Repteis - 2 a 10 - 2020_04_28.xls')
# excel = pd.ExcelFile('./data/Compilacao Livros Repteis - 2 a 10 - 2020_04_28 _ com subordens e perdidos incendio.xls')
excel = pd.ExcelFile(
    './data/Compilacao Livros Repteis - 2 a 10 - 2020_09_27 _ com subordens e perdidos incendio e tipos.xlsx')
sheet_name = excel.sheet_names

print('The excel file contains the following sheets:', sheet_name)
print('\nDatabase is in sheet:', sheet_name[0])


# In[3]:


db = excel.parse(sheet_name[0], sep=';', encoding='utf-8-sig')
repteis = db.copy()

print(f'The database has {db.shape[0]} rows and {db.shape[1]} columns.')


# ## Adjusting column names
# 
# ### removing '\n', '\t', and other special characters

# In[4]:


repteis.columns = [str(col).replace(r'\n','') for col in repteis.columns]


# In[5]:


# for col in repteis.columns:
#     if 'collector' in col.lower():
#         print(col)


# ## Adjusting Determiners and Collectors Names

# In[6]:


names_col = ['DeterminatorLastName1', 'DeterminatorFirstName1', 'DeterminatorLastName2',
             'DeterminatorFirstName2', 'CollectorLastName1', 'CollectorFirstName1', 
             'CollectorLastName2', 'CollectorFirstName2', 'CollectorLastName3', 'CollectorFirstName3',
             'CollectorLastName4', 'CollectorFirstName4', 'CollectorLastName5', 'CollectorFirstName5',
             'CollectorLastName6', 'CollectorFirstName6']


# In[7]:


for name_col in names_col:
    if 'last' in name_col.lower():
        repteis[name_col] = repteis[name_col].apply(lambda x: treat_names(x, pos='last'))
    else:
        repteis[name_col] = repteis[name_col].apply(treat_names)


# ### creating column joining First and Last names
# 
# I'm doing this only for the first collectors and determiners

# In[8]:


repteis['DeterminatorFirst_and_LastName'] = repteis['DeterminatorFirstName1'].str.strip() + ' ' + repteis['DeterminatorLastName1'].str.strip()

repteis['CollectorFirst_and_LastName'] = repteis['CollectorFirstName1'].str.strip() + ' ' + repteis['CollectorLastName1'].str.strip()


# Doing the same thing for the other columns (2,3,4,5 and 6)

# In[9]:


for i in range(2, 7):    
    if i < 3:
        # determinator 
        repteis[f'DeterminatorFirst_and_LastName{i}'] = repteis[f'DeterminatorFirstName{i}'].astype(str).str.strip() + ' ' + repteis[f'DeterminatorLastName{i}'].astype(str).str.strip()
    
    # collector
    repteis[f'CollectorFirst_and_LastName{i}'] = repteis[f'CollectorFirstName{i}'].str.strip() + ' ' + repteis[f'CollectorLastName{i}'].str.strip()


# In[10]:


# p.s.: Second Determinator's column is all empty!
repteis['DeterminatorFirst_and_LastName2'].unique()


# In[11]:


# repteis['CollectorFirst_and_LastName6'].unique()


# ## Author names...

# In[12]:


repteis['author_full'] = repteis['Autor']


# In[13]:


repteis['first_author'] = repteis['Autor'].apply(lambda x: str(x).split(',')[0])


# ## Treating taxon columns

# In[14]:


# adicionei Subordem para a nova base (remover se for tratar a base antiga)
taxon_columns = ['Kingdom', 'Phylum', 'Class', 'Ordem', 'Subordem', 'Familia', 'Genero_ent',
                 'Genero_atual', 'Especie_ent', 'Especie_atual', 'Subespecie_ent',
                 'Subespecie_atual']  # selecting taxonomy columns

treat_taxon_columns(repteis, taxon_columns)


# ## Adjusting Gender and Species

# In[15]:


# dica da Manoela: epiteto especifico deve ser todo minusculo (especie e subespecie, nesse caso)
repteis['Especie_atual'] = repteis['Especie_atual'].str.lower()
repteis['Subespecie_atual'] = repteis['Subespecie_atual'].str.lower()


# <br>
# 
# ## adding `Genero` and `Especie`together (they completely identify each animal's species)

# In[16]:


repteis['genero_e_especie_ent'] = repteis['Genero_ent'] + ' ' + repteis['Especie_ent']
repteis['genero_e_especie_atual'] = repteis['Genero_atual'] + ' ' + repteis['Especie_atual']

repteis['genero_e_especie_ent'] = repteis['genero_e_especie_ent'].str.lower().str.capitalize()
repteis['genero_e_especie_atual'] = repteis['genero_e_especie_atual'].str.lower().str.capitalize()


# ## Catching Month and Year

# date_columns= ['DataDeEntrada','DataDaDeterminacao','DataColetaInicial'] 

# <font color='red' size='4'>Falta tratar a coluna `Ano descrição`</font>

# In[17]:


repteis['ano_determinacao'] = repteis['DataDaDeterminacao'].apply(lambda x: getMonthAndYear(x)[-1])
repteis['ano_coleta'] = repteis['DataColetaInicial'].apply(lambda x: getMonthAndYear(x)[-1])
repteis['ano_entrada'] = repteis['DataDeEntrada'].apply(lambda x: getMonthAndYear(x)[-1])

repteis['mes_determinacao'] = repteis['DataDaDeterminacao'].apply(lambda x: getMonthAndYear(x)[0])
repteis['mes_coleta'] = repteis['DataColetaInicial'].apply(lambda x: getMonthAndYear(x)[0])
repteis['mes_entrada'] = repteis['DataDeEntrada'].apply(lambda x: getMonthAndYear(x)[0])


# converting to int

# In[18]:


repteis['ano_determinacao'] = repteis['ano_determinacao'].apply(str_with_nan2int) #has NaN
repteis['ano_coleta'] = repteis['ano_coleta'].apply(str_with_nan2int) #has NaN
repteis['ano_entrada'] = repteis['ano_entrada'].apply(str_with_nan2int) #has NaN

repteis['mes_determinacao'] = repteis['mes_determinacao'].apply(str_with_nan2int) #has NaN
repteis['mes_coleta'] = repteis['mes_coleta'].apply(str_with_nan2int) #has NaN
repteis['mes_entrada'] = repteis['mes_entrada'].apply(str_with_nan2int) #has NaN


# <br>
# 
# ## Adjusting `Altitude` column
# 
# <font color='red'>**p.s.:** I'm assuming it's all on the same measure unit (in meters) </font>

# In[19]:


repteis['altitude'] = repteis['MinAltitude'].str.extract('(\d+)')
repteis['max_altitude'] = repteis['MaxAltitude'].str.extract('(\d+)')


# <br>
# 
# ## Adjusting Latitude and Longitude

# In[21]:


for col in repteis.columns:
    if 'long' in col.lower():
        print(col)


# In[20]:


repteis['Lat'] = repteis['Lat'].apply(convert2float)
repteis['Long'] = repteis['Long'].apply(convert2float)


# <br>
# 
# ## Creating column with brazilian regions

# In[21]:


repteis['regiao'] = repteis['EstadoOuProvincia'].apply(brazilian_region)


# <br>
# 
# ## Adjusting Types (`NotasTaxonomicas`)

# In[22]:


def define_type(t):
    t = str(t).strip().lower().capitalize()
    
    if t == 'Nan':
        return np.NAN
    else:
        return t


# In[23]:


repteis['type_status'] = repteis['NotasTaxonomicas'].apply(define_type)


# <br>
# 
# ## Adjusting `Ordem` column

# In[24]:


repteis['Ordem'] = repteis['Ordem'].apply(correct_squamata)
repteis['Ordem'] = repteis['Ordem'].apply(correct_nd)


# <br>
# 
# ## Specimens lost in the fire
# 
# <font color='red'>**works only in the new database** </font>

# In[25]:


def lost_in_fire(description):
    '''
    Returns 1 if that specimen was lost in the fire, 0 otherwise.
    '''
    description = str(description)
    
    # removing accents
    description = unidecode.unidecode(description)
    
    if 'perdido no incendio' in description:
        return 1
    else:
        return 0


# In[26]:


repteis['lost_in_fire'] = repteis['CollectionObjectRemarks'].apply(lost_in_fire)


# In[27]:


# checagem
# repteis[repteis['lost_in_fire'] == 1]['CollectionObjectRemarks'].unique()


# <br>
# 
# ## Selecting Subset of Main DB

# In[31]:


# 'genero_e_especie_ent', 'genero_e_especie_atual'
selected_columns = ['NumeroDeCatalogo','DataDeEntrada','DataDaDeterminacao','DataColetaInicial',
                    'ano_entrada', 'mes_entrada', 'ano_determinacao', 'mes_determinacao',
                    'ano_coleta', 'mes_coleta',
                    'Class','Kingdom', 
                    'Genero_ent', 'Genero_atual', 'Especie_ent', 'Especie_atual','Subespecie_atual','type_status',
                    'DeterminatorFirstName1', 'DeterminatorLastName1','DeterminatorFirst_and_LastName',
                    'DeterminatorFirst_and_LastName2',
                    'CollectorFirst_and_LastName', 'CollectorFirst_and_LastName2',
                    'CollectorFirst_and_LastName3', 'CollectorFirst_and_LastName4',
                    'CollectorFirst_and_LastName5', 'CollectorFirst_and_LastName6',
                    'altitude', 'max_altitude',
                    'Ordem','Subordem',  'Familia', 'Phylum', 'Qualificador_atual', 'NotasTaxonomicas',
                    'Lat', 'Long', 'Municipio', 
                    'EstadoOuProvincia', 'Pais', 'Continente', 'regiao', 'lost_in_fire',
                    'Ano descrição', 'author_full', 'first_author']


# In[32]:


NewTable = repteis[selected_columns].copy()


# ## Renaming columns
# 
# Setting new standardized column names to facilitate future steps.

# In[33]:


renames = {
    'NumeroDeCatalogo':'numero_catalogo',
    'DataDeEntrada':'data_entrada',
    'DataDaDeterminacao':'data_determinacao',
    'DataColetainicial':'data_coleta',
    'Class':'class',
    'Kingdom':'kingdom',
    'Genero_ent':'genero_ent',
    'Genero_atual':'genero_atual',
    'Especie_ent':'especie_ent',
    'Especie_atual':'especie_atual',
    'Subespecie_atual':'subespecie_atual',
    'Type Status 1':'type',
    'Ordem':'ordem',
    'Subordem':'subordem',
    'Familia':'familia',
    'Phylum':'phylum',
    'Qualificador_atual':'qualificador_atual',
    'NotasTaxonomicas':'notas_taxonomicas',
    'Lat':'lat',
    'Long':'long', 
    'Municipio':'municipio', 
    'EstadoOuProvincia':'estado_ou_provincia',
    'Pais':'pais', 
    'Continente':'continente',
    'DeterminatorFirst_and_LastName':'determinator_full_name',
    'DeterminatorFirst_and_LastName2':'determinator_full_name2',
    'CollectorFirst_and_LastName':'collector_full_name',
    'CollectorFirst_and_LastName2':'collector_full_name2',
    'CollectorFirst_and_LastName3':'collector_full_name3',
    'CollectorFirst_and_LastName4':'collector_full_name4',
    'CollectorFirst_and_LastName5':'collector_full_name5',
    'CollectorFirst_and_LastName6':'collector_full_name6',
    'Ano descrição':'ano_descricao'
}


# In[34]:


NewTable = NewTable.rename(columns=renames)


# <br>
# 
# ## Exporting to `CSV`
# 
# name: <font color='blue'>./src/treated_db.csv</font>
# sep: ';'
# encoding: 'utf-8-sig'

# In[35]:


NewTable.to_csv('./data/treated_db.csv', sep=';', encoding='utf-8-sig')

