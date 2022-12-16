import time
import requests
import re
from pprint import pprint

#FUNCTION TO GET CURRENT WEBPAGE IN HTML FORMAT
def get_page(session, url):
    request = session.get(url).text
    html_text = re.sub("\s+", " ", request)
    return html_text

#PARSING OF PARENT INFO VALUES EXTRACTED FROM PARENT WEBPAGE
def validate_parent_info(parents_info, parents_dict):
    if parents_info[0] == 'Foundation':
        parents_dict['FATHER_NAME'] = 'Foundation'

    if parents_info[1] == 'Foundation':
        parents_dict['MOTHER_NAME'] = 'Foundation'

    if parents_info[0] == 'Unknown':
        parents_dict['FATHER_NAME'] = 'Unknown'

    if parents_info[1] == 'Unknown':
        parents_dict['MOTHER_NAME'] = 'Unknown'

    if len(parents_info[0]) == 3:
        parents_dict['FATHER_ID'] = parents_info[0][0]
        parents_dict['FATHER_NAME'] = parents_info[0][1]
        parents_dict['FATHER_REG_NUMBER'] = parents_info[0][2]

    if len(parents_info[1]) == 3:
        parents_dict['MOTHER_ID'] = parents_info[1][0]
        parents_dict['MOTHER_NAME'] = parents_info[1][1]
        parents_dict['MOTHER_REG_NUMBER'] = parents_info[1][2]
    return parents_dict

#FUNCTION TO TRANSFORM GENDER FORMAT
def refine_data(value):
    if value == 'female':
        return 'F'
    if value == 'male':
        return 'M'
    if value != 'female' or value != 'male':
        return ''


#INITIALIZATION DICTIONARY FOR PARENTS PAGE
def init_parent_dict():
    return {
        'MOTHER_ID': None,
        'FATHER_ID': None,
        'MOTHER_NAME': None,
        'FATHER_NAME': None,
        'MOTHER_REG_NUMBER': None,
        'FATHER_REG_NUMBER': None
    }

#DICTIONARY FOR CAT INFO FORMING FINAL FORMAT
def transform_dict_format(cats_id, cat_info, parents_info, awards_info):
    return {
        'ID': cats_id,
        'NAME': refine_data(cat_info['Name']),
        'SOURCE_DB': 'German Database',
        'SOURCE_ID': cats_id,
        'REGISTRATION_NUMBER_BEFORE': None,
        'REGISTRATION_NUMBER_CURRENT': None,
        'TITLE_BEFORE': refine_data(cat_info['Aktueller Titel']),
        'TITLE_AFTER': None,
        'BREED': refine_data(cat_info['Rasse']),
        'COLOR_CODE': refine_data(cat_info['Farbcode']),
        'BIRTH_DATE': refine_data(cat_info['Geburtsdatum']),
        'GENDER': refine_data(cat_info['Geschlecht']),
        'CHIP': None,
        'NOTE(DESCRIPTION)': refine_data(cat_info['Beschreibung']),
        'AWARDS': awards_info,
        'HEALTH_STATUS': None,
        'CATTERY': None,
        'MOTHER_ID': parents_info['MOTHER_ID'],
        'FATHER_ID': parents_info['FATHER_ID'],
        'MOTHER_NAME': parents_info['MOTHER_NAME'],
        'FATHER_NAME': parents_info['FATHER_NAME'],
        'MOTHER_REG_NUMBER': parents_info['MOTHER_REG_NUMBER'],
        'FATHER_REG_NUMBER': parents_info['FATHER_REG_NUMBER']
    }

