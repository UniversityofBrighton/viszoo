import unidecode
import numpy as np
import pandas as pd

# proprietary functions in ./src/MNViz.py
from column_dict import *
from treatment_utils import *

def file_to_dataframe(state, app_version):
    file = state['file']
    if 'custom_mapping_file' not in state:
        if app_version == 'reptiles':
            data = excel_to_dataframe_reptiles(file)
        elif app_version == 'crustaceas':
            data = excel_to_dataframe_crustacea(file)
        elif app_version == 'GBIF':
            data = GBIF_tsv_to_dataframe(file)
    else:
        data = custom_file_to_dataframe(file, state['custom_mapping_file'], state['separator'])
    return data


# function to go from the excel file to the pandas dataframe used for the app
def excel_to_dataframe_reptiles(file):

    # name of the file used to test this : './data/Compilacao Livros Repteis - 2 a 10 - 2020_09_27 _ com subordens e perdidos incendio e tipos.xlsx'
    excel = pd.ExcelFile(file)
    sheet_name = excel.sheet_names

    db = excel.parse(sheet_name[0], sep=';', encoding='utf-8-sig')

    reptiles = db
    reptiles.columns = [str(col).replace(r'\n','') for col in reptiles.columns]

    names_col = {'DeterminatorFirst_and_LastName1': ['DeterminatorLastName1', 'DeterminatorFirstName1'],
                'CollectorFirst_and_LastName1': ['CollectorLastName1', 'CollectorFirstName1'],}
    for key, value in names_col.items():
        reptiles = create_column_full_name(reptiles, value[1], value[0], key)
        
    reptiles['author_full'] = reptiles['Autor']

    reptiles['first_author'] = reptiles['Autor'].apply(lambda x: str(x).split(',')[0])

    # 3 important dictionnaries and list initialised using column_dict.py
    renames = dict()
    selected_columns = list()
    dtypes = dict()
    
    column_dict = column_dict_reptiles

    for new_name, info in column_dict.items():
        renames[info['file_name']] = new_name

        if info['selected']:
            selected_columns.append(new_name)
            dtypes[new_name] = info['type']

    reptiles = reptiles.rename(columns=renames)

    # treatment for taxons columns
    taxon_columns = ['kingdom', 'phylum', 'class', 'order', 'suborder', 'family', 'genus_old',
                    'genus', 'species_old', 'species', 'subspecies_old',
                    'subspecies']  # selecting taxonomy columns

    treat_taxon_columns(reptiles, taxon_columns)

    # species and subspecies should be all lowercase
    reptiles['species'] = reptiles['species'].str.lower()
    reptiles['subspecies'] = reptiles['subspecies'].str.lower()

    # setting months and years
    reptiles['year_determined'] = reptiles['determined_date'].apply(lambda x: getMonthAndYear(x)[-1])
    reptiles['year_collected'] = reptiles['collected_date'].apply(lambda x: getMonthAndYear(x)[-1])
    reptiles['year_cataloged'] = reptiles['cataloged_date'].apply(lambda x: getMonthAndYear(x)[-1])

    reptiles['month_determined'] = reptiles['determined_date'].apply(lambda x: getMonthAndYear(x)[0])
    reptiles['month_collected'] = reptiles['collected_date'].apply(lambda x: getMonthAndYear(x)[0])
    reptiles['month_cataloged'] = reptiles['cataloged_date'].apply(lambda x: getMonthAndYear(x)[0])

    # Adjusting `Altitude` column
    reptiles['altitude'] = reptiles['MinAltitude'].str.extract('(\d+)')
    reptiles['max_altitude'] = reptiles['MaxAltitude'].str.extract('(\d+)')

    #regions treatment
    reptiles['region'] = reptiles['state'].apply(brazilian_region)
    
    # type defining
    reptiles['type_status'] = reptiles['NotasTaxonomicas'].apply(define_type)

    # specific order treatment
    reptiles['order'] = reptiles['order'].apply(correct_squamata)
    reptiles['order'] = reptiles['order'].apply(correct_nd)

    # creation of lost_in_fire column
    reptiles['lost_in_fire'] = reptiles['CollectionObjectRemarks'].apply(lost_in_fire)


    # column selection for the resulting dataframe
    NewTable = reptiles[selected_columns]

    # apply new types with respect to NaN
    for (key,value) in dtypes.items():
        NewTable[key] = NewTable.loc[:,key].apply(apply_type_with_nan, args=[value])


    return NewTable


