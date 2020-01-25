import sys

import pandas as pd

from lib import string_to_float, get_code_aggregat, label_aggregat, label_fonction, pad_ndept, clean_insee_type
import models


DATAFILE = sys.argv[1]
EXPORT_FILE_NAME = sys.argv[2]
DATADIR = 'data_output/'


# create dataframe from csv
data = pd.read_csv(DATAFILE, sep=';', encoding="ISO-8859-1", dtype=str)

# convertir colonnes de dépense en float
for col in ['SD', 'SC', 'OBNETDEB', 'OBNETCRE', 'OOBDEB', 'OOBCRE']:
    data[col] = data[col].apply(str).apply(string_to_float)

# autre traitements
data['COMPTE'] = data['COMPTE'].apply(str)
data['INSEE'] = data['INSEE'].fillna(0).apply(str).apply(clean_insee_type)

# étiquetter les aggregats
data['code_aggregat'] = data['COMPTE'].apply(get_code_aggregat)
data = data.dropna(subset=['code_aggregat'])
data['aggregat'] = data['code_aggregat'].apply(label_aggregat)

# calculer les dépenses selon les aggrégats
calcul_depense_1 = data['code_aggregat'].isin([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
calcul_depense_2 = data['code_aggregat'].isin([7.0, 8.0, 9.0])
calcul_depense_3 = data['code_aggregat'].isin([10.0, 11.0])

data.loc[calcul_depense_1, 'depense'] = data['SD'] - data['SC']
data.loc[calcul_depense_2, 'depense'] = data['OBNETDEB'] - data['OBNETCRE'] - (data['OOBDEB'] - data['OOBCRE'])
data.loc[calcul_depense_3, 'depense'] = data['OBNETDEB']

# tronquer et étiquetter les codes fonctions
data['FONCTION'].fillna(0, inplace=True)
data['code_fonction'] = data['FONCTION'].apply(lambda x: str(x)[0])
data['fonction'] = data['code_fonction'].apply(lambda x: label_fonction(int(x)))

# concat departement et code insee
data['departement'] = data['NDEPT'].apply(pad_ndept)
data['INSEE'].fillna(0, inplace=True)
data['code_commune'] = data['departement'] + data['INSEE'].apply(lambda x: str(int(x)))

# aggregation par fonction et aggrégat de compte
grouped_data = (
    data
    .groupby(['siren', 'NDEPT', 'CTYPE', 'NOMEN', 'CATEG', 'LBUDG', 'IDENT', 'fonction', 'code_commune', 'aggregat'])
    .agg({'depense': 'sum'})
    .reset_index()
)

# import et join pop data
pop_data = models.population_data()
grouped_data_w_pop = grouped_data.merge(pop_data, how='left', on='code_commune')

# écriture data
grouped_data_w_pop.to_csv(DATADIR + EXPORT_FILE_NAME, encoding="utf-8")
print("csv exporté in {} sous le nom {}".format(DATADIR, EXPORT_FILE_NAME))