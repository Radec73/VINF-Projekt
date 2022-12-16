# THIS SCRIPT WAS MADE BY BC. MATEJ DELINCAK AS A MASTER OF DATABASE, ITS SCHEMA AND OTHER FEATURES
# SCRIPT WAS DEVELOPED FOR MERGING CRAWLED DATABASES NEEDED FOR TEAM PROJECT AND MODIFIED BY RADOVAN CYPRICH
import pathlib
import pandas


data = []
count = 0
current_batch = 0

for file in pathlib.Path('./data').glob('*.csv'):
    current_batch = count
    df = pandas.read_csv(file, encoding="utf-8",
                         delimiter='|',
                         header=0,
                         lineterminator=';',
                         dtype={'SOURCE_ID': 'Int32', 'FATHER_ID': 'Int32', 'MOTHER_ID': 'Int32'})
    print(f"Batch {file} start")
    for index, row in df.iterrows():
        if str(row['ID']).count('\r\n') == 1:
            row['ID'] = row['ID'].replace('\r\n', '')
        if str(row['ID']).count('\n') == 1:
            row['ID'] = row['ID'].replace('\n', '')
        if len(str(row['ID'])) == 0:
            continue
        row['ID'] = int(row['ID']) + current_batch
        if not pandas.isnull(row["FATHER_ID"]):
            row['FATHER_ID'] = int(row['FATHER_ID']) + current_batch
        if not pandas.isnull(row["MOTHER_ID"]):
            row['MOTHER_ID'] = int(row['MOTHER_ID']) + current_batch
        if 'CURRENT_COUNTRY' not in row:
            row['CURRENT_COUNTRY'] = None
        if 'ORIGIN_COUNTRY' not in row:
            row['ORIGIN_COUNTRY'] = None
        data.append(row)
        count += 1
        if count % 10000 == 0:
            print(count, end=' ')

    print('')
    print(f"Batch {file} done")


cols = ['ID', 'NAME', 'SOURCE_DB', 'SOURCE_ID', 'REGISTRATION_NUMBER_BEFORE', 'REGISTRATION_NUMBER_CURRENT', 'ORIGIN_COUNTRY', 'CURRENT_COUNTRY', 'TITLE_BEFORE', 'TITLE_AFTER', 'BREED', 'COLOR', 'COLOR_CODE', 'BIRTH_DATE',
        'GENDER', 'CHIP', 'NOTE(DESCRIPTION)', 'AWARDS', 'HEALTH_STATUS', 'CATTERY', 'MOTHER_ID', 'FATHER_ID', 'MOTHER_NAME', 'FATHER_NAME', 'MOTHER_REG_NUMBER', 'FATHER_REG_NUMBER']
df = pandas.DataFrame(data)
df = df[cols]
df.to_csv('all_cats.txt', index=False, float_format='%g',
          header=True, encoding='utf-8', sep='|', line_terminator=';\r\n')