# function to go from the excel file to the pandas dataframe used for the app
def excel_to_dataframe_crustacea(file):

    excel = pd.ExcelFile(file)
    sheet_name = excel.sheet_names

    db = excel.parse(sheet_name[0], sep=';', encoding='utf-8-sig')

    crustacea = db
    crustacea.columns = [str(col).replace(r'\n','') for col in crustacea.columns]

    names_col = {'determinator_full_name1': ['Determiner Last Name1', 'Determiner First Name1'],
                'collector_full_name1': ['Collector Last Name1', 'Collector First Name1'],}
    for key, value in names_col.items():
        crustacea = create_column_full_name(crustacea, value[1], value[0], key)

    # 3 important dictionnaries and list initialised using column_dict.py
    renames = dict()
    selected_columns = list()
    dtypes = dict()
    
    column_dict = column_dict_crustacea

    for new_name, info in column_dict.items():
        renames[info['file_name']] = new_name

        if info['selected']:
            selected_columns.append(new_name)
            dtypes[new_name] = info['type']

    crustacea = crustacea.rename(columns=renames)

    # treatment for taxons columns
    taxon_columns = ['kingdom', 'phylum', 'class', 'order', 'suborder', 'family',
                    'genus', 'species']  # selecting taxonomy columns

    treat_taxon_columns(crustacea, taxon_columns)

    # species and subspecies should be all lowercase
    crustacea['species'] = crustacea['species'].str.lower()

    # setting months and years  
        
    crustacea['year_determined'] = crustacea['Determined Date1'].apply(catch_year)
    crustacea['year_collected'] = crustacea['collected_date'].apply(catch_year)
    crustacea['year_cataloged'] = crustacea['cataloged_date'].apply(catch_year)

    crustacea['month_determined'] = crustacea['Determined Date1'].apply(catch_year, args=[True])
    crustacea['month_collected'] = crustacea['collected_date'].apply(catch_year, args=[True])
    crustacea['month_cataloged'] = crustacea['cataloged_date'].apply(catch_year, args=[True])
    #regions treatment
    crustacea['region'] = crustacea['region'].apply(brazilian_region)
    
    # type defining
    crustacea['type_status'] = crustacea['type_status'].apply(correct_type)

    crustacea['min_depth'] = crustacea['min_depth'].apply(get_depth)
    crustacea['max_depth'] = crustacea['max_depth'].apply(get_depth)


    crustacea['lat'] = crustacea['lat'].apply(correct_lat)
    crustacea['long'] = crustacea['long'].apply(correct_long)


    # column selection for the resulting dataframe
    NewTable = crustacea[selected_columns]

    NewTable = NewTable[NewTable['order'] == 'Decapoda']

    # apply new types with respect to NaN
    for (key,value) in dtypes.items():
        NewTable[key] = NewTable[key].apply(apply_type_with_nan, args=[value])


    return NewTable

def GBIF_tsv_to_dataframe(file):


    date_columns = ['eventDate', 'dateIdentified']
    gbif = pd.read_csv(file, sep='\t', parse_dates=date_columns)

    gbif.columns = [str(col).replace(r'\n','') for col in gbif.columns]

    # 3 important dictionnaries and list initialised using column_dict.py
    renames = dict()
    selected_columns = list()
    dtypes = dict()
    
    column_dict = column_dict_GBIF

    for new_name, info in column_dict.items():
        renames[info['file_name']] = new_name

        if info['selected']:
            selected_columns.append(new_name)
            dtypes[new_name] = info['type']

    return dataframe_treatment(gbif, renames, dtypes, selected_columns)

def update_dtypes(dtypes, row):
    type = row["type"]
    name = row["field"]

    if type == "text":
        dtypes[name] = str
    elif type == "integer":
        dtypes[name] = int
    elif type == "float":
        dtypes[name] = float

    return dtypes

def dataframe_treatment(data, renames, dtypes, selected_columns):

    data = data.rename(columns=renames)

    if 'determiner_first_name' in list(renames.values()) and 'determiner_last_name' in list(renames.values()):
        data = create_column_full_name(data, 'determiner_last_name', 'determiner_first_name', 'determinator_full_name')

    if 'collector_first_name' in list(renames.values()) and 'collector_last_name' in list(renames.values()):
        data = create_column_full_name(data, 'collector_last_name', 'collector_first_name', 'collector_full_name')

    data['year_determined'] = data['determined_date'].apply(lambda x : x.year)
    data['year_collected'] = data['collected_date'].apply(lambda x : x.year)

    data['month_determined'] = data['determined_date'].apply(lambda x : x.month)
    data['month_collected'] = data['collected_date'].apply(lambda x : x.month)


    data = data[selected_columns]

    for (key,value) in dtypes.items():
        data[key] = data[key].apply(apply_type_with_nan, args=[value])

    return data

def read_custom_mapping(custom_mapping_file):

    mapping = pd.read_csv(custom_mapping_file, index_col=False, header=0)

    date_columns = mapping.where(mapping["type"] == 'date')["name in your file"].dropna().tolist()
    print(date_columns)

    renames = dict()
    dtypes = dict()

    selected_columns = get_selected_columns()

    for i in mapping.index:
        if mapping.loc[i, "name in your file"] != '':
            renames[mapping.loc[i,"name in your file"]] = mapping.loc[i,"field"]
        if mapping.loc[i,'selected']:
            selected_columns[mapping.loc[i,"field"]] = True
            dtypes = update_dtypes(dtypes, mapping.loc[i])

    return date_columns, renames, dtypes, selected_columns


def custom_file_to_dataframe(file, custom_mapping_file, separator):
    
    date_columns, renames, dtypes, selected_columns = read_custom_mapping(custom_mapping_file)

    data = pd.read_csv(file, sep=separator,parse_dates=date_columns)

    data = dataframe_treatment(data, renames, dtypes, selected_columns)

    return data