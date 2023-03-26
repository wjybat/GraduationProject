import string

import hanlp
import os
import re

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    condition={'tok':False,'words_bag':True,'ner':False,'test':False}

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
                            '》', '——','、','—','（','）'])
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

