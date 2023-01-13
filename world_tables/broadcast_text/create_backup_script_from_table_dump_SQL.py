from os import path
from os import system
import re

dirpath = path.dirname(path.abspath(__file__))

###################################
# config
target_file_name = "broadcast_text_dump.sql"
output_file_name = "broadcast_text_rollback.sql"

table_name = "broadcast_text"
table_index_column_name = "entry"
table_column_1 = "male_text"
table_column_2 = "female_text"
###################################


target_file = path.join(dirpath, target_file_name)
output_file = path.join(dirpath, output_file_name)

if not path.exists(target_file):
    print(f"'{target_file}' not found.")

if not path.exists(output_file):
    command = f"touch {output_file}"
    system(command)
    print(f"'{output_file}' was created.")

# open file
rFile = open(target_file, "r")
wFile = open(output_file, "w")

rFileLines = rFile.readlines()

for line in rFileLines:
    if line.startswith("INSERT"):
        line = re.sub(r"^INSERT.*VALUES ", "", line)
        line = re.sub(r";$", "", line)
        line = re.sub(r"^\(", "", line)
        line = re.sub(r"\)$", "", line)
        items = re.split(r"\),\(", line)
        for item in items:
            item = re.sub(r",\d+", "", item)
            item = re.sub(r",[^ ]", ",''", item)
            parts = re.split(r",'", item)
            content = (
                "UPDATE `{}` WHERE `{}`={} SET `{}`={}, `{}`={};\n".format(
                    table_name,
                    table_index_column_name,
                    parts[0],
                    table_column_1,
                    parts[1],
                    table_column_2,
                    parts[2],
                )
            )
            wFile.writelines(content)

# close file
rFile.close()
wFile.close()
