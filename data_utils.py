import pandas as pd

def filter_data(data: pd.DataFrame, families_filter_out, time1, time2):

  filtered_data =  data.where((data['ano_coleta'] <= time2) & (data['ano_coleta'] >= time1))
  filtered_data = filtered_data.where((~filtered_data['familia'].isin(families_filter_out)))

  return filtered_data