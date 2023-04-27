import os
import math
import hanlp
import re


def ner(path):
    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
    ResFile = open(path+r'\result\ner.txt', mode='w', encoding='ANSI')
    WriteFile1 = open(path+r'\result\class_org.txt', mode='w', encoding='ANSI')
    WriteFile2 = open(path+r'\result\class_loc.txt', mode='w', encoding='ANSI')
    with open(path+r'\天津市突发地质灾害应急预案.txt', mode='r', encoding='ANSI') as OriFile:
        line = OriFile.readline()
        index=0
        while line:
            if line.strip() != '':
                outcome = HanLP(line.strip(), tasks="ner/msra")["ner/msra"]
                written_in_org = False
                written_in_loc = False
                for_write = str(outcome)
                if for_write != '[]':
                    ResFile.write(for_write + '\n')
                for item in outcome:
                    if item[1] == 'ORGANIZATION' and not written_in_org:
                        WriteFile1.write('序号'+str(index)+'：'+line + '\n')
                        written_in_org = True
                    if item[1] == 'LOCATION' and not written_in_loc:
                        WriteFile2.write('序号'+str(index)+'：'+line + '\n')
                        written_in_loc = True
            index+=1
            line = OriFile.readline()
        OriFile.close()
    ResFile.close()


def classify(path):
    ReadFile = open(path+r'\result\sentences.txt', mode='r', encoding='ANSI')
    WriteFile = open(path+r'\result\classification.txt', mode='w', encoding='ANSI')
    WriteFile.write('组织机构类' + '\n')
    ReadLine = ReadFile.readline().strip()
    index=0
    while ReadLine:
        if re.match(r'.*[局部委队院站][^长员].*', ReadLine) or re.match(r'.*办公室.*', ReadLine):
            WriteFile.write('序号'+str(index)+'：'+ReadLine + '\n' + '\n')
        ReadLine = ReadFile.readline().strip()
        index+=1
    WriteFile.write('地址类' + '\n')
    ReadFile.seek(0, 0)
    ReadLine = ReadFile.readline().strip()
    index=0
    while ReadLine:
        if re.match(r'.*天津.*', ReadLine) or re.match(r'.*蓟州.*', ReadLine):
            WriteFile.write('序号'+str(index)+'：'+ReadLine + '\n' + '\n')
        ReadLine = ReadFile.readline().strip()
        index+=1
    ReadFile.close()
    WriteFile.close()


if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    ner(path)
    classify(path)