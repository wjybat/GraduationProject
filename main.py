import math
import string

import hanlp
import os
import re

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    condition={'tok':False,'words_bag':False,'sort':False,'sentencing':False,'TF':False,'KMeans':True,'ner':False,'test':False}

    if condition['test']:
        HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
        # tok=HanLP['tok/coarse']
        print(HanLP(['预防为主，以人为本。坚持人民至上、生命至上，把保障人民群众生命财产安全作为工作的出发点和落脚点，建立健全群测群防机制，'
                     '最大程度减少突发地质灾害造成的损失。'],tasks='tok/coarse').pretty_print)
        # print(re.search('www', 'www.runoob.com').group())
        print(string.punctuation)

    if condition['tok']:
        HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
        ResFile=open('resTOKpretty.txt',mode='w')
        with open('天津市突发地质灾害应急预案.txt',mode='r') as OriFile:
            line = OriFile.readline()
            while line:
                if line.strip()!='':
                    res_list=HanLP(line.strip(),tasks='tok/coarse')['tok/coarse']
                    exclude=list(string.punctuation)
                    exclude.extend([ '，', '。', '：', '”', '’', '？', '；', '《',
                            '》', '——','、','—','（','）','〔','〕','．'])
                    for item in res_list:
                        if item not in exclude and re.match(r'.*\d+.*',item) is None and \
                                re.match(r'[一二三四五六七八九十]+',item) is None and \
                                re.match(r'[ⅠⅡⅢⅣⅤⅥⅦⅧⅨ]+',item) is None:
                            ResFile.write(str(item)+'\n')
                line = OriFile.readline()
            OriFile.close()
        ResFile.close()

    if condition['words_bag']:
        WriteFile=open('resWb1.txt',mode='r+',encoding='ANSI')
        ReadFile=open('resTOKpretty1.txt',mode='r',encoding='ANSI')
        ReadLine=ReadFile.readline().strip()
        while ReadLine:
            WriteFile.seek(0,0)
            WriteLine=WriteFile.readline().strip()
            count=0
            has=False
            line_num=1
            last_pos=0
            while WriteLine:
                word=WriteLine.split('|')[0]
                count=int(WriteLine.split('|')[1])
                if word==ReadLine:
                    count+=1
                    has=True
                    break
                else:
                    last_pos=WriteFile.tell()
                    WriteLine=WriteFile.readline().strip()
                    line_num+=1
            if has:
                WriteFile.seek(last_pos,0)
                WriteFile.write('%s|%05d\n' %(word,count))
            else:
                count=1
                WriteFile.seek(0,2)
                WriteFile.write('%s|%05d\n' %(ReadLine,count))
            ReadLine = ReadFile.readline().strip()
        ReadFile.close()
        WriteFile.close()

    if condition['sort']:
        ReadFile=open('resWb1.txt',mode='r+',encoding='ANSI')
        WriteFile = open('sortedWordBags.txt', mode='w', encoding='ANSI')
        total_lines_count=len(ReadFile.readlines())
        print(total_lines_count)
        ReadFile.seek(0,0)
        cur_line=0
        while cur_line<total_lines_count:
            MaxCount = 0
            change_word = ''
            change_pos = 0
            last_pos = 0
            ReadLine = ReadFile.readline().strip()
            while ReadLine:
                word = ReadLine.split('|')[0]
                count = int(ReadLine.split('|')[1])
                if count>MaxCount:
                    change_word=word
                    MaxCount=count
                    change_pos=last_pos
                last_pos=ReadFile.tell()
                ReadLine = ReadFile.readline().strip()
            WriteFile.write('%s|%05d\n' %(change_word,MaxCount))
            ReadFile.seek(change_pos,0)
            ReadFile.write('%s|%05d\n' %(change_word,0))
            ReadFile.seek(0,0)
            cur_line+=1
        ReadFile.close()
        WriteFile.close()

    if condition['sentencing']:
        HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
        ReadFile=open('天津市突发地质灾害应急预案.txt',mode='r',encoding='ANSI')
        WriteFile=open('分句.txt',mode='w',encoding='ANSI')
        ResFile=open('tokenForTF.txt',mode='w',encoding='ANSI')
        ReadLine=ReadFile.readline()
        while ReadLine:
            if ReadLine.strip().find('。')!=-1:
                Sentences=ReadLine.strip().split('。')
                for sentence in Sentences:
                    if sentence!='':
                        WriteFile.write(sentence+'\n')
                        init_list = HanLP(sentence, tasks='tok/coarse')['tok/coarse']
                        res_list=[]
                        exclude = list(string.punctuation)
                        exclude.extend(['，', '。', '：', '”', '’', '？', '；', '《',
                                        '》', '——', '、', '—', '（', '）', '〔', '〕', '．'])
                        for item in init_list:
                            if item not in exclude and re.match(r'.*\d+.*', item) is None and \
                                    re.match(r'[一二三四五六七八九十]+', item) is None and \
                                    re.match(r'[ⅠⅡⅢⅣⅤⅥⅦⅧⅨ]+', item) is None:
                                res_list.append(item)
                        ResFile.write(str(res_list)+'\n')
            ReadLine=ReadFile.readline()
        ReadFile.close()
        WriteFile.close()
        ResFile.close()

    if condition['TF']:
        ReadFile1 = open('sortedWordBags.txt', mode='r', encoding='ANSI')
        ReadFile2 = open('tokenForTF.txt', mode='r', encoding='ANSI')
        WriteFile=open('TFIDFScore.txt',mode='w',encoding='ANSI')
        total_sentences_count = len(ReadFile2.readlines())
        ReadFile2.seek(0, 0)
        WBList=[]
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
                    IDFList[index]+=1
                index+=1
            ReadLine = ReadFile2.readline().strip()
        for i in range(len(IDFList)):
            IDFList[i]=math.log((total_sentences_count/(IDFList[i]+1)))
        ReadFile2.seek(0,0)
        ReadLine=ReadFile2.readline().strip()
        while ReadLine:
            scoreVec = [0.0 for _ in WBList]
            word_list = ReadLine.strip('[').strip(']').split(', ')
            word_list = [str(x.strip('\'')) for x in word_list]
            index=0
            for item in WBList:
                if item in word_list:
                    scoreVec[index]+=word_list.count(item)
                index+=1
            for i in range(len(scoreVec)):
                scoreVec[i]=scoreVec[i]/len(word_list)*IDFList[i]
            WriteFile.write(str(scoreVec)+'\n')
            ReadLine = ReadFile2.readline().strip()
        ReadFile1.close()
        ReadFile2.close()
        WriteFile.close()

    if condition['KMeans']:
        k=9
        ReadFile = open('TFIDFScore.txt', mode='r', encoding='ANSI')
        total_sentences_count = len(ReadFile.readlines())
        ReadFile.seek(0,0)
        gap=total_sentences_count//(k-1)
        cores=[]
        scores=ReadFile.readlines()
        for index in range(len(scores)):
            scores[index]=scores[index].strip().strip('[').strip(']').split(', ')
            scores[index]=list(map(float,scores[index]))
        cores.append(scores[0])
        for i in range(1,k-1):
            cores.append(scores[i*gap])
        cores.append(scores[-1])
        catalog=[-1 for _ in scores]
        ReadFile.seek(0,0)
        def eula_dist(a,b):
            if len(a)!=len(b):
                print('wrong dimension!')
                exit(0)
            distance=0.0
            for serial in range(len(a)):
                distance+=(a[serial]-b[serial])**2
            return distance
        changed=True
        times=10000
        while times>0 and changed:
            changed=False
            index_score=0
            for score in scores:
                nearest_dist=math.inf
                nearest_core=-1
                index_core=0
                for core in cores:
                    dist=eula_dist(score,core)
                    if dist<nearest_dist:
                        nearest_dist=dist
                        nearest_core=index_core
                    index_core+=1
                catalog[index_score]=nearest_core
                index_score+=1
            for num in range(len(cores)):
                mean=[0.0 for _ in range(len(cores[0]))]
                count=0
                cat_index=0
                for item in catalog:
                    if item==num:
                        mean=[mean[i]+scores[cat_index][i] for i in range(len(mean))]
                        count+=1
                    cat_index+=1
                if count>0:
                    mean=[mean[i]/count for i in range(len(mean)) ]
                if cores[num]!=mean:
                    cores[num]=mean
                    changed=True
            times-=1
        ReadFile1 = open('分句.txt', mode='r', encoding='ANSI')
        sentences=ReadFile1.readlines()
        WriteFile=open('cluster.txt', mode='w', encoding='ANSI')
        for num in range(len(cores)):
            cat_index=0
            for core_num in catalog:
                if core_num==num:
                    WriteFile.write(sentences[cat_index])
                cat_index+=1
            WriteFile.write('\n')
        ReadFile.close()
        ReadFile1.close()
        WriteFile.close()
        print(times)

    if condition['ner']:
        HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
        ResFile=open('resNER.txt',mode='w')
        with open('天津市突发地质灾害应急预案.txt',mode='r') as OriFile:
            line = OriFile.readline()
            while line:
                if line.strip()!='':
                    ResFile.write(str(HanLP(line.strip())["ner/msra"])+'\n')
                line = OriFile.readline()
            OriFile.close()
        ResFile.close()

