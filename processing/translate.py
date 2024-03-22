############# ref https://github.com/andrikosrikos/Google-Cloud-Support/blob/master/Google%20Translate%20API

import csv

# Imports the Google Cloud client library
from google.cloud import translate_v2 as translate

# Instantiates a client
translate_client = translate.Client()

#Translating the text to specified target language
def translate(text, lang):
  # Translates some text into 'lang'
  translation = translate_client.translate(
    text,
    target_language=lang)

  return (translation)


def has_numbers(inputString):
  return any(char.isdigit() for char in inputString)
  
def translateCSV(path, lang):
  to_translate = []
  
  with open("../data/original/"+path, newline='', encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    data_file = []
    for row in reader:
      data_file.append(list(map(lambda s: s.replace('\t', ''),row[:-1])))
      for entry in row[:-1]:
        e = entry.replace('\t', '')
        if e not in to_translate and has_numbers(e) == False:
          to_translate.append(e)
  
  # print(to_translate)
  
  res = translate(to_translate,lang)
  
  translate_dict = {}
  
  for obj in res:
    translate_dict[obj["input"]] = obj["translatedText"]
  
  print("-- TRANSLATION --")
  for key, value in translate_dict.items():
    print(" ",str(key),": ",str(value))
  
  data = data_file
  len_data = len(data)

  translated = []
  for index, row in enumerate(data):
    tr = []
    for entry in row:
      if entry in translate_dict:
        tr.append(translate_dict[entry])
      else:
        tr.append(entry)
    translated.append(tr)
  
  with open("../data/translated/"+path, 'w', newline='') as file:
    writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerows(translated)

# translate data/original/asia-export.csv to English
# save translation in data/translated/asia-export.csv
translateCSV('asia-export.csv','en')