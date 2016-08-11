import os
import yaml

table_name_file = os.environ["TABLE_NAME_FILE"]
with open(table_name_file,'r') as stream:
    table_name_dict =  yaml.load(stream)
os.environ.update(table_name_dict)
print os.environ
print "success"