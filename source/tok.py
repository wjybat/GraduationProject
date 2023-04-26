import string
import hanlp
import re
import os


def tokenize(excl_list,path):
    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
    HanLP['tok/coarse'].dict_combine={'以人为本','人民至上','生命至上','群测群防','山体','市指挥部',
                                      '市应急局','市规划资源局','市卫生健康委','市交通运输委','市委宣传部',
                                      '市委网信办','市公安局','市民政局','市水务局','市住房城乡建设委',
                                      '市城市管理委','市教委','市农业农村委','市农业农村委','市发展改革委','市财政局','市文化和旅游局',
                                      '市气象局','市通信管理局','市粮食和物资局','市商务局','国网天津市电力公司','武警天津总队',
                                      '市消防救援总队'}
    ResFile = open(path+r'\result\tokens_final.txt', mode='w',encoding='ANSI')
    with open(path+r'\天津市突发地质灾害应急预案.txt', mode='r',encoding='ANSI') as OriFile:
        line = OriFile.readline()
        while line:
            if line.strip() != '':
                res_list = HanLP(line.strip(), tasks='tok/coarse')['tok/coarse']
                for item in res_list:
                    if item not in excl_list and re.match(r'.*\d+.*', item) is None and \
                            re.match(r'[一二三四五六七八九十]+', item) is None and \
                            re.match(r'[ⅠⅡⅢⅣⅤⅥⅦⅧⅨ]+', item) is None:
                        ResFile.write(str(item) + '\n')
            line = OriFile.readline()
        OriFile.close()
    ResFile.close()


if __name__ == '__main__':
    exclude = list(string.punctuation)
    exclude.extend(['，', '。', '：', '”', '’', '？', '；', '《',
                    '》', '——', '、', '—', '（', '）', '〔', '〕', '．'])
    exclude.extend(['的','和','等','或','在','对','是','两','按','将','以','从','于'])
    path=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    tokenize(exclude,path)