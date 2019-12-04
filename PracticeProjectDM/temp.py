import re
from collections import defaultdict
import MySQLdb
from stop_words import get_stop_words

db = MySQLdb.connect("localhost","root","root123","test")
freqOfClass = "select category_id,title,count(*) AS classFrequency from cavideos group by category_id;"
with db.cursor(MySQLdb.cursors.DictCursor) as cursor:
    cursor.execute(freqOfClass)
    allCategInfo = cursor.fetchall()

allData = "SELECT video_id,channel_title,category_id,title,likes,dislikes,views,description,thumbnail_link FROM cavideos"
with db.cursor(MySQLdb.cursors.DictCursor) as cursor:
    cursor.execute(allData)
    allDataResult = cursor.fetchall()

arrDictOfProbabilityClass = []
arrDictOfWordsCountOfClass = []


for video in allCategInfo:
    dictClassProbability = {}
    dictClassWordsCount = {}
    counter = 0
    dictClassProbability.update(categoryId = video.get('category_id'), classProbability = video.get('classFrequency')/ len(allDataResult))
    arrDictOfProbabilityClass.append(dictClassProbability)
    for data in allDataResult:
        if(video.get('category_id') == data.get('category_id')):
            temp = video.get('title').split(' ')
            counter = counter + len(temp)
    dictClassWordsCount.update(category_id = video.get('category_id'), countOfwords = counter)
    arrDictOfWordsCountOfClass.append(dictClassWordsCount)


#print(arrDictOfWordsCountOfClass)
def CountFrequency(my_list):
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return freq


searchText = "hand"
arrWordList = []
stop_words = get_stop_words('english')
finalListwithCatId = {}
index = 0
for videodata in allDataResult:
    for word in videodata.get("title").split():
       word = re.sub("[^\w\s]", " ",word)
       if word not in stop_words:
           dictWordCategoryInfo={}
           dictWordCategoryInfo [word] = videodata.get("category_id")
           arrWordList.append(dictWordCategoryInfo)

mergedWordCategDict = defaultdict(list)
finalMergedWordCategDict = {}

for d in arrWordList:  # you can list as many input dicts as you want here
    for key, value in d.items():
        mergedWordCategDict[key].append(value)

for k,v in mergedWordCategDict.items():
    if not (k==' '):
        wordFreqCount = CountFrequency(v)
        finalMergedWordCategDict[k] = wordFreqCount
countOfUniqueWords = len(finalMergedWordCategDict)


fullTextToBeSearched = "hand walk"
tempdict = {}
dictProbabilityResult = {}
probabilityOfSearchedText = {}
arrFullTextToBeSearched = fullTextToBeSearched.lower().split(' ')
#print(arrFullTextToBeSearched)
for i in arrFullTextToBeSearched:

    try:
        #print("textToBeSearched")
        #print(i)
        for textWord in finalMergedWordCategDict:
            if (textWord.lower() == i):
                tempdict = finalMergedWordCategDict.get(textWord)
                #print("tempdict")
                #print(tempdict)
        for category in [o['category_id'] for o in allCategInfo]:
            #print(category)
            for categoryWordCount in arrDictOfWordsCountOfClass:
                tempWordCount = 0
                #print(categoryWordCount)
                if (categoryWordCount.get('category_id') == category):
                    tempWordCount = categoryWordCount.get('countOfwords')
                    if not(category in tempdict.keys()):
                        categoryFrequency = 0
                    else:
                        categoryFrequency = tempdict.get(category)
            probabilityForCAtegory = (categoryFrequency + 1) / (tempWordCount + countOfUniqueWords)
            categoryProbabilityDict = {category: probabilityForCAtegory}
            dictProbabilityResult.update(categoryProbabilityDict)
            probabilityOfSearchedText[i] = dictProbabilityResult
    except:
        print("fail")
print(probabilityOfSearchedText)

productOfProbOfSearchedText = {1: 1, 2: 1, 10: 1, 15: 1, 17: 1, 19: 1, 20: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 43: 1}
for searchedText in probabilityOfSearchedText:
    for category in allCategInfo:
        #print(productOfProbOfSearchedText[category.get('category_id')])
        #print(probabilityOfSearchedText.get(searchedText).get(category.get('category_id')))
        temp = (productOfProbOfSearchedText[category.get('category_id')])* (probabilityOfSearchedText.get(searchedText).get(category.get('category_id')))
        productOfProbOfSearchedText[category.get('category_id')] = temp
        #print(productOfProbOfSearchedText[category.get('category_id')])






dictProbabilityTochooseCategory = {}
for category in allCategInfo:
    for probOfClass in arrDictOfProbabilityClass:
        print("categoryProbabilityDict")
        print(probOfClass)
        if(category.get('category_id') == probOfClass.get('categoryId')):
            probabilityTochooseCategory = probOfClass.get('classProbability')*productOfProbOfSearchedText.get(category.get('category_id'))
            dictProbabilityTochooseCategory[probOfClass.get('categoryId')] = probabilityTochooseCategory
print(dictProbabilityTochooseCategory)
result = []
resultPercentArr = []

result =sorted(dictProbabilityTochooseCategory.values(),reverse= True)
topThreeResult = (result[0:3])
print(topThreeResult)
sum = sum(topThreeResult)
for k in topThreeResult:
    pct = k * 100.0 / sum
    resultPercentArr.append(pct)
print(resultPercentArr)


'''s = sum(result.v)
for k, v in result.items():
    pct = v * 100.0 / s
    print(k, pct)'''

