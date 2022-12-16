# BREEDS DICTIONARY
breeds_dict = {
    '': 'XSH',
    'Norwegische Waldkatze': 'NFO',
    'Abessinier': 'ABY',
    'American Curl (Kurzhaar)': 'ACS',
    'American Curl Langhaar': 'ACL',
    'American Shorthair': 'ASH',
    'Arabian Mau': 'ARM',
    'Asian Bombay': 'BOM',
    'Asian Burma': 'BUR',
    'Asian Burmilla': 'BML',
    'Asian Self': 'ASN',
    'Balinese': 'BAL w',
    'Bengal': 'BEN',
    'Birma': 'SBI',
    'Bombay': 'BOM',
    'Britisch Kurzhaar': 'BRI',
    'Britisch Langhaar': 'BLH',
    'Burma': 'BUR',
    'Burmilla': 'BML',
    'Cashmere': 'CAM',
    'Chartreux': 'CHA',
    'Chausie': 'CHS',
    'Cornish Rex': 'CLX',
    'Deutsch Langhaar': 'DLH',
    'Devon Rex': 'DRX',
    'Don Sphinx': 'DSX',
    'Europäisch Kurzhaar': 'BUR',
    'Exotic Shorthair': 'EXO',
    'German Rex': 'GRX',
    'German Rex Hybrid': 'GRX',
    'Halblanghaar': 'XLH',
    'Hauskatze': 'HPS',
    'Highland Fold': 'SFL',
    'Japanese Bobtail': 'JBT',
    'Javanese': 'JBT',
    'Kurilische Bobtail Kurzhaar': 'KBS',
    'Kurilische Bobtail Langhaar': 'KBL',
    'Kurzhaar': 'XSH',
    'LaPerm Kurzhaar': 'LPS',
    'LaPerm Langhaar': 'LPL',
    'Lykoi': 'LYS',
    'Maine Coon': 'MCO',
    'Mekong Bobtail': 'MBT',
    'Mischling': 'HPS',
    'Nebelung': 'NEB',
    'Neva Masquarade': 'SIB',
    'Ocicat': 'OCI',
    'Orientalisch Kurzhaar': 'OSH',
    'Perser': 'PER',
    'Peterbald': 'PBD',
    'Ragdoll': 'RAG',
    'Russisch Blau': 'RUS',
    'Savannah': 'SAV',
    'Scottish Fold': 'SFS',
    'Scottish Fold Langhaar': 'SFL',
    'Selkirk Rex': 'SRL',
    'Selkirk Rex Kurzhaar': 'SRX',
    'Serengeti': 'SGT',
    'Serval': 'SER',
    'Seychellois': 'SIA',
    'Seychellois Halblanghaar': 'BAL',
    'Siam': 'SIA',
    'Siam Variant': 'SIA',
    'Sibirische Katze': 'SIB',
    'Singapura': 'SIN',
    'Snowshoe': 'SNO',
    'Sokoke': 'SOK',
    'Somali': 'SOM',
    'Sphinx': 'SPH',
    'Thai': 'THA',
    'Thai Langhaar': 'THA',
    'Tonkanese': 'TON',
    'Toyger': 'TOY',
    'Türkisch Angora': 'TUA',
    'Türkisch Van': 'TUV',
    'Türkisch Van (Kurzhaar)': 'TUV',
    'York': 'YOR',
    'Ägyptisch Mau': 'MAU'
}
# TITLES DICTIONARY
titles_dict = {  # 'Baby Champion',
    # #  'Champion',
    # #  'Champion Alter',
    # #  'Champion Premior',
    # #  'Double Grand Champion',
    # #  'Double Grand Champion Alter',
    # #  'European Champion',
    # #  'European Champion Premior',
    # #  'European Silver Champion',
    # #  'Gold Champion',
    # #  'Grand Champion',
    # #  'Grand Champion Alter',
    # #  'Grand European Champion',
    # #  'Grand European Champion Premior',
    # #  'Grand European Gold Champion',
    # #  'Grand European Silver Champion',
    # #  'Grand European Silver Champion Premior',
    # #  'Grand International Champion',
    # #  'Grand International Champion Premior',
    # #  'Grand International Gold Champion',
    # #  'Grand International Silver Champion',
    # #  'House Hold Pet Champion',
    # #  'House Hold Pet European Champion',
    # #  'International Champion',
    # #  'International Champion Premior',
    # #  'International Gold Champion',
    # #  'International Gold Champion Premior',
    # #  'International Silver Champion',
    # #  'International Silver Champion Premior',
    # #  'Junior Champion',
    # #  'Kitten Champion',
    # #  'Quadruple Grand Champion',
    # #  'Silver Champion',
    # #  'Supreme Grand Champion',
    # #  'Supreme Grand Champion Alter',
    # #  'Triple Grand Champion',
    # #  'Triple Grand Champion Alter',
    # #  'Träger des Felidae Gütesiegels',
    # #  'Träger des RVDE Gütesiegels',
    # #  'US Champion',
    # #  'US Grand Champion',
    # #  'US International Grand Champion',
    # #  'World Champion',
    # #  'World Champion Premior',
    # #  'World Gold Champion',
    # #  'World Gold Champion Premior',
    # #  'World Platinum Champion',
    # #  'World Silver Champion',
    # #  'World Silver Champion Premior'
}
# FUNCTION  TO MAP GERMAN DATABASE IDS TO OUR IDS
def map_ids(lines):
    count = 1
    id_pairs = {}
    for x in lines:
        rec = x.replace(';', '').split('|')
        id_pairs.update({rec[3]: str(count)})
        count += 1
    return id_pairs
