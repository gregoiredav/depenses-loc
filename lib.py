from functools import reduce

import pandas as pd

from compta import AGGREGATS_FONCTIONS, AGGREGATS_COMPTES, MODES_DE_CALCUL_DEPENSES


class Cleaner(object):

    def __init__(self, actions):
        self.actions = actions

    def clean(self, df):
        for col, action in self.actions.items():
            df[col] = df[col].apply(action)
        return df

    @staticmethod
    def chiffre(ligne):
        return float(ligne.replace(',', '.'))

    @staticmethod
    def insee(ligne):
        if ligne.startswith('`'):
            return ligne[1:]
        return ligne

    @staticmethod
    def fonction(ligne):
        if ligne == '':
            return '000'
        else:
            return (
                ligne
                .replace('-', '')
                .replace('.', '')
            )

    @staticmethod
    def ndept(ligne):
        if ligne.startswith('0'):
            ligne = ligne[1:]
        return ligne


class Compta(object):

    @classmethod
    def creer_aggregat_compte(cls, ligne):
        for code, aggregat in AGGREGATS_COMPTES.items():
            try:
                comptes_a_inclure = aggregat['comptes_a_inclure']
            except KeyError:
                print(aggregat)
                raise
            comptes_a_exclure = aggregat['comptes_a_exclure']
            if cls._flag_aggregat_compte(ligne, comptes_a_inclure, comptes_a_exclure):
                return code

    @staticmethod
    def label_aggregat_compte(code):
        if code:
            return AGGREGATS_COMPTES[code]['label']

    @staticmethod
    def creer_aggregat_fonction(code):
        return int(code[0])

    @staticmethod
    def label_aggregat_fonction(code):
        return AGGREGATS_FONCTIONS[code]

    @staticmethod
    def calcul_depenses_par_aggregat_compte(df):
        modes_de_calcul = MODES_DE_CALCUL_DEPENSES(df)
        for mode_de_calcul in modes_de_calcul:
            codes_aggregat = mode_de_calcul['codes_aggregat_compte']
            calcul_depense = mode_de_calcul['calcul']
            label_calcul = mode_de_calcul['label_calcul']
            df.loc[df['code_aggregat_compte'].isin(codes_aggregat), 'depense'] = calcul_depense
            df.loc[df['code_aggregat_compte'].isin(codes_aggregat), 'calcul_depense'] = label_calcul
        return df

    @staticmethod
    def _flag_aggregat_compte(ligne, a_prendre, a_exclure):
        flag = False
        for compte in a_prendre:
            if ligne.startswith(compte):
                flag = True
        for compte in a_exclure:
            if ligne.startswith(compte):
                flag=False
        return flag

    @staticmethod
    def corriger_aggregat_fonction_vote_par_nature(code):
        return int(code[2])


def flag_vote_par_nature(df):
    grouped = (
        df
        .groupby('IDENT')
        .apply(_custom_aggregation)
        .reset_index()
    )
    vote_par_nature = (
        True
        & (grouped['fonction_min_length'] >= 3)
        & (
                (grouped['aggregat_set'] == {9}) |
                (grouped['aggregat_set'] == {0, 9})
        )
    )
    grouped['vote_par_nature'] = vote_par_nature
    return grouped


def _series_min_length(series):
    return reduce(lambda x, y: min(x, y), map(len, series))


def _series_to_set(series):
    return set(series)


def _custom_aggregation(df):
    names = {
        'fonction_min_length': _series_min_length(df['FONCTION']),
        'aggregat_set': _series_to_set(df['code_aggregat_fonction']),
    }
    return pd.Series(names)
