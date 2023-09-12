import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url):
    response = requests.get(url, timeout=15).text
    if '.m3u8' not in response:
        #response = requests.get(url).text
        if '.m3u8' not in response:
            if windows:
                print('https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u')
                return
            #os.system(f'wget {url} -O temp.txt')
            os.system(f'curl "{url}" > temp.txt')
            response = ''.join(open('temp.txt').readlines())
            if '.m3u8' not in response:
                print('https://raw.githubusercontent.com/benmoose39/YouTube_to_m3u/main/assets/moose_na.m3u')
                return
    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end-tuner : end]:
            link = response[end-tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
    print(f"{link[start : end]}")

#s = requests.Session()
with open('../youtube_channel_info.txt') as f:
    groups = []  # 用于存储每组数据的列表
    group = []  # 用于存储当前组数据的列表

    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            group.append(ch_name)  # 将当前元素添加到当前组列表中
            
            if len(group) == 1:  # 判断当前组是否已满
                groups.append(group)  # 将当前组添加到groups列表中
                group = []  # 清空当前组列表
        else:
            grab(line)
            
    if len(group) > 0:
        groups.append(group)

    for group in groups:
        print(' '.join(str(item) for item in group))
        
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
