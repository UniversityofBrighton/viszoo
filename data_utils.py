import pandas as pd

#there are 5 positional arguments
def filter_data(data, families_filter_out, type_filter_out, time1, time2):

  data[['familia','type_status']] = data[['familia','type_status']].astype(str)

  filtered_data =  data.where((data['ano_coleta'] <= time2) & (data['ano_coleta'] >= time1))
  filtered_data = filtered_data.where((~filtered_data['familia'].isin(families_filter_out)))
  filtered_data = filtered_data.where((~filtered_data['type_status'].isin(type_filter_out)))

  return filtered_data
