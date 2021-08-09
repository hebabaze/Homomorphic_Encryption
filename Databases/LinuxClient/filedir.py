import os

# List all files in a directory using os.listdir
basepath = '/home/usor/PFE/'
for entry in os.listdir(basepath):
    if entry.endswith('.json'):
        print(entry)
