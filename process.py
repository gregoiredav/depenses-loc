import sys

import pandas as pd

from lib import Cleaner, Compta, flag_vote_par_nature
import models


DATAFILE = sys.argv[1]
EXPORT_FILE_NAME = sys.argv[2]
OUTPUT_DATADIR = 'data_output/'

CATEGORIES = ['Commune']


# create dataframe from csv
df = pd.read_csv(
    filepath_or_buffer=DATAFILE,
    sep=';',
    encoding="ISO-8859-1",
    dtype=str,
    na_filter=False,
)

# Data cleaning
cleaner = Cleaner({
    'EXER': int,
    'INSEE': Cleaner.insee,
    'FONCTION': Cleaner.fonction,
    'NDEPT': Cleaner.ndept,
    'OOBDEB': Cleaner.chiffre,
    'OOBCRE': Cleaner.chiffre,
    'SD': Cleaner.chiffre,
    'SC': Cleaner.chiffre,
    'OBNETDEB': Cleaner.chiffre,
    'OBNETCRE': Cleaner.chiffre,
})
df = cleaner.clean(df)

# Filter par catégorie
df = df[df['CATEG'].isin(CATEGORIES)]

# Label aggregat de compte
df.loc[:, 'code_aggregat_compte'] = df['COMPTE'].apply(Compta.creer_aggregat_compte)
df.dropna(subset=['code_aggregat_compte'], inplace=True)
df['aggregat_compte'] = df['code_aggregat_compte'].apply(Compta.label_aggregat_compte)

# calculer les dépenses selon les aggrégats de compte
df = Compta.calcul_depenses_par_aggregat_compte(df)

# Aggréger code fonctions
df['code_aggregat_fonction'] = df['FONCTION'].apply(Compta.creer_aggregat_fonction)

# Flag votes par nature et corriger l'aggrégat
flags = flag_vote_par_nature(df)
df = df.merge(flags, on='IDENT')

correction = Compta.corriger_aggregat_fonction_vote_par_nature
mask = df['vote_par_nature']
df.loc[mask, 'code_aggregat_fonction'] = df.loc[mask, 'FONCTION'].apply(correction)

# étiquetter les codes fonctions
df['aggregat_fonction'] = df['code_aggregat_fonction'].apply(Compta.label_aggregat_fonction)

# aggregation par fonction et aggrégat de compte
grouped_df = (
    df
    .groupby([
        'siren',
        'NDEPT',
        'INSEE',
        'CTYPE',
        'NOMEN',
        'CATEG',
        'LBUDG',
        'IDENT',
        'code_aggregat_fonction',
        'aggregat_fonction',
        'code_aggregat_compte',
        'aggregat_compte',
    ])
    .agg({'depense': 'sum'})
    .reset_index()
)

# import et join pop data
grouped_df['code_commune'] = grouped_df['NDEPT'] + grouped_df['INSEE']
pop_data = models.population_data()
grouped_data_w_pop = grouped_df.merge(pop_data, how='left', on='code_commune')

# écriture data
grouped_data_w_pop.to_csv(OUTPUT_DATADIR + EXPORT_FILE_NAME, encoding="utf-8")
print("csv exporté in {} sous le nom {}".format(OUTPUT_DATADIR, EXPORT_FILE_NAME))