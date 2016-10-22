import glob
import re
import time
from time import sleep
from Levenshtein import ratio
#from difflib import SequenceMatcher

startTime = float(time.time())

def isSimilar(a, b):
    return ratio(a,b)
    #return SequenceMatcher(None, a, b).ratio()

def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

def getFiles(path):
    files = []
    names = []
    output = []
    rawFiles = glob.glob(path+"*.txt")
    for thing in rawFiles:
        f = open(thing, "r").read()
        files.append(f)
        if thing.rfind('\\') != -1:
            name = thing[int(thing.rfind('\\'))+1:]
        elif thing.rfind('/'):
            name = thing[int(thing.rfind('/'))+1:]
        else:
            name = thing
        names.append(name)
    output.append(names)
    output.append(files)
    return output

#Gets the essay text into propper format 
raw = getFiles("../essays/Examined/")
rawNames = raw[0]
rawEssays = raw[1]
essays = []

#Splits the essays up into a usable dictionary array
for i in range(len(rawEssays)):
    essayInfo = {}
    essayInfo['name'] = rawNames[i]
    essayInfo['raw'] = rawEssays[i]
    essayInfo['sentences'] = []
    rawParagraphs  = rawEssays[i].split("\n")
    tempParagraphs = []
    sentences = []
    for paragraph in rawParagraphs:
        if len(paragraph.split(" ")) > 20:
            tempParagraphs.append(paragraph)
    for paragraph in tempParagraphs:
        rawSentences = re.split('\. |\? |! ',paragraph)
        tempsentences = []
        for sentence in rawSentences:
            sentence = sentence.strip()
            words = int(len(sentence.split(" ")))
            if words > 5:
                essayInfo['sentences'].append(sentence)
    essays.append(essayInfo)

howMany = 0
perc = 0.0

def scan(chunker):
    global howMany
    for chunky in chunker:
        howMany += 1
        perc = float(float(howMany) / float(len(chunker)))
        print perc
        for essay in essays:
            copys = []
            counter = 0
            for chunkySentence in chunky['sentences']:
                for essaySentence in essay['sentences']:
                    if chunkySentence != essaySentence:
                        if isSimilar(chunkySentence, essaySentence) > 0.7:
                            essays[howMany-1]['counts'] = counter
                            essays[howMany-1]['copies'] = {'name':essay['name'], 'sentence': [chunkySentence, essaySentence]}
                            counter += 1
                            copys.append(chunkySentence)
                            copys.append(essaySentence)


looper = essays
scan(looper)

counts = []

for essay in looper:
    if "counts" in essay:
        counts.append(float(essay['counts']))
countMed = median(counts)

print countMed
open('temp.txt', 'w').close()

f = open('temp.txt', 'w')
f.write
f.write(":::RED:::")
f.close()


print "TIME:::::: "+str(float(time.time()) - startTime)
"""for i in range(len(essays)):
    for n in range(len(essays)):
        counter = 0
        copycats = []
        if n != i:
            for isentence in essays[i]['sentences']:
                for nsentence in essays[n]['sentences']:
                    if isSimilar(isentence, nsentence) > 0.6:
                        counter += 1
                        copycats.append([isentence,nsentence])
        if counter >= 1:
            print "Alert!! {} and {} are flagged {} times, here are the setences:".format(essays[i]['name'], essays[n]['name'], counter)
            for copycat in copycats:
                print copycat[0]
                print copycat[1]

            print "\n\n"
"""
