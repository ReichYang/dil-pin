from flask import Flask
import flask
from flask import Flask, redirect, url_for, request,session
from datetime import datetime
import re, sys,os, json
from flask import render_template
import Pinterest
import urllib.request as req
from flask_fontawesome import FontAwesome


application = Flask(__name__)
application.secret_key = os.urandom(12)

@application.route("/")
def index():
    return render_template("login.html")


@application.route('/login', methods=['POST', 'GET'])
def login(data=None):
    if request.method == 'POST':
        user = request.form['username']
        email=request.form['email']
        pw = request.form['password']
        print(user, file=sys.stdout)
        pint = Pinterest.Pinterest(username=user,email=email, password=pw)
        flask.current_app.account= pint
        login_sts= pint.login()
        print(login_sts.status_code, file=sys.stdout)
        print(pint.get_user_overview(), file=sys.stdout)
        print(flask.current_app.account)
        if(login_sts.status_code==200):
            session['username']=user
            session['password']=pw
            session['email']=email
            return render_template("user.html",data=pint.get_user_overview())


    if request.method == 'GET':
        
        query = flask.request.args.get('query')
        # current_account = flask.g.get('current')
        current_account=flask.current_app.account
        # print(current_account)
        res = []
        search_batch = current_account.search('pins', query)
        while len(search_batch) > 0 and len(res) < 1000:
            res += search_batch
            search_batch = current_account.search('pins', query=query)
        # res=current_account.search('pins',query)
        with open(str(query)+'.json', 'w') as f:
            json.dump(res, f)

        return flask.jsonify(res)

@application.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == 'GET':
        # print(flask.request.args)
        query = flask.request.args.get('query')
        # print(flask.request.args.getlist('doc_imgs[]'))

        # print('get query'+query)
        imgs = flask.request.args.getlist('doc_imgs[]')
        # print(imgs)
        path=query
        # print('path is')
        # print(path)
        if not os.path.exists(path):
            os.mkdir(path)
        
        
        
        print('downloading pictures')
        for i in imgs:
            img_name=re.search(pattern='[0-9a-z]*.jpg',string=i).group()
            # print('/'+path+'/'+img_name)  
            req.urlretrieve(i, path+'/'+img_name)
        return  "susscess"




if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8080, debug=True,use_reloader=True)