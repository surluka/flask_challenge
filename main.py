# from extractors.wanted import extract_wanted_jobs
# from file import save_to_file

# keyword = input("무슨 직종을 검색 하시겠습니까?\n")

# jobs = extract_wanted_jobs(keyword)

# save_to_file(keyword, jobs)


# 콘트롤 타워 같은 역할을 한다.... 이건 백엔드 이다... 다양한 검색 결과를 위하여 오브젝트(클래스)화 시킨다면 좀더 다이나믹하게 사용 할 수 있어 보인다
# 검색어가 엉뚱하게 들어 왔을때 즉 아무것도 검색이 되지 않았을때의 문제를 해결하지 못했다... 추후에 만들어 보도록 한다.  (사실 이게 제일 중요한건데....)
# 에라가 나오는것을 보니 각 익스트랙터 에서 try ecept 를 사용하면 손쉽게 해결 할 수 있다 n/a 를 넣는다거나 하면 되지 않을까 시간이 없어서 얼른 마무리 한다

from flask import Flask, render_template, request, redirect , send_file
from extractors.berlin import extract_berlin_jobs
from extractors.web3 import extract_web3_jobs
from file import save_to_file

app = Flask("JobScrapper")                                      # 플라스크를 실행한다

db = {}  # 딕셔너리의 구조를 모르면 헤깔릴 수 있음                 # 이 딕셔너리에다가 각 검색어(key) 의 밸류값을 몽땅 저장하게 된다 일종의 캐쉬 파일 저장  

@app.route("/")                                                 # /에 접근했을때 자동 실행 되는 플라스크
def home():
    return render_template("home.html")                         # 렌더 템플릿 명령으로 home.html 을 렌더링 해 준다  주소창을 보면 home.html 이 아닌것을 알 수 있다 루트에 렌더링 되는것이다 


@app.route("/search")                                           # home.html 에 보면 action 으로 /search 를 발동시킨다 그럼 이 플라스크가 실행이 된다 개념이 맞는지 모르겠다
def search():
    
    keyword = request.args.get("keyword")                       # 키워드를 받아온다 플레이스 홀더의 keyword 를 받아오는데 html 의 구조와 문법을 몰라서 정확히는 알지 못하겠다
    
    if keyword == None:                                         # 키워드를 안너은채 엔터 눌렀을때 None 값이 나오니까
        return redirect("/")                                    # / 로 렌더링 해 버린다
    
    if keyword in db:                          # db 의 키값에서 키워드가 있다면
        jobs = db[keyword]                     # 그 키의 밸류를 jobs 로 한다 가 된다 밸류값이 리스트로 엄청 길다.... 키값은 키워드가 되고 밸류값은 검색한 리스트가 되는거임
    else:
        jobs = extract_berlin_jobs(keyword) + extract_web3_jobs(keyword)   # 결과를 합친다.
        db[keyword] = jobs                                                 # 캐쉬를 위해서 db 에 저장해 둔다 캐쉬라는 말이 맞는지도 모르겠다
        # print(db) # 요렇게 해 보면 키워드키값에 대한 밸류값을 볼 수 있다....밸류는 당연하게 리스트안에 딕셔너리가 들어가 있는 형태가 됨

    return render_template("search.html", keyword = keyword, jobs = jobs)  # 검색에 대한 결과를 위하여 렌더링 해 주고 필요한 매개변수를 만들어 너어 주었다 그래야 search.html 에서 받아서 화면에 뿌릴 수 있다

@app.route("/export")                                                      # 파일을 저장할때 발동될 플라스크 이다                                                 
def export():

    keyword = request.args.get("keyword")                                  # 역시나 플라스크가 keyword 를 요청한다

    if keyword == None:                                                    # 키워드가 없을때는 루트로 렌더링 한다
        return redirect("/")

    if keyword not in db:                                                  # 키워드가 입력이 되었는데 db 캐쉬에는 없다면
        return redirect(f"/search?keyword={keyword}")                      # 친절하게도 /search 에 키워드를 입력해서 너어준다 그럼 결과물이 보일테지 고로 검색 하지 않고 다운만 누르면 동작이 되는 신박한 구조

    save_to_file(keyword, db[keyword])                                     # 키워드를 받아와서 파일을 만들고

    return send_file(f"{keyword}.csv", as_attachment=True)                 # 다운로드 창이 뜬다

app.run("0.0.0.0")                                                         # vsc 에서 로컬로 동작한다