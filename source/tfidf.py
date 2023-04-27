import os
import math


def cal_score(path):
    ReadFile1 = open(path+r'\result\sorted_wb_final.txt', mode='r', encoding='ANSI')
    ReadFile2 = open(path+r'\result\tokensForTF_final.txt', mode='r', encoding='ANSI')
    WriteFile = open(path+r'\result\tfidf_score.txt', mode='w', encoding='ANSI')
    total_sentences_count = len(ReadFile2.readlines())
    ReadFile2.seek(0, 0)
    WBList = []
    ReadLine = ReadFile1.readline().strip()
    while ReadLine:
        word = ReadLine.split('|')[0]
        count = int(ReadLine.split('|')[1])
        WBList.append(word)
        ReadLine = ReadFile1.readline().strip()
    IDFList = [0.0 for _ in WBList]
    ReadLine = ReadFile2.readline().strip()
    while ReadLine:
        word_list = ReadLine.strip('[').strip(']').split(', ')
        word_list = [str(x.strip('\'')) for x in word_list]
        index = 0
        for item in WBList:
            if item in word_list:
                IDFList[index] += 1
            index += 1
        ReadLine = ReadFile2.readline().strip()
    for i in range(len(IDFList)):
        IDFList[i] = math.log((total_sentences_count / (IDFList[i] + 1)))
    ReadFile2.seek(0, 0)
    ReadLine = ReadFile2.readline().strip()
    while ReadLine:
        scoreVec = [0.0 for _ in WBList]
        word_list = ReadLine.strip('[').strip(']').split(', ')
        word_list = [str(x.strip('\'')) for x in word_list]
        index = 0
        for item in WBList:
            if item in word_list:
                scoreVec[index] += word_list.count(item)
            index += 1
        for i in range(len(scoreVec)):
            scoreVec[i] = scoreVec[i] / len(word_list) * IDFList[i]
        WriteFile.write(str(scoreVec) + '\n')
        ReadLine = ReadFile2.readline().strip()
    ReadFile1.close()
    ReadFile2.close()
    WriteFile.close()


if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cal_score(path)