from __future__ import print_function
from pprint import pprint
from difflib import SequenceMatcher
import operator
import codecs
import sys
import json

mappingTable = None
mappingRotates = [114, 174]

totalWrong = 0
totalChars = 0
logFile = None
debug = False


def log(msg):
	print(msg)
	print(msg, file=logFile)


def strord(str):
	return map(ord, str)

def arrchr(arr):
	return "".join(map(unichr,arr))

def arrdot(arr):
	return ".".join(map(str,arr))

def dotarr(chrs):
	return map(int, chrs.split("."))

def utfstr(arrs):
	strarr = [" ".join(map(arrchr, arr)) for arr in arrs]
	return "\n".join(strarr)

# inputs are strord mapped array of arrays
def utfdebug(arrs):
	for arr in arrs:
		assert (len(arr) == len(arrs[0]))

	strarr = [""] * len(arrs)

	for i in xrange(len(arr)):
		wordarr = []
		for arr in arrs:
			word = ""

			for dec in arr[i]:
				word += "'" + unichr(dec) + "'" + str(dec) + " "

			wordarr.append(word +  "(" + str(len(arr[i])) + ")")

		maxLen = max([len(word) for word in wordarr])
		for j, word in enumerate(wordarr):
			strarr[j] += wordarr[j]
			strarr[j] += " " * (maxLen - len(word))
			strarr[j] += "  |  "

	return "\n".join(strarr)

def applyMap(srcArr):
	transArr = []
	lookAhead = 3
	numLetters = len(srcArr)

	start = 0
	while start < numLetters:
		for j in [3, 2, 1]:#reversed(xrange(1, 1 + lookAhead)):
			end = min(start + j, numLetters)
			src = arrdot(srcArr[start : end])

			if src in mappingTable:
				trans = max(mappingTable[src].iteritems(), key=operator.itemgetter(1))[0]
				transArr.extend(dotarr(trans))
				#if debug: print("applyMap", src, trans)
				start = end - 1
				break
			elif (end - start) == 1:
				#if debug: print("applyMap", dotarr(src))
				transArr.extend(dotarr(src))
				break;

		start += 1
	#if debug: print("end", srcArr, transArr,"\n");
	return transArr


def applyRotate(srcArr):
	i = 0
	while i < len(srcArr) -1 :
		if srcArr[i] in mappingRotates:
			srcArr[i], srcArr[i + 1] = srcArr[i + 1], srcArr[i]
			i += 1
		i += 1
	return srcArr

def addMapping(src, dst):
	global mappingTable

	#print(src, dst)
	if src in mappingTable:
		if dst in mappingTable[src]:
			mappingTable[src][dst] += 1
		else:
			mappingTable[src][dst] = 1
	else:
		mappingTable[src] = {dst: 1}

	#print("addMapping", src, dst, mappingTable[src])


def mapDirect(tple):
	srcArr, destArr = tple
	#print("mapDirect", srcArr, destArr)

	if len(srcArr) == len(destArr):
		for i in xrange(len(srcArr)):
			addMapping(str(srcArr[i]), str(destArr[i]))


def mapDiff(tple):
	srcArr, destArr, transArr = tple
	opcodes = SequenceMatcher(None, transArr, destArr).get_opcodes()

	#print("opcodes", opcodes)

	for op in opcodes:
		src = srcArr[op[1]:op[2]]
		trans = transArr[op[1]:op[2]]
		dest = destArr[op[3]:op[4]]

		if op[0] == 'replace':
			#print("replace", src, trans, dest)

			if (op[2] - op[1]) == (op[4] - op[3]): #same length
				mapDirect((src, dest))
			else:
				addMapping(arrdot(trans), arrdot(dest))

		# 	print("\nreplace", utfdebug([[srcArr],[destArr],[transArr]]))
		# 	print(op, src, trans, dest)

		# elif op[0] == 'delete':
		# 	print("\ndelete", utfdebug([[srcArr],[destArr],[transArr]]))
		# 	print(op, src, trans, dest)

		# elif op[0] == 'insert':
		# 	print("\ninsert", utfdebug([[srcArr],[destArr],[transArr]]))
		# 	print(op, src, trans, dest)


