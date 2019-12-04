import json
import math
import numpy as np
import MySQLdb

from flask import Flask, render_template, request, jsonify
from stop_words import get_stop_words
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.tokenize import sent_tokenize, word_tokenize



db = MySQLdb.connect("localhost","root","root123","test")
query = "SELECT id,url,caption FROM captionimages"
with db.cursor(MySQLdb.cursors.DictCursor) as cursor:
    cursor.execute(query)
    videos = cursor.fetchall()

tfArray = []
i=0
idfArray = []
stop_words = get_stop_words('english')
recordTF_IDF_Dictionary = {}
recordTFDictionary = {}
recordIDF_Dictionary = {}

def stemSentence(sentence):
    token_words = word_tokenize(sentence)

    stem_sentence = []
    for word in token_words:
        stem_sentence.append(ps.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

def calculateIDF(word, dataVideos, recordIDF_Dictionary, tf, docId,title):
    ''', channelTitle, views,likes, dislikes):'''
    wordCountIdf = 0
    for dataVideo in dataVideos:
        titleText= dataVideo["caption"]
        titleText = stemSentence(titleText)
        wordCountIdf += titleText.count(word)
    idf = math.log10(len(videos)/wordCountIdf)
    docIDFdic = {'document_id':docId, 'idf':idf}
    docTF_IDFDict = {'document_id':docId, 'tf_idf':tf*idf, 'tf':tf, 'idf':idf, 'title':title}
    '''views':views, 'likes':likes, 'dislikes':dislikes, 'channelTitle':channelTitle}'''
    if word not in recordIDF_Dictionary:
        word_IDF_Arr = []
        word_IDF_Arr.append(docIDFdic)
        recordIDF_Dictionary.update({word: word_IDF_Arr})
        word_TF_IDF_Arr = []
        word_TF_IDF_Arr.append(docTF_IDFDict)
        recordTF_IDF_Dictionary.update({word: word_TF_IDF_Arr})
    else:
        recordIDF_Dictionary.get(word).append(docIDFdic)
        recordTF_IDF_Dictionary.get(word).append(docTF_IDFDict)
    print(recordTF_IDF_Dictionary)
    return recordIDF_Dictionary

for data in videos:
   text = data["caption"]
   caption = data["caption"]
   docId = data["id"]
   '''title = data["title"]
   channelTitle = data["channel_title"]
   views = data["views"]
   likes = data["likes"]
   dislikes = data["dislikes"]'''
   text = stemSentence(text)
   list_str = text.split()
   wordslist = list(set(list_str))
   tfDictionary = ({})
   idfDictionary = ({})


   wordCountIdf = 0

   for word in wordslist:
       word = ps.stem(word)
       if word not in stop_words:
        wordCount = text.count(word)
        totalWordCount = len(text)
        tf = wordCount / totalWordCount
        docTfdic = {'document_id' : docId, 'tf': tf}
        if word not in recordTFDictionary:
            s=[]
            s.append(docTfdic)
            recordTFDictionary.update({word:s})
        else:
            recordTFDictionary.get(word).append(docTfdic)
        recordIDF_Dictionary = calculateIDF(word, videos, recordIDF_Dictionary,tf,docId,caption)
        '''title, channelTitle, views,likes, dislikes)'''
        wordCountIdf += wordCount
       else:
           print("stop word" + word)



with open('TF-image.txt', 'w') as json_file:
  json.dump(recordTFDictionary, json_file)
with open('IDF-image.txt', 'w') as json_file:
      json.dump(recordIDF_Dictionary, json_file)
with open('TF_IDF-image.txt', 'w') as json_file:
  json.dump(recordTF_IDF_Dictionary, json_file)


db.close()
app = Flask(__name__)
@app.route('/textSearch', methods=['POST'])
def textSearch():
    if __name__ == '__main__':
        app.run()