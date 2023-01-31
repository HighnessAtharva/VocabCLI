import requests
import csv
import time
import json


def check_definition_exists(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    return response.status_code == 200
            
counter=0
exists_count=0
missing_count=0

with open("domains.csv", "r") as domains_csv:
    domains_reader = csv.reader(domains_csv)
    with open("no_defs.csv", "w", newline="") as exists_csv:
        for row in domains_reader:
            word = row[0]
            if not check_definition_exists(word):         
                exists_writer = csv.writer(exists_csv)
                exists_writer.writerow([word])
                print(f"{word} does not exist ❌")
            else:
                print(f"{word} exists ✅")
                
            counter+=1
            print(f"Total words processed: {counter}")