from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}

#decorator(@)는 바로 아래에 있는 [함수]를 찾아. 함수의 이름은 상관 없음
#html파일들은 [templates]라는 이름의 디렉토 안에 존재해야해
@app.route("/")
def home():
    return render_template("job.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        #소문자로
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    #html파일로 searchingBy라는 변수에 word(값)을 넣어준다. -> html에서는 {{searchingBy}} 이런식으로 데이터를 사용할 수 있다.
    return render_template("report.html",
                           resultsNumber=len(jobs),
                           searchingBy=word,
                           jobs=jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")

app.run(host="0.0.0.0")