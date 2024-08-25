# 현재 강좌에 있는 csv 저장 방법은 2종이 있다 csv 모듈을 활용하여 작성하는 방법이 좀더 좋아 보인다
# 이 방법으로는 리스트 안에 , 가 있을때 쎌이 떨어져 버리는 웃지못할 사고가 발생한다 난중에 고쳐 보자

def save_to_file(file_name, jobs):                                             # 파일 네임과, 리스트를 받아온다
    file = open(f"{file_name}.csv", "w", encoding='utf-8')                     # 파일을 만든다, 인코딩을 하지 않으면 에러가 날 확률이 높다 
    file.write("title, company, link\n")                                       # 초기 헤더를 쓴다

    for job in jobs:                                                           # 반복문을 통해 해당 위치에 줄줄이 쓴다 키값에 있는 밸류를 적어주는 형태로 되어 있다
       file.write(f"{job['title']},{job['company']},{job['link']}\n")

    file.close()                                                               # 파일을 닫아준다


