LIBELLE_AGGREGATS = {
    1: 'Achats et charges externes',
    2: 'Impôts et taxes',
    3: 'Charges de personnel',
    4: 'Autres charges de gestion courante',
    5: 'Charges financieres',
    6: 'Charges exceptionnelles',
    7: 'Depenses directes d investissement',
    8: 'Subventions d equipement versees',
    9: 'Prises de participation',
    10: 'Prets accordes',
    11: 'Remboursement d emprunts et de dettes assimilees',
}

DEFINITION_AGGREGATS = {
    1: {'a_prendre': ['60', '61', '62'], 'a_exclure': ['621']},
    2: {'a_prendre': ['63'], 'a_exclure': ['631', '633']},
    3: {'a_prendre': ['64', '621', '631', '633'], 'a_exclure': []},
    4: {'a_prendre': ['65'], 'a_exclure': []},
    5: {'a_prendre': ['66'], 'a_exclure': []},
    6: {'a_prendre': ['67'], 'a_exclure': ['675', '676']},
    7: {'a_prendre': ['20', '21', '23'], 'a_exclure': ['204']},
    8: {'a_prendre': ['204'], 'a_exclure': []},
    9: {'a_prendre': ['261', '271', '272', '25'], 'a_exclure': []},
    10: {'a_prendre': ['26', '27'], 'a_exclure': ['261', '271', '272', '25']},
    11: {'a_prendre': ['16'], 'a_exclure': ['1688', '166']},
}

LIBELLE_FONCTIONS = {
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