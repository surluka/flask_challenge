import requests
from bs4 import BeautifulSoup

# 이 사이트는 정확히 검색어 지원을 안한다... 보유하고 있는 카테고리가 있고 그 카테고리를 클릭 하거나 카테고리 검색을 했을때 있어야만 결과물이 보여진다. 없으면 에러창이 나온다
# 페이지네이션의 경우 계속 넥스트 버튼을 체크 해 봐야 마지막을 알 수 있다 while 문을 쓰는편이 좋긴 하다 if, try 등 방법은 많다
# html 과 css 를 전혀 모르기 때문에 애로사항이 많다
# 최대한 심플하고 쉽게 하는것을 목표로 했다


header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}   # 귀찮은 헤더 

def extract_web3_jobs(keyword):                                                                             # 키워드를 입력하여 실행
    
    jobs_list = []                                                                                          # 리턴할 리스트

    page_num = 1                                                                                            # 1번 페이지부터 검색 시작한다
    next_disable = False                                                                                    # "page-item next disabled" 이라는 클라스가 보이면 True 로  

    while not next_disable:                                                                                 # ! 가 아니다 not 이다 뭔가 직관적인거 같기도 하고 헤깔릴꺼 같기도 하고 while 문 써보면서 연습한다
        response = requests.get(f"https://web3.career/{keyword}-jobs?page={page_num}", headers=header)          # 키워드릴 입력하여 카테고리 첫번째 페이지에 접근 첫번째 페이지는 리 다이렉트 되어 있다
        soup = BeautifulSoup(response.content, "html.parser")                                                   # 파싱하고
        jobs = soup.find("tbody", class_="tbody").find_all("tr", class_="table_row")                            # 잡스를 불러온다 리스트로 받음        
        del jobs[4]                                                                                             # 광고창이 들어가 있다.... 늘 5번째에 나온다 정확하게 하려면 광고창의 성분을 찾아서 지워주면 된다 이거 안지워주면 계속 에러남

        # print(len(jobs))                                                                                      # 잘되는지 확인용  한페이지에 25개가 나오니 25가 나오면 정상

        for job in jobs:                                                     
            title = job.find("h2", class_="fs-6 fs-md-5 fw-bold my-primary").text                               # 타이틀을 찾는다 클라스명으로 찾으면 된다 이거 모르겠음... h2, h3 의 text는 우찌 불러온단 말인가 --- 중간에 광고가 들어가서 에러가 나온 것이었음
            company = job.find("h3", class_="").text                                                            # 이것도 마찬가지 h4 만 들어가면 text 가 먹질 안는다 모르겠음--- 중간에 광고가 들어가서 에러가 나온 것이었음
            link = f"https://web3.career{job.find('a')['href']}"                                                # 링크도 불러온다 이번엔["href"]를 사용해 봤다

            job = {"title":title,                                                                               # 딕셔너리를 만들어서
                   "company":company,
                   "link":link}

            jobs_list.append(job)                                                                               # 리스트에 업데이트 해 준다

        if soup.find("li", class_="page-item next disabled"):                                                   # "page-item next disabled" 이 나오게 되면 break 를 해도 되고 지금처럼 변수를 써도 되고 맘대로다                                                                                                                                                                                                        # page-item next disabled 즉 넥스트 버튼이 꺼져있다면 클라스가 존재한다면 마지막 페이지라는 말                                                                             # 넥스트 디저블이 활성화가 되어 반복문 동작을 멈춘다
            next_disable = True                                                                                 # 변수를 바꿔줘서 초보답게 시인성을 높인다
        else:                                                                                                   # 못찾게 되면 페이지수를 업데이트 한다
            page_num+=1                                                                                         # 페이지 숫자에 1을 더한다.....

    return(jobs_list)                                                                                           # 최종값을 리턴 해 준다                             

# extract_web3_jobs("python")                                                                                   # 동작 확인용


