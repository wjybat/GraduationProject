import string

import hanlp
import os
import re

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
    condition={'tok':False,'words_bag':False,'ner':False,'test':True}

    if condition['test']:
        # tok=HanLP['tok/coarse']
        print(HanLP(['预防为主，以人为本。坚持人民至上、生命至上，把保障人民群众生命财产安全作为工作的出发点和落脚点，建立健全群测群防机制，'
                     '最大程度减少突发地质灾害造成的损失。'],tasks='tok/coarse'))
        # print(re.search('www', 'www.runoob.com').group())
        print(string.punctuation)

    if condition['tok']:
        ResFile=open('resTOK.txt',mode='w')
        tok=HanLP['tok/coarse']
        with open('天津市突发地质灾害应急预案.txt',mode='r') as OriFile:
            line = OriFile.readline()
            while line:
                if line.strip()!='':
                    ResFile.write(str(HanLP(line.strip(),tasks='tok/coarse'))+'\n')
                line = OriFile.readline()
            OriFile.close()
        ResFile.close()

    if condition['words_bag']:
        ResFile=open('resTOK.txt',mode='w')
        tok=HanLP['tok/coarse']
        with open('天津市突发地质灾害应急预案.txt',mode='r') as OriFile:
            line = OriFile.readline()
            while line:
                if line.strip()!='':
                    ResFile.write(str(HanLP(line.strip(),tasks='tok/coarse'))+'\n')
                line = OriFile.readline()
            OriFile.close()
        ResFile.close()

    if condition['ner']:
        ResFile=open('resNER.txt',mode='w')
        with open('天津市突发地质灾害应急预案.txt',mode='r') as OriFile:
            line = OriFile.readline()
            while line:
                if line.strip()!='':
                    ResFile.write(str(HanLP(line.strip())["ner/msra"])+'\n')
                line = OriFile.readline()
            OriFile.close()
        ResFile.close()

