import sqlite3
import os
# 데이터베이스 파일명
db_filename = 'stdlist.db'

def check():
    # 데이터베이스 파일이 존재하지 않으면 생성
    if not os.path.exists(db_filename):
        # 데이터베이스 연결
        connection = sqlite3.connect(db_filename)
        
        # 데이터베이스 커서 생성
        cursor = connection.cursor()
        
        # 데이터베이스 파일 생성 후 작업
        # 여기에서 테이블을 생성하거나 다른 작업을 수행할 수 있습니다.
        
        # 커밋 및 연결 종료
        connection.commit()
        connection.close()
        
create_table_query="""
CREATE TABLE IF NOT EXISTS stable_diffusion2(
    idx INTEGER NOT NULL PRIMARY KEY,
    User	TEXT,
	stdname	TEXT NOT NULL,
    positive_prompt TEXT NOT NULL,
    nagative_prompt TEXT NOT NULL,
    filter TEXT NOT NULL,
    uploaded_file1 TEXT NOT NULL,
    uploaded_file2 TEXT NOT NULL,
    result_file TEXT NOT NULL,
    share INTEGER NOT NULL
);
"""

def create_table():
    check()
    list = sqlite3.connect('stdlist.db')
    cursor = list.cursor()
    
    # 이미 테이블이 생성되었는지 확인
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stable_diffusion2';")
    if cursor.fetchone() is None:
        # 테이블이 아직 생성되지 않은 경우 테이블 생성
        cursor.execute(create_table_query)   
        list.commit()

    list.close()  
     
#정보 저장
def save(index, username, stdname, pprompt, nprompt, f, img1, img2, rf, share):   
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    insert_data_query='''
    INSERT INTO stable_diffusion2(idx, User, stdname, positive_prompt, 
    nagative_prompt, filter, uploaded_file1, uploaded_file2, result_file, share)
    VALUES(?,?,?,?,?,?,?,?,?,?);
    '''
    
    data_to_insert = (index, username, stdname, pprompt, nprompt, f, img1, img2, rf, share)
    
    cursor.execute(insert_data_query, data_to_insert)

    list.commit()
    list.close()
    return None

#저장된 데이터 전부 불러오기
def load_list(stdname):
    create_table()
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    data_list=[]
    if(stdname=="all"):
        select_data_query='''
        SELECT * FROM stable_diffusion2 WHERE share=1;
        '''
        cursor.execute(select_data_query)
    else:
        select_data_query='''
        SELECT * FROM stable_diffusion2 WHERE stdname=? AND share=1;
        '''
        cursor.execute(select_data_query,(stdname,))
        
    data=cursor.fetchall()
    
    for row in data:
        data_list.append(row)
        
    list.commit()
    list.close()
    return data_list

def user_load_list(stdname, user):
    create_table()
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    data_list=[]
    if(stdname=="all"):
        select_data_query='''
        SELECT * FROM stable_diffusion2 WHERE User=?;
        '''
        cursor.execute(select_data_query,(user,))
    else:
        select_data_query='''
        SELECT * FROM stable_diffusion2 WHERE stdname=? AND share=1 AND User=?;
        '''
        cursor.execute(select_data_query,(stdname, user,))
        
    data=cursor.fetchall()
    
    for row in data:
        data_list.append(row)
        
    list.commit()
    list.close()
    return data_list

#특정 인덱스 값 가져오기
def Now_idx():    
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    select_data_query = "SELECT COUNT(*) FROM stable_diffusion2;"
    cursor.execute(select_data_query)
    row = cursor.fetchone()
    count=row[0]
    
    list.commit()
    list.close()
    return count+1

#특정 인덱스 값의 데이터 가져오기
def load_std(idx):
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    select_data_query='''
    SELECT * FROM stable_diffusion2 WHERE idx=?;
    '''
    cursor.execute(select_data_query,(idx,))
    data=cursor.fetchall()
    
    list.commit()
    list.close()
    print(data)
    return data

def delete(idx):
    list=sqlite3.connect('stdlist.db')
    cursor=list.cursor()
    
    delete_data_query="DELETE FROM stable_diffusion2 WHERE idx=?"
    cursor.execute(delete_data_query,(idx,))
    list.commit()
    list.close()
    return None

#create_table()
# for i in range(22,24):
#     delete(i)