def getScore(tple):
	global totalChars, totalWrong
	res = []
	truthArr, transArr = tple

	for i in xrange(len(truthArr)):
		totalChars += 1

		if i < len(transArr):
			if truthArr[i] == transArr[i]:
				res.append(2798) #right
				continue

		res.append(2790) #wrong
		totalWrong += 1

	return res


def trainTranslator(srcPath, destPath, mappingPath):
	global mappingTable

	mappingTable = json.loads(open(mappingPath,'r').read().replace("'","\""))
	srcLines = map(unicode.strip, open(srcPath,'r').read().strip().decode('utf-8').split("\n"))
	destLines = map(unicode.strip, open(destPath,'r').read().strip().decode('utf-8').split("\n"))

	numLines = len(srcLines)
	srcLines = srcLines[0:numLines]
	destLines = destLines[0:numLines]

	assert(len(srcLines) == len(destLines))
	lineCount = len(srcLines)
	trans1Lines = [[]] * lineCount
	transLines = [[]] * lineCount
	scoreLines = [[]] * lineCount


	# compute direct mappings
	for i in xrange(lineCount):
		#log("\n" + str(i))
		srcLines[i] = map(strord,srcLines[i].split())
		destLines[i] = map(strord, destLines[i].split())
		srcLines[i] = map(applyRotate, srcLines[i])

		# if len(srcLines[i]) != len(destLines[i]):
		# 	print(i+1, "length", len(srcLines[i]), len(destLines[i]))
		# 	continue

		assert(len(srcLines[i]) == len(destLines[i]))

		debug = (True if i == 4 else False)
		trans1Lines[i] = map(applyMap, srcLines[i])
		map(mapDiff, zip(srcLines[i], destLines[i], trans1Lines[i]))


	for i in xrange(lineCount):
		log("\n" + str(i))

		transLines[i] = map(applyMap, srcLines[i])
		scoreLines[i] = map(getScore, zip(destLines[i], transLines[i]))

		if unichr(2790) in utfstr([scoreLines[i]]): #only error lines
			log(utfstr([srcLines[i], destLines[i], trans1Lines[i], transLines[i], scoreLines[i]]))
			log(utfdebug([srcLines[i], destLines[i], trans1Lines[i], transLines[i], scoreLines[i]]))

		#return

	pprint(mappingTable)
	pprint(mappingTable, logFile)

	log("Score: " + str(100 - (totalWrong * 100.0 /totalChars)))


def applyTranslator(srcPath, destPath, mappingPath):
	global mappingTable

	mappingTable = json.loads(open(mappingPath,'r').read().replace("'","\""))
	srcLines = map(unicode.strip, open(srcPath,'r').read().strip().decode('utf-8').split("\n"))
	destFile = codecs.open(destPath, 'w', 'utf-8')
	lineCount = len(srcLines)

	for i in xrange(lineCount):
		srcLines[i] = map(strord,srcLines[i].split())
		srcLines[i] = map(applyRotate, srcLines[i])
		transLine = map(applyMap, srcLines[i])

		log("\n" + str(i))
		print(utfstr([transLine]))
		print(utfstr([transLine]), file=destFile)
		log(utfstr([srcLines[i], transLine]))
		log(utfdebug([srcLines[i], transLine]))

if __name__ == '__main__':
	logFile = codecs.open('data/out.txt', 'w', 'utf-8')
	#trainTranslator('data/train-font.txt', 'data/train-guj.txt', 'mapping.json')
	trainTranslator('data/ekadashi-font.txt', 'data/ekadashi-guj-src.txt', 'mapping.json')

	#applyTranslator('data/hajari-font.txt', 'data/hajari-guj.txt', 'mapping.json')
	#applyTranslator('data/kirtanavali_font.txt', 'data/kirtanavali-guj.txt', 'mapping.json')
	#applyTranslator('data/ekadashi-font.txt', 'data/ekadashi-guj.txt', 'mapping.json')

