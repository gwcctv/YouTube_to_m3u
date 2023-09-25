import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url):
    response = requests.get(url, timeout=15).text
    if '.m3u8' not in response:
        # response = requests.get(url).text
        if '.m3u8' not in response:
            if windows:
                return 'https://raw.githubusercontent.com/gwcctv/YouTube_to_m3u/main/assets/404.mp4'
            # os.system(f'wget {url} -O temp.txt')
            os.system(f'curl "{url}" > temp.txt')
            response = ''.join(open('temp.txt').readlines())
            if '.m3u8' not in response:
                return 'https://raw.githubusercontent.com/gwcctv/YouTube_to_m3u/main/assets/404.mp4'
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
    return link[start : end]

with open('../youtube_channel_info.txt') as f:
    groups = []  # 用于存储每组数据的列表
    group = []  # 用于存储当前组数据的列表

    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            if group:
                groups.append(group)  # 将当前组添加到groups列表中
                group = []  # 清空当前组列表
            line = line.split('|')
            ch_name = line[0].strip()
            group.append(ch_name)  # 将标题添加到当前组列表中
        else:
            link = grab(line)
            group.append(link)  # 将链接添加到当前组列表中
            
    if group:
        groups.append(group)

    for group in groups:
        if len(group) == 1:  # 如果当前组只有标题而没有链接
            group.append('https://raw.githubusercontent.com/gwcctv/YouTube_to_m3u/main/assets/404.mp4')
        print(' '.join(str(item) for item in group))
        
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
