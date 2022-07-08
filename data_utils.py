import pandas as pd
from src.MNViz_colors import cores_familia_crustacea, cores_familia_reptiles

#there are 5 positional arguments
def filter_data(data, families_filter_out, type_filter_out, time1, time2):

  data[['family','type_status']] = data[['family','type_status']].astype(str)

  filtered_data =  data.where((data['year_collected'] <= time2) & (data['year_collected'] >= time1))
  filtered_data = filtered_data.where((~filtered_data['family'].isin(families_filter_out)))
  filtered_data = filtered_data.where((~filtered_data['type_status'].isin(type_filter_out)))

  return filtered_data


def create_map_data(data:pd.DataFrame):
  renames = {
    'long':'lon'
  }

  to_keep = [
    'lon',
    'lat',
  ]

  data =  data.rename(columns=renames)[to_keep][:3000]
  data.dropna(subset=to_keep, inplace=True)

  return data

def get_colors(app_version):
  if app_version == 'crustacea':
      return cores_familia_crustacea
  elif app_version == 'reptiles':
      return cores_familia_reptiles