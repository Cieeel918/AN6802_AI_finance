from flask import Flask, request, render_template
import sqlite3
import datetime

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return(render_template('index.html')) 

@app.route("/main",methods=["GET","POST"])
def main():
    user_name=request.form.get("q")
    t=datetime.datetime.now()
    conn=sqlite3.connect('user.db')
    c=conn.cursor()
    c.execute('insert into user values(?,?)',(user_name,t))
    # 使用占位符 ? 向 user 表插入一行数据。
    # 变量 name 和 t 应该是你预先定义好的数据
    conn.commit() #提交事务，保存插入的数据。
    c.close()
    conn.close()

    return(render_template('main.html'))

@app.route("/foodexp", methods=['GET', 'POST']) 
def foodexp():
    return(render_template('foodexp.html'))

@app.route("/foodexp_pred",methods=["POST","GET"])
def foodexp_pred():
    q = float(request.form.get("q"))
    return(render_template("foodexp_pred.html",r=(q * 0.4851)+147.4))
    
@app.route("/ethical_test", methods=['GET', 'POST']) 
def ethical_test():
    return(render_template('ethical_test.html'))

@app.route("/ethical_result",methods=["POST","GET"])
def ethical_result():
    answer = request.form.get("answer")
    if answer == "false":
        return(render_template("pass.html"))
    elif answer == "true":
        return(render_template("fail.html"))

@app.route("/userlog", methods=['GET', 'POST']) 
def userlog():
    #从 user 表中查询所有数据，然后一边打印每一行，一边把它们拼接成一个字符串 r。
    #打开数据库连接，获取游标对象用于执行 SQL。
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    #执行 SQL 查询，获取 user 表中的所有数据。
    c.execute('select * from user')
    r=''
    for row in c:
        r = r + str(row) + "\n" #把所有行拼成一个多行字符串。
    print(r)
    c.close()
    conn.close()
    return(render_template('userlog.html',r=r))

if __name__=='__main__':
    app.run()