# from easynmt import EasyNMT
# # model_name = "m2m_100_418M"
# model_name = "mbart50_m2m"
# model = EasyNMT(model_name)

# def translate(src, trg, src_text):
#     translations = model.translate(src_text, source_lang=src, target_lang=trg)
#     return translations

import requests

url = "http://37bf2f78b40c.ngrok.io/translate"

def translate(src, trg, src_text):
  payload={'src': src,
  'dest': trg,
  'text': src_text}

  headers = {}
  response = requests.request("POST", url, headers=headers, data=payload)
  res = response.text#.encode('ascii').decode('unicode-escape')
  return res