import hanlp
import os
import string
import re


def sentencing(path):
    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
    HanLP['tok/coarse'].dict_combine = {'以人为本', '人民至上', '生命至上', '群测群防', '山体', '市指挥部',
                                        '市应急局', '市规划资源局', '市卫生健康委', '市交通运输委', '市委宣传部',
                                        '市委网信办', '市公安局', '市民政局', '市水务局', '市住房城乡建设委',
                                        '市城市管理委', '市教委', '市农业农村委', '市农业农村委', '市发展改革委', '市财政局', '市文化和旅游局',
                                        '市气象局', '市通信管理局', '市粮食和物资局', '市商务局', '国网天津市电力公司', '武警天津总队',
                                        '市消防救援总队'}
    ReadFile = open(path+r'\天津市突发地质灾害应急预案.txt', mode='r', encoding='ANSI')
    WriteFile = open(path+r'\result\sentences.txt', mode='w', encoding='ANSI')
    ResFile = open(path+r'\result\tokensForTF_final.txt', mode='w', encoding='ANSI')
    ReadLine = ReadFile.readline()
    while ReadLine:
        if ReadLine.strip().find('。') != -1:
            Sentences = ReadLine.strip().split('。')
            for sentence in Sentences:
                if sentence != '':
                    WriteFile.write(sentence + '\n')
                    init_list = HanLP(sentence, tasks='tok/coarse')['tok/coarse']
                    res_list = []
                    exclude = list(string.punctuation)
                    exclude.extend(['，', '。', '：', '”', '’', '？', '；', '《',
                                    '》', '——', '、', '—', '（', '）', '〔', '〕', '．'])
                    exclude.extend(['的','和','等','或','在','对','是','两','按','将','以','从','于'])
                    for item in init_list:
                        if item not in exclude and re.match(r'.*\d+.*', item) is None and \
                                re.match(r'[一二三四五六七八九十]+', item) is None and \
                                re.match(r'[ⅠⅡⅢⅣⅤⅥⅦⅧⅨ]+', item) is None:
                            res_list.append(item)
                    ResFile.write(str(res_list) + '\n')
        ReadLine = ReadFile.readline()
    ReadFile.close()
    WriteFile.close()
    ResFile.close()


if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sentencing(path)