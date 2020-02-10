import flask
from flask import Flask, redirect, url_for, request,session, jsonify
from datetime import datetime
import re, sys,os, json
from flask import render_template
import Pinterest
import urllib.request as req
from flask_fontawesome import FontAwesome


app = Flask(__name__)
app.secret_key = os.urandom(12)



@app.route("/")
def index():
    return render_template("login.html")


@app.route('/login', methods=['POST', 'GET'])
def login(data=None):
    if request.method == 'POST':
        user = request.form['username']
        email=request.form['email']
        pw = request.form['password']
        # print(user, file=sys.stdout)
        pint = Pinterest.Pinterest(username=user,email=email, password=pw)
        flask.current_app.account= pint
        login_sts= pint.login()
        # print(login_sts.status_code, file=sys.stdout)
        # print(pint.get_user_overview(), file=sys.stdout)
        # print(flask.current_app.account)

        user_info= pint.get_user_overview()
        flask.current_app.user_info= user_info

        if(login_sts.status_code==200):
            session['username']=user
            session['password']=pw
            session['email']=email
            return render_template("user.html",data=user_info)
        else:
            return redirect(url_for('login'))

    if request.method == 'GET':
        
        query = flask.request.args.get('query')
        # current_account = flask.g.get('current')
        current_account=flask.current_app.account
        # print(current_account)
        res = []
        search_batch = current_account.search('pins', query)
        while len(search_batch) > 0 and len(res) < 500:
            res += search_batch
            search_batch = current_account.search('pins', query=query)
        # res=current_account.search('pins',query)
        with open(str(query)+'.json', 'w') as f:
            json.dump(res, f)

        return flask.jsonify(res)

@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == 'GET':
        query = flask.request.args.get('query')
        imgs = flask.request.args.getlist('doc_imgs[]')

        path=query


        user_name = flask.current_app.user_info['username']

      
        if not os.path.exists('Pics'):
            os.mkdir('Pics')
        
        if not os.path.exists('Pics/'+user_name+query):
            os.mkdir('Pics/'+user_name+'_'+query)
        
        print('downloading pictures')
        for i in imgs:
            img_name=re.search(pattern='[0-9a-z]*.jpg',string=i).group()
            # print('/'+path+'/'+img_name)  
            req.urlretrieve(i, 'Pics/'+user_name+'_'+query+'/'+img_name)
        return  "susscess"


@app.route('/account', methods=['POST', 'GET'])
def account():
    if request.method == 'GET':
        user_info = flask.current_app.user_info

        with open(user_info['username']+'.json', 'w') as f:
            json.dump(user_info, f)
    return "success"
    
@app.route('/analysis', methods=['POST','GET'])
def analysis():
        if request.method == 'GET':
            dirs=os.listdir('Pics')
            return render_template('analysis.html',data=dirs)


@app.route('/get_folder', methods=['GET'])
def get_folder():
     if request.method == 'GET':
         folder = flask.request.args.get('name')
         folder= folder.strip()
         res={}
         res['summary']=os.stat('Pics/'+folder)
         res['array']=os.listdir('Pics/'+folder)

        # So the variable res['array'] contains all the file names you need to use.
        # You could continue coding from here
        # This method should generate things that could possibly return to the html page (analysis.html)


         return jsonify(result=res)




# @app.route('/scrapper')
# def scrapper():
#     current_user=session.get('username')
#     current_pw=session.get('password')
#     current_email=session.get('email')
#     print(current_pw, file=sys.stderr)
#     print(current_email, file=sys.stderr)
#     print(current_user, file=sys.stderr)
#     # pint = Pinterest.Pinterest(email=current_email, password=current_pw, username=current_user)
#     # print(pint.login())
#     user_data=pint.get_user_overview()

#     # data=pint.get_user_overview()

#     return render_template("user.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True,use_reloader=True)