# FUNCTION TO DELETING TAGS AN UNNEEDED INFO TO GET JUST INFORMATIONS ABOUT CATS PARENTS
# USING 3 REGEX FUNCTIONS ONE WOULD BE TO LONG AND COMPLICATED
def extract_parent_informations(context):
    parent_info_block_pattern = re.compile(
        r'<td bgcolor="#F5F4D4" class="ak" width=200 height="440" rowspan=8>.*?</td><td>.*?</td>.*?</div><div class="ak">.*?</div>')
    check_pattern = re.compile(r'<td bgcolor="#F5F4D4" class="ak" width=200 height="440" rowspan=8>(.*?)</td>')
    result_pattern = re.compile(
        r'<font color=".*?id=(.*?)&type=sb&l=0"><font color=".*?"><b>(.*?)</font></b></a><br/><table><tr><td>.*?</td><td>(.*?)</td>')

    parent_info_block = re.findall(parent_info_block_pattern, context)
    no_parent = re.findall(check_pattern, context)
    result = re.findall(result_pattern, str(parent_info_block))
    #CHECKING EMPTY PAGE NO INFORMATION OR UNKNOWN PARENT
    if len(no_parent) == 0:
        return 'NOT FOUND'
    if len(no_parent) > 0 and no_parent[0] == 'Foundation':
        result.insert(0, 'Foundation')
    if len(no_parent) > 0 and no_parent[1] == 'Foundation':
        result.append('Foundation')
    if len(no_parent) > 0 and no_parent[0] == 'Unknown':
        result.insert(0, 'Unknown')
    if len(no_parent) > 0 and no_parent[1] == 'Unknown':
        result.append('Unknown')

    parent_dict = validate_parent_info(result, init_parent_dict())
    return parent_dict

#FUNCTION TO EXTRACT INFORMATION FROM THIRD PAGE ABOUT CATS REWARDS
def extract_awards_informations(context):
    awards_info = re.compile(r'<table cellpadding="1" width="700"><tr><td class="u1" colspan="2"><b>(.*?)</b>')
    return '•'.join(re.findall(awards_info, context))

# FUNCTION TO EXTRACT INFORMATION ABOUT CAT ION MAIN PAGE
# USING DIFFERENT REGEX TECHNIQUES
def extract_cat_informations(context):
    cat_info1 = re.compile(r'<td class="a" align="right">.*?<b>.*</b></td>')
    result = ''.join(re.findall(cat_info1, context))
    result = re.sub('<[^>]*>', '', result) + '   '
    groups = re.findall(r'(\w+[ ]?\w+):[ ]{1,2}(.*?)[ ]{2,3}', result)
    return dict(groups)

# PARSING FUNCITON TO TRANSFORM DICTIONARY INTO ONE STRING WHICH WILL BE WRITTEN INTO TEXTFILE
def transform_to_final_format(cats_id, cat_info, parent_info, awards_info):
    cats_data = transform_dict_format(cats_id, cat_info, parent_info, awards_info)
    csv_format = ''
    values = cats_data.values()
    for value in values:
        if value is None:
            csv_format = csv_format + '|'
            continue
        csv_format = csv_format + str(value) + '|'
    print(csv_format)
    return csv_format[:-1] + ';\n'
#FUNCTION TO CHCECK RESULTS IF SCRAPING WAS SUCCESFUL SO IF WE GOT ANY DATA

def check_result(cat_id,content,content2,content3):
    if content2 == 'NOT FOUND':
        print('NOT FOUND')
        return
    file = open('textfile.txt', 'a', encoding="utf-8")
    data = transform_to_final_format(cat_id, content, content2, content3)
    file.write(data)
    file.close()
    time.sleep(0.5)
    # EVERY N RECORDS SCRAPPED SETTING SOME SLEEP FOR AVOIDING TIMEOUTS
    if cat_id % 101 == 0:
        time.sleep(5)
    elif cat_id % 600 == 0:
        time.sleep(20)
    elif cat_id % 1000 == 0:
        time.sleep(30)
    elif cat_id % 2500 == 0:
        time.sleep(60)
# FUNCTION TO GET CONTENTS FROM ALL 3 PAGES WITH INFORMATION ABOUT CAT
def start_crawling(x,y):
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=0))
    for cat_id in range(x, y):
        print(cat_id)
        content = extract_cat_informations(
            get_page(session, f'https://www.felidae-ev.de/stammdaten.php?id={cat_id}&type=sd'))
        content2 = extract_parent_informations(
            get_page(session, f'https://www.felidae-ev.de/stammdaten.php?id={cat_id}&type=sb'))
        content3 = extract_awards_informations(
            get_page(session, f'https://www.felidae-ev.de/stammdaten.php?l=0&id={cat_id}&type=a'))
        check_result(cat_id,content,content2,content3)
# SCRAPPING FROM
x = 199721 # LAST ID WAS 199720
# SCRAPPINT TO
y = 220000 # SET SOME BORDER
start_crawling(x,y)
