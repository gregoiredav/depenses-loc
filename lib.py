from nomenclatures import DEFINITION_AGGREGATS, LABEL_AGGREGATS, LABEL_FONCTIONS


def string_to_float(ligne):
    return float(ligne.replace(',','.'))


def get_code_aggregat(ligne):
    for code_aggregat, conditions in DEFINITION_AGGREGATS.items():
        if flag_aggregat(ligne, conditions['a_prendre'], conditions['a_exclure']):
            return code_aggregat


def flag_aggregat(ligne, a_prendre, a_exclure):
    flag = False
    for compte in a_prendre:
        if ligne.startswith(compte):
            flag = True
    for compte in a_exclure:
        if ligne.startswith(compte):
            flag=False
    return flag


def label_aggregat(code):
    if code:
        return LABEL_AGGREGATS[code]


def label_fonction(code):
    return LABEL_FONCTIONS[code]


def pad_ndept(code):
    if len(str(code)) == 1:
        code = '0' + str(code)
    return str(code)