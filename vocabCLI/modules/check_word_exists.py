import requests
import csv
import json


def check_definition_exists(word):
    time.sleep(2)
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    return response.status_code == 200
            

def check_words_exist():
    with open("domains.csv", "r") as domains_csv:
        domains_reader = csv.reader(domains_csv)
        for row in domains_reader:
            word = row[0]
            if check_definition_exists(word):
                with open("exists.csv", "a") as exists_csv:
                    exists_writer = csv.writer(exists_csv)
                    exists_writer.writerow([word])
