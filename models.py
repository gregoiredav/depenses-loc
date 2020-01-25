import pandas as pd


DATA_DIR = 'data_input/'


def population_data():
    pop_data_path = DATA_DIR + 'base_pop_insee.csv'
    pop_data = pd.read_csv(pop_data_path, sep=';')
    pop_data_agg = pop_data.groupby(['COM', 'LIBCOM']).sum().sort_values('P16_POP', ascending=False).reset_index()
    return pop_data_agg.rename(columns={'COM': 'code_commune', 'LIBCOM': 'commune', 'P16_POP': 'population_2016'})
