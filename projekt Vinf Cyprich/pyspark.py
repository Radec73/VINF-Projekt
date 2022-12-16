import os
import time
from transformations import transform_parent_id, transform_parent_name, change_date_format, get_lines, \
    get_breed, transform_to_final_format, map_ids, breeds_dict
from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# REPLACE TRANSFORMED COLUMS BY NEW VALUES
def replace_columns(lines, result):
    count = 1
    transformed = []
    for a in lines:
        rec = a.replace(';', '').split('|')
        rec[0] = str(count)
        rec[8] = result[count - 1][0]
        rec[10] = result[count - 1][1]
        rec[17] = result[count - 1][2]
        rec[18] = result[count - 1][3]
        rec[19] = result[count - 1][4]
        rec[20] = result[count - 1][5]
        transformed.append(rec)
        count += 1
    return transformed


# ENV INIT
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
# SPARK INIT
spark = SparkSession.builder.master("local[*]").appName("Catabase").getOrCreate()
# READER
records = spark.read.option("delimiter", "|").csv("catsCRAWLED.txt", header=False)
# ID PAIRS FROM TRANSFORM MODULE
lines = get_lines()
pairs = map_ids(lines)
# MEASURING TIME OF MAP FUNCTION
start = time.time()
# TRANSFORMATION OF ATTRIBUTES IN RDD FORMAT
rdd0 = records.rdd.map(lambda row: (get_breed(row[8], breeds_dict),
                                    change_date_format(row[10]),
                                    transform_parent_id(row[17], pairs),
                                    transform_parent_id(row[18], pairs),
                                    transform_parent_name(row[19]),
                                    transform_parent_name(row[20])))

result = rdd0.collect()
end = time.time()
#TIME TAKEN OF MAPPING ATTRIBUTES
print("Mapping time taken: " + str(end - start) + " seconds")

# dataframe = rdd0.toDF()
# dataframe.show()
#CALL FUNCTION TO REPLACE COLUMNS IN DATASET
lines = replace_columns(lines, result)

file = open('catsSPARK.txt', 'a', encoding="utf-8")
file.write(
    'ID|NAME|SOURCE_DB|SOURCE_ID|REGISTRATION_NUMBER_BEFORE|REGISTRATION_NUMBER_CURRENT|ORIGIN_COUNTRY|CURRENT_COUNTRY|TITLE_BEFORE|TITLE_AFTER|BREED|COLOR_CODE|COLOR|BIRTH_DATE|GENDER|CHIP|NOTE(DESCRIPTION)|AWARDS|HEALTH_STATUS|CATTERY|MOTHER_ID|FATHER_ID|MOTHER_NAME|FATHER_NAME|MOTHER_REG_NUMBER|FATHER_REG_NUMBER;\n')
count = 0
for x in lines:
    # CORRECTIONS ADDING SOME NEW COLUMNS ACCORDING TO OUR SCHEMA
    x.insert(6, None)
    x.insert(7, None)
    x.insert(12, None)
    write_result = transform_to_final_format(x)
    file = open('catsSPARK.txt', 'a', encoding="utf-8")
    file.write(write_result)
    count += 1
file.close()
