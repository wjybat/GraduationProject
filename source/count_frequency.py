import os


def count_freq(path):
    WriteFile = open(path+r'\result\words_bag_final.txt', mode='r+', encoding='ANSI')
    ReadFile = open(path+r'\result\tokens_final.txt', mode='r', encoding='ANSI')
    ReadLine = ReadFile.readline().strip()
    while ReadLine:
        WriteFile.seek(0, 0)
        WriteLine = WriteFile.readline().strip()
        count = 0
        has = False
        line_num = 1
        last_pos = 0
        while WriteLine:
            word = WriteLine.split('|')[0]
            count = int(WriteLine.split('|')[1])
            if word == ReadLine:
                count += 1
                has = True
                break
            else:
                last_pos = WriteFile.tell()
                WriteLine = WriteFile.readline().strip()
                line_num += 1
        if has:
            WriteFile.seek(last_pos, 0)
            WriteFile.write('%s|%05d\n' % (word, count))
        else:
            count = 1
            WriteFile.seek(0, 2)
            WriteFile.write('%s|%05d\n' % (ReadLine, count))
        ReadLine = ReadFile.readline().strip()
    ReadFile.close()
    WriteFile.close()


def sort_freq(path):
    ReadFile = open(path+r'\result\words_bag_final(copy).txt', mode='r+', encoding='ANSI')
    WriteFile = open(path+r'\result\sorted_wb_final.txt', mode='w', encoding='ANSI')
    total_lines_count = len(ReadFile.readlines())
    print(total_lines_count)
    ReadFile.seek(0, 0)
    cur_line = 0
    while cur_line < total_lines_count:
        MaxCount = 0
        change_word = ''
        change_pos = 0
        last_pos = 0
        ReadLine = ReadFile.readline().strip()
        while ReadLine:
            word = ReadLine.split('|')[0]
            count = int(ReadLine.split('|')[1])
            if count > MaxCount:
                change_word = word
                MaxCount = count
                change_pos = last_pos
            last_pos = ReadFile.tell()
            ReadLine = ReadFile.readline().strip()
        WriteFile.write('%s|%05d\n' % (change_word, MaxCount))
        ReadFile.seek(change_pos, 0)
        ReadFile.write('%s|%05d\n' % (change_word, 0))
        ReadFile.seek(0, 0)
        cur_line += 1
    ReadFile.close()
    WriteFile.close()


if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # count_freq(path)
    sort_freq(path)
