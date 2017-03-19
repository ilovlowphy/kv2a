#-*- coding: UTF-8 -*- 
# import glob
import os
import sqlite3
import time
from datetime import datetime
import re
import codecs

anki_list=[]
def get_vocabfile_path():
    for i in ['G','F','H','I','J','K','L','M','N','E','O','P','Q','R','S','T','U','V','W','X','Y','Z','A','B','C','D']:
        # if glob.glob(i+':\\system\\vocabulary\\vocab.db'):
        if os.path.isfile(i+':\\system\\vocabulary\\vocab.db'):
            # print i+':\\system\\vocabulary\\vocab.db'
            return i+':\\system\\vocabulary\\vocab.db'
            # break
    print 'Please connect your kindle to the computer!'
    old_file_name = raw_input('Press Enter to exit!')

def timestamp_to_strtime(timestamp):
    """将 13 位整数的毫秒时间戳转化成本地普通时间 (字符串格式)
    :param timestamp: 13 位整数的毫秒时间戳 (1456402864242)
    :return: 返回字符串格式 {str}'2016-02-25 20:21:04.242000'
    """
    local_str_time = datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
    return local_str_time

def time_conv(tt):
    try:
        st3 = time.strptime(tt, '%Y-%m-%d-%H%M')
        return time.mktime(st3)
    except ValueError:
        return 0
# print time_conv(st2)

def get_syn_time_history():
    syn_time_history=[]
    all_files=os.listdir(os.getcwd())
    for fl in all_files:
        fl_name=os.path.splitext(fl)
        if fl_name[1]=='.txt':
            if time_conv(fl_name[0]):
                syn_time_history.append(time_conv(fl_name[0]))
    return syn_time_history


syn_time_history=get_syn_time_history()
if syn_time_history:
    last_syn_time=max(syn_time_history)*1000
else:
    last_syn_time=0

#print last_syn_time

# print get_vocabfile_path()
file_apth=get_vocabfile_path()
if file_apth:
    conn = sqlite3.connect(file_apth)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM LOOKUPS')
    values = cursor.fetchall()
    # print len(values)
    for row in values:
    #    print row[0]
        anki_list_item=[]
        cloze_word=''
        cloze=''
        values1 =[]
        values2 =[]
        anki_list_item.append(row[0]) #id
        cursor.execute('SELECT word, stem FROM WORDS WHERE id=?',(row[1],))
        values1 = cursor.fetchall()
        cloze_word=values1[0][0]
        anki_list_item.append(values1[0][0]) #句中出现的形式
        anki_list_item.append(values1[0][1]) #单词原形
        cursor.execute('SELECT title, authors FROM BOOK_INFO WHERE id=?',(row[2],))
        values2 = cursor.fetchall()
        anki_list_item.append(values2[0][0]) #书名
        anki_list_item.append(values2[0][1]) #作者
        anki_list_item.append(row[4]) #position
        cloze=re.sub('([^a-zA-Z])('+cloze_word+')([^a-zA-Z])','\g<1>{{c1::\g<2>}}\g<3>',row[5])
        anki_list_item.append(cloze) #例句
        anki_list_item.append(timestamp_to_strtime(row[6]))
        anki_list_item.append(row[6]) #时间戳   
        anki_list.append(anki_list_item)
        # print anki_list_item

    # print anki_list
    cursor.close()
    conn.close()
    if anki_list:
        st2=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H%M')
        f=open(os.getcwd()+os.path.sep+st2+'.txt','w')
        for anki_item in anki_list:
            if anki_item[8]>last_syn_time:
                # f.write(('\t'.join(anki_item)[0:6]+'\n').encode('utf-8'))
                f.write((anki_item[0]+u'\t'+anki_item[1]+u'\t'+anki_item[2]+u'\t'+anki_item[3]+u'\t'+anki_item[4]+u'\t'+anki_item[5]+u'\t'+anki_item[6]+u'\t'+anki_item[7]+u'\n').encode('utf-8'))
        f.close()
    else:
        print 'The vocabuleries have been syned before'


