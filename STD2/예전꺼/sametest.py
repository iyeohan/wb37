import cv2
import os
import pandas as pd
from skimage.metrics import structural_similarity as ssim
import std_CompVis
import std_tutorial

#사진 리스트
photo_list = []

for f in os.listdir('static/img'):
    if 'jpeg' in f:
        photo_list.append(f)

#사진 크기
photo_size = list(map(lambda x: os.path.getsize('static/img' + '/' + x), photo_list))

#데이터 프레임으로
fsp = pd.DataFrame({'filename_raw':photo_list, 'size':photo_size})

import re   # 정규표현식
com = re.compile(' \d')
fsp['filename'] = list(map(lambda x: com.sub('', x), photo_list))

print('사진의 갯수 :', len(fsp)) 

# Photo Value Counts
pvc = pd.DataFrame({'filename':fsp['filename'].value_counts().index, 'fn_counts':fsp['filename'].value_counts().values})   
psvc = pd.DataFrame({'size':fsp['size'].value_counts().index, 'size_counts':fsp['size'].value_counts().values})   

fsp = pd.merge(fsp, pvc, how = 'left', on = 'filename')
fsp = pd.merge(fsp, psvc, how = 'left', on = 'size')

fsp_nsn = fsp.sort_values(['filename_raw'], ascending = False).drop_duplicates(['filename'], keep = 'first')

pvc_nsn = pd.DataFrame({'filename':fsp_nsn['filename'].value_counts().index, 'fn_counts_nsn':fsp_nsn['filename'].value_counts().values})   
psvc_nsn = pd.DataFrame({'size':fsp_nsn['size'].value_counts().index, 'size_counts_nsn':fsp_nsn['size'].value_counts().values})   

fsp_nsn = pd.merge(fsp_nsn, pvc_nsn, how = 'left', on = 'filename')
fsp_nsn = pd.merge(fsp_nsn, psvc_nsn, how = 'left', on = 'size')

delete = []  # 삭제할 파일 목록을 저장할 리스트
indices_to_delete = []  # 삭제할 인덱스를 저장할 리스트

for i in range(len(fsp_nsn)-1,-1,-1):
    if (fsp_nsn['size'][i] <= 5000):
        delete.append(fsp_nsn['filename_raw'][i])
        fsp_nsn=fsp_nsn.drop(i, axis=0)
    
fsp_nsn.reset_index(drop=True, inplace=True)

for i in range(len(fsp_nsn)):
    
    # 사진 읽기
    imageA = cv2.imread('static/img/'+fsp_nsn['filename_raw'][i])
    # 이미지를 grayscale로 변환
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)

    for x in range(len(fsp_nsn)):

        imageB = cv2.imread('static/img/'+fsp_nsn['filename_raw'][x])
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        if fsp_nsn['filename'][i]!=fsp_nsn['filename'][x]:
            # 이미지의 구조가 같다면 이미지 비교
            if len(grayA)==len(grayB):
                (score, diff) = ssim(grayA, grayB, full=True)
                
                # 차이가 없다면 하나는 delete에 넣어주기
                if score == 1:
                    delete.append(fsp_nsn['filename_raw'][i])
                
                # 구조가 같지만 차이가 존재한다면 직접 확인하기     
                elif score>=0.5:
                    print('확인해보시오! : ', fsp_nsn['filename_raw'][i], '/', fsp_nsn['filename_raw'][x], f'(score : {score})')

#delete = delete + list(fsp[~fsp['filename_raw'].isin(fsp_nsn['filename_raw'])]['filename_raw'])
delete = list(fsp[~fsp['filename_raw'].isin(fsp_nsn['filename_raw'])]['filename_raw'])

print('삭제할 목록 :', delete)