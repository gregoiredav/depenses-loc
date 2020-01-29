AGGREGATS_COMPTES = {
    1: {
        'label': 'Achats et charges externes',
        'comptes_a_inclure': ['60', '61', '62'],
        'comptes_a_exclure': ['621'],
    },
    2: {
        'label': 'Impôts et taxes',
        'comptes_a_inclure': ['63'],
        'comptes_a_exclure': ['631', '633'],
    },
    3: {
        'label': 'Charges de personnel',
        'comptes_a_inclure': ['64', '621', '631', '633'],
        'comptes_a_exclure': [],
    },
    4: {
        'label': 'Autres charges de gestion courante',
        'comptes_a_inclure': ['65'],
        'comptes_a_exclure': [],
    },
    5: {
        'label': 'Charges financieres',
        'comptes_a_inclure': ['66'],
        'comptes_a_exclure': [],
        },
    6: {
        'label': 'Charges exceptionnelles',
        'comptes_a_inclure': ['67'],
        'comptes_a_exclure': ['675', '676'],
    },
    7: {
        'label': 'Depenses directes d\'investissement',
        'comptes_a_inclure': ['20', '21', '23'],
        'comptes_a_exclure': ['204'],
    },
    8: {
        'label': 'Subventions d equipement versees',
        'comptes_a_inclure': ['204'],
        'comptes_a_exclure': [],
    },
    9: {
        'label': 'Prises de participation',
        'comptes_a_inclure': ['261', '271', '272', '25'],
        'comptes_a_exclure': [],
    },
    10: {
        'label': 'Prêts accordés',
        'comptes_a_inclure': ['26', '27'],
        'comptes_a_exclure': ['261', '271', '272', '25'],
    },
    11: {
        'label': 'Remboursement d\'emprunts et de dettes assimilées',
        'comptes_a_inclure': ['16'],
        'comptes_a_exclure': ['1688', '166'],
    },
}

AGGREGATS_FONCTIONS = {
    0: 'Services généraux et opérations non ventilables',
    1: 'Sécurité et salubrité publiques',
    2: 'Enseignement – formation',
    3: 'Culture',
    4: 'Sport et jeunesse',
    5: 'Interventions sociales et santé',
    6: 'Famille',
    7: 'Logement',
    8: 'Aménagement et services urbains, environnement',
    9: 'Action économique',
}


def MODES_DE_CALCUL_DEPENSES(df):
    return [
        {
            'codes_aggregat_compte': [1, 2, 3, 4, 5, 6],
            'calcul': df['SD'] - df['SC'],
            'label_calcul': 'SD - SC',
        },
        {
            'codes_aggregat_compte': [7, 8, 9],
            'calcul': (df['OBNETDEB'] - df['OBNETCRE']) - (df['OOBDEB'] - df['OOBCRE']),
            'label_calcul': '(OBNETDEB - OBNETCRE) - (OOBDEB - OOBCRE)',
        },
        {
            'codes_aggregat_compte': [10, 11],
            'calcul': df['OBNETDEB'],
            'label_calcul': 'OBNETDEB',
        },
    ]