# FUNCTION RETURNING TRANSFORMED BREEDS SHORT VERSION
def get_breed(record, breeds_dict):
    if record is not None:
        return breeds_dict[str(record)]
    else:
        return ''
# FUNCTION TO CHANGE DATE FORMAT
def change_date_format(date):
    if date != '' and date is not None :
        parts = date.split('.')
        return parts[2] + '-' + parts[1] + '-' + parts[0]
    else:
        return ''

# FUNCTION TO TRANSFORM PARENT IDS
def transform_parent_id(record, id_pairs):
    if record != '' and record is not None:
        return id_pairs[str(record)]
    else:
        return ''

# FUNCTION TO TRANSFORM PARENT NAMES
def transform_parent_name(record):
    if record == 'Unknown' or record is None:
        return ''
    elif record == 'Foundation':
        return '###FOUNDATION###'
    else:
        return record

# FUNCTION TO MAKE TRANSFORMATIONS OVER ALL NEEDED COLUMNS
def format_corrections(count, record, id_pairs):
    rec = record.replace(';', '').split('|')
    rec[0] = str(count)
    rec[8] = breeds_dict[rec[8]]
    rec[10] = change_date_format(str(rec[10]))
    rec[17] = transform_parent_id(str(rec[17]), id_pairs)
    rec[18] = transform_parent_id(str(rec[18]), id_pairs)
    rec[19] = transform_parent_name(str(rec[19]))
    rec[20] = transform_parent_name(str(rec[20]))
    rec.insert(6, None)
    rec.insert(7, None)
    rec.insert(12, None)
    return rec

# FUNCTION TO PARSE DATA TO FINAL FORMAT
def transform_to_final_format(rec):
    csv_format = ''
    for value in rec:
        if value is None:
            csv_format += '|'
            continue
        csv_format += str(value) + '|'
    return (''.join(csv_format)[:-1] + ';\n')


def get_lines():
    with open("all_cats.txt", encoding='utf-8') as file:
        lines = file.readlines()
        return [line.rstrip() for line in lines]

# MAIN TRANSFORMING DATA LINES ONE BY ONE AND CREATION OF NEW TRANSFORMED DATAFILE WITH HEADER
lines = get_lines()
file = open('cats5.txt', 'a', encoding="utf-8")
file.write(
    'ID|NAME|SOURCE_DB|SOURCE_ID|REGISTRATION_NUMBER_BEFORE|REGISTRATION_NUMBER_CURRENT|ORIGIN_COUNTRY|CURRENT_COUNTRY|TITLE_BEFORE|TITLE_AFTER|BREED|COLOR_CODE|COLOR|BIRTH_DATE|GENDER|CHIP|NOTE(DESCRIPTION)|AWARDS|HEALTH_STATUS|CATTERY|MOTHER_ID|FATHER_ID|MOTHER_NAME|FATHER_NAME|MOTHER_REG_NUMBER|FATHER_REG_NUMBER;\n')
count = 1
id_pairs = map_ids(lines)

for x in lines:
    rec = format_corrections(count, x, id_pairs)
    result = transform_to_final_format(rec)
    file = open('cats5.txt', 'a', encoding="utf-8")
    file.write(result)
    count += 1


# BLOCK FOR MANUAL DELETING WRONG DATA (NO EXISTING NAMES)
# count = 0
# id_count = 1
# for x in lines:
#     rec = x.replace(';', '').split('|')
#     if rec[1]=='' or len(rec[1])<2:
#         count+=1
#         continue
#     rec[0] = str(id_count)
#     id_count += 1
#     result = transform_to_final_format(rec)
#     file = open('all_cats3.txt', 'a', encoding="utf-8")
#     file.write(result)
# print(count)