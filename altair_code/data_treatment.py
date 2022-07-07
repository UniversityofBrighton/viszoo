import unidecode
import numpy as np
import pandas as pd

# proprietary functions in ./src/MNViz.py
from src.MNViz import *

# function to define type
def define_type(t):
    t = str(t).strip().lower().capitalize()

    if t == 'Nan' or t=='Null':
        return np.NAN
    else:
        return t

# function to apply new types with respect to NaN
def apply_type_with_nan(value, new_type):
    try:
        if str(value).lower() == 'nan':
            return np.NaN
        else:
            return new_type(value)
    except:
        return np.NAN

# function to determine if the instance was lost to fire
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

# function to go from the excel file to the pandas dataframe used for the app
def excel_to_dataframe(file):

    # name of the file used to test this : './data/Compilacao Livros Repteis - 2 a 10 - 2020_09_27 _ com subordens e perdidos incendio e tipos.xlsx'
    excel = pd.ExcelFile(file)
    sheet_name = excel.sheet_names

    db = excel.parse(sheet_name[0], sep=';', encoding='utf-8-sig')

    repteis = db
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

    # aggregating name columns
    repteis['DeterminatorFirst_and_LastName'] = repteis['DeterminatorFirstName1'].str.strip() + ' ' + repteis['DeterminatorLastName1'].str.strip()
    repteis['CollectorFirst_and_LastName'] = repteis['CollectorFirstName1'].str.strip() + ' ' + repteis['CollectorLastName1'].str.strip()

    for i in range(2, 7):    
        if i < 3:
            # determinator 
            repteis[f'DeterminatorFirst_and_LastName{i}'] = repteis[f'DeterminatorFirstName{i}'].astype(str).str.strip() + ' ' + repteis[f'DeterminatorLastName{i}'].astype(str).str.strip()
        
        # collector
        repteis[f'CollectorFirst_and_LastName{i}'] = repteis[f'CollectorFirstName{i}'].str.strip() + ' ' + repteis[f'CollectorLastName{i}'].str.strip()


    repteis['author_full'] = repteis['Autor']

    repteis['first_author'] = repteis['Autor'].apply(lambda x: str(x).split(',')[0])


    # renaming of columns
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
        'Subespecie_ent':'subespecie_ent',
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
    repteis = repteis.rename(columns=renames)

    # treatment for taxons columns
    taxon_columns = ['kingdom', 'phylum', 'class', 'ordem', 'subordem', 'familia', 'genero_ent',
                    'genero_atual', 'especie_ent', 'especie_atual', 'subespecie_ent',
                    'subespecie_atual']  # selecting taxonomy columns

    treat_taxon_columns(repteis, taxon_columns)

    # species and subspecies should be all lowercase
    repteis['especie_atual'] = repteis['especie_atual'].str.lower()
    repteis['subespecie_atual'] = repteis['subespecie_atual'].str.lower()

    # setting months and years
    repteis['ano_descricao'] = repteis['data_determinacao'].apply(lambda x: getMonthAndYear(x)[-1])
    repteis['ano_coleta'] = repteis['data_coleta'].apply(lambda x: getMonthAndYear(x)[-1])
    repteis['ano_entrada'] = repteis['data_entrada'].apply(lambda x: getMonthAndYear(x)[-1])

    repteis['mes_determinacao'] = repteis['data_determinacao'].apply(lambda x: getMonthAndYear(x)[0])
    repteis['mes_coleta'] = repteis['data_coleta'].apply(lambda x: getMonthAndYear(x)[0])
    repteis['mes_entrada'] = repteis['data_entrada'].apply(lambda x: getMonthAndYear(x)[0])

    # Adjusting `Altitude` column
    repteis['altitude'] = repteis['MinAltitude'].str.extract('(\d+)')
    repteis['max_altitude'] = repteis['MaxAltitude'].str.extract('(\d+)')

    #regions treatment
    repteis['regiao'] = repteis['estado_ou_provincia'].apply(brazilian_region)
    
    # type defining
    repteis['type_status'] = repteis['NotasTaxonomicas'].apply(define_type)

    # specific order treatment
    repteis['ordem'] = repteis['ordem'].apply(correct_squamata)
    repteis['ordem'] = repteis['ordem'].apply(correct_nd)

    # creation of lost_in_fire column
    repteis['lost_in_fire'] = repteis['CollectionObjectRemarks'].apply(lost_in_fire)


    # column selection for the resulting dataframe
    selected_columns = ['numero_catalogo','data_entrada','data_determinacao','data_coleta',
                        'ano_entrada', 'mes_entrada', 'mes_determinacao',
                        'ano_coleta', 'mes_coleta',
                        'class','kingdom', 
                        'genero_ent', 'genero_atual', 'especie_ent', 'especie_atual','subespecie_atual','type_status','determinator_full_name',
                        'determinator_full_name2',
                        'collector_full_name', 'collector_full_name2',
                        'collector_full_name3', 'collector_full_name4',
                        'collector_full_name5', 'collector_full_name6',
                        'altitude', 'max_altitude',
                        'ordem','subordem',  'familia', 'phylum', 'qualificador_atual',
                        'lat', 'long', 'municipio', 
                        'estado_ou_provincia', 'pais', 'continente', 'regiao', 'lost_in_fire',
                        'ano_descricao', 'author_full', 'first_author']
    NewTable = repteis[selected_columns]


    # apply new types with respect to NaN
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
        'numero_catalogo':int,
        'ano_entrada':int,
        'mes_entrada':int,
        'mes_determinacao':int,
        'ano_coleta':int,
        'mes_coleta':int,
        'altitude':float,
        'max_altitude':float,
        'lat':float,
        'long':float, 
        'lost_in_fire':int,
        'ano_descricao':int,
        'author_full':str,
        'first_author':str,
    }
    for (key,value) in dtypes.items():
        NewTable[key] = NewTable[key].apply(apply_type_with_nan, args=[value])


    return NewTable