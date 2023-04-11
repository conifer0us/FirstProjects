from google_trans_new import google_translator
import random
import os
import requests
import json 
 
subreddit = 'tifu'
count = 1
timeframe = 'day' #hour, day, week, month, year, all
listing = 'random'

title = [0]
url = [0]
content =[0]
def get_reddit(subreddit,count):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?count={count}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
        exit()
    return request.json()
def getpost():
    top_post = get_reddit(subreddit,count)
    title[0] = top_post[0]['data']['children'][0]['data']['title']
    url[0] = top_post[0]['data']['children'][0]['data']['url']
    content[0] = top_post[0]['data']['children'][0]['data']['selftext']
    if len(content) > 4990:
        getpost()
getpost()
title = title[0]
content=content[0]
print(f'{title}\n{content}')
translator = google_translator()
language_codes = ['af','sq','am','ar','hy','az','eu','be','bn','bs','bg','ca','ceb','ny','zh-cn','zh-tw','co','hr','cs','da','nl','en','eo','et','tl','fi','fr','fy','gl','ka','de','el','gu','ht','ha','haw','iw','he','hi','hmn','hu','is','ig','id','ga','it','ja','jw','kn','kk','km','ko','ku','ky','lo','la','lv','lt','lb','mk','mg','ms','ml','mt','mi','mr','mn','my','ne','no','or','ps','fa','pl','pt','pa','ro','ru','sm','gd','sr','st','sn', 'sd','si','sk','sl','so','es','su','sw','sv','tg','ta','te','th','tr','uk','ur','ug','uz','vi','cy','xh','yi','yo', 'zu']
# file = open("texttotranslate.txt")
# texttotranslate = file.read().replace('\n','')
# file.close()
texttotranslate = content
texttotranslate.encode('utf-16')
translateto = random.choice(language_codes)
texttotranslate = translator.translate(texttotranslate, lang_tgt=translateto)
for i in range(30):
    translatefrom = translateto
    translateto = random.choice(language_codes)
    texttotranslate = translator.translate(texttotranslate, lang_tgt=translateto, lang_src=translatefrom)
translatefrom = translateto
texttotranslate = translator.translate(texttotranslate, lang_src = translatefrom, lang_tgt='en')
texttotranslate = title + '\n\n' +texttotranslate
text_file = open("translatedtext.txt", "w")
text_file.write(texttotranslate)
text_file.close()
print('\n\nOpening translated reddit post!')
os.popen('translatedtext.txt')