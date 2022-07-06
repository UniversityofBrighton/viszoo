import unidecode
import numpy as np
import pandas as pd

# proprietary functions in ./src/MNViz.py
from src.MNViz import *

def define_type(t):
    t = str(t).strip().lower().capitalize()

    if t == 'Nan' or t=='Null':
        return np.NAN
    else:
        return t


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

def excel_to_dataframe(file):
    # excel = pd.ExcelFile('./data/Compilacao Livros Repteis - 2 a 10 - 2020_04_28.xls')
    # excel = pd.ExcelFile('./data/Compilacao Livros Repteis - 2 a 10 - 2020_04_28 _ com subordens e perdidos incendio.xls')
    # './data/Compilacao Livros Repteis - 2 a 10 - 2020_09_27 _ com subordens e perdidos incendio e tipos.xlsx'
    excel = pd.ExcelFile(file)
    sheet_name = excel.sheet_names

    db = excel.parse(sheet_name[0], sep=';', encoding='utf-8-sig')
    repteis = db.copy()


    repteis.columns = [str(col).replace(r'\n','') for col in repteis.columns]


    names_col = ['DeterminatorLastName1', 'DeterminatorFirstName1', 'DeterminatorLastName2',
                'DeterminatorFirstName2', 'CollectorLastName1', 'CollectorFirstName1', 
                'CollectorLastName2', 'CollectorFirstName2', 'CollectorLastName3', 'CollectorFirstName3',
                'CollectorLastName4', 'CollectorFirstName4', 'CollectorLastName5', 'CollectorFirstName5',
                'CollectorLastName6', 'CollectorFirstName6']


    for name_col in names_col:
        if 'last' in name_col.lower():
            repteis[name_col] = repteis[name_col].apply(lambda x: treat_names(x, pos='last'))
        else:
            repteis[name_col] = repteis[name_col].apply(treat_names)



    repteis['DeterminatorFirst_and_LastName'] = repteis['DeterminatorFirstName1'].str.strip() + ' ' + repteis['DeterminatorLastName1'].str.strip()

    repteis['CollectorFirst_and_LastName'] = repteis['CollectorFirstName1'].str.strip() + ' ' + repteis['CollectorLastName1'].str.strip()



    for i in range(2, 7):    
        if i < 3:
            # determinator 
            repteis[f'DeterminatorFirst_and_LastName{i}'] = repteis[f'DeterminatorFirstName{i}'].astype(str).str.strip() + ' ' + repteis[f'DeterminatorLastName{i}'].astype(str).str.strip()
        
        # collector
        repteis[f'CollectorFirst_and_LastName{i}'] = repteis[f'CollectorFirstName{i}'].str.strip() + ' ' + repteis[f'CollectorLastName{i}'].str.strip()


    # In[10]:



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


    repteis['Ano descrição'] = repteis['DataDaDeterminacao'].apply(lambda x: getMonthAndYear(x)[-1])
    repteis['ano_coleta'] = repteis['DataColetaInicial'].apply(lambda x: getMonthAndYear(x)[-1])
    repteis['ano_entrada'] = repteis['DataDeEntrada'].apply(lambda x: getMonthAndYear(x)[-1])


    repteis['mes_determinacao'] = repteis['DataDaDeterminacao'].apply(lambda x: getMonthAndYear(x)[0])
    repteis['mes_coleta'] = repteis['DataColetaInicial'].apply(lambda x: getMonthAndYear(x)[0])
    repteis['mes_entrada'] = repteis['DataDeEntrada'].apply(lambda x: getMonthAndYear(x)[0])


    # converting to int

    # In[18]:


    repteis['Ano descrição'] = repteis['Ano descrição'].apply(str_with_nan2int) #has NaN
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



    for col in repteis.columns:
        if 'long' in col.lower():
            print(col)



    repteis['Lat'] = repteis['Lat'].apply(convert2float)
    repteis['Long'] = repteis['Long'].apply(convert2float)


    repteis['regiao'] = repteis['EstadoOuProvincia'].apply(brazilian_region)


    repteis['type_status'] = repteis['NotasTaxonomicas'].apply(define_type)



    repteis['Ordem'] = repteis['Ordem'].apply(correct_squamata)
    repteis['Ordem'] = repteis['Ordem'].apply(correct_nd)

    repteis['lost_in_fire'] = repteis['CollectionObjectRemarks'].apply(lost_in_fire)

    # 'genero_e_especie_ent', 'genero_e_especie_atual'
    selected_columns = ['NumeroDeCatalogo','DataDeEntrada','DataDaDeterminacao','DataColetaInicial',
                        'ano_entrada', 'mes_entrada', 'mes_determinacao',
                        'ano_coleta', 'mes_coleta',
                        'Class','Kingdom', 
                        'Genero_ent', 'Genero_atual', 'Especie_ent', 'Especie_atual','Subespecie_atual','type_status',
                        'DeterminatorFirstName1', 'DeterminatorLastName1','DeterminatorFirst_and_LastName',
                        'DeterminatorFirst_and_LastName2',
                        'CollectorFirst_and_LastName', 'CollectorFirst_and_LastName2',
                        'CollectorFirst_and_LastName3', 'CollectorFirst_and_LastName4',
                        'CollectorFirst_and_LastName5', 'CollectorFirst_and_LastName6',
                        'altitude', 'max_altitude',
                        'Ordem','Subordem',  'Familia', 'Phylum', 'Qualificador_atual',
                        'Lat', 'Long', 'Municipio', 
                        'EstadoOuProvincia', 'Pais', 'Continente', 'regiao', 'lost_in_fire',
                        'Ano descrição', 'author_full', 'first_author']


    NewTable = repteis[selected_columns].copy()


    renames = {
        'NumeroDeCatalogo':'numero_catalogo',
        'DataDeEntrada':'data_entrada',
        'DataDaDeterminacao':'data_determinacao',
        'DataColetaInicial':'data_coleta',
        'Class':'class',
        'Kingdom':'kingdom',
        'Genero_ent':'genero_ent',
        'Genero_atual':'genero_atual',
        'Especie_ent':'especie_ent',
        'Especie_atual':'especie_atual',
        'Subespecie_atual':'subespecie_atual',
        'Ordem':'ordem',
        'Subordem':'subordem',
        'Familia':'familia',
        'Phylum':'phylum',
        'Qualificador_atual':'qualificador_atual',
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

    dtypes = {
        'data_entrada':str,
        'data_determinacao':str,
        'data_coleta':str,
        'class':str,
        'kingdom':str,
        'genero_ent':str,
        'genero_atual':str,
        'especie_ent':str,
        'especie_atual':str,
        'subespecie_atual':str,
        'ordem':str,
        'subordem':str,
        'familia':str,
        'phylum':str,
        'qualificador_atual':str,
        'notas_taxonomicas':str,
        'municipio':str, 
        'estado_ou_provincia':str,
        'pais':str, 
        'continente':str,
        'determinator_full_name':str,
        'determinator_full_name2':str,
        'collector_full_name':str,
        'collector_full_name2':str,
        'collector_full_name3':str,
        'collector_full_name4':str,
        'collector_full_name5':str,
        'collector_full_name6':str,
    }

    NewTable = NewTable.rename(columns=renames)

    return NewTable