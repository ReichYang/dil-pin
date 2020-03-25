import flask
from flask import Flask, redirect, url_for, request,session, jsonify, flash
from datetime import datetime
import re, sys,os, json
from flask import render_template
import Pinterest
import urllib.request as req
# from flask_fontawesome import FontAwesome
import vision_functions
import os, shutil
import zipfile
from http import HTTPStatus
from flask import Flask
from werkzeug.exceptions import HTTPException, NotFound
import werkzeug, time

app = Flask(__name__)
app.secret_key = os.urandom(12)

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/")
def index():
    return render_template("login.html")

@app.route('/back')
def back():
    return render_template("user.html",data=flask.current_app.user_info)

@app.route('/login', methods=['POST', 'GET'])
def login(data=None):
    if request.method == 'POST':
        user = request.form['username']
        email=request.form['email']
        pw = request.form['password']
        # print(user, file=sys.stdout)
        pint = Pinterest.Pinterest(username=user,email=email, password=pw)
        flask.current_app.account= pint
        try:
            login_sts= pint.login()
            flask.current_app.loginsts= login_sts
            user_info= pint.get_user_overview()
            flask.current_app.user_info= user_info
        # except:
        #     return render_template('login.html',error=404)

            if(login_sts.status_code==200):
                session['username']=user
                session['password']=pw
                session['email']=email
                return render_template("user.html",data=user_info)
        except Exception as inst: 
            # print("priting error")
            # print(inst)
            # print('printing the code')
            print(inst.args)
            if (inst.args[0][:3]=='401'):
                return render_template('login.html',error='401')
            elif(inst.args[0][:3]=='404'):
                return render_template('login.html',error='404')
            elif (inst.args[0][:3]=='429'):
                return render_template('login.html',error='429')
        # print(login_sts.status_code, file=sys.stdout)
        # print(pint.get_user_overview(), file=sys.stdout)
        # print(flask.current_app.account)
        # try:
        # user_info= pint.get_user_overview()
        # flask.current_app.user_info= user_info
        # except:
        #     return render_template('login.html',error=404)

        # if(login_sts.status_code==200):
        #     session['username']=user
        #     session['password']=pw
        #     session['email']=email
        #     return render_template("user.html",data=user_info)


    if request.method == 'GET':
        
        query = flask.request.args.get('query')
        # current_account = flask.g.get('current')
        current_account=flask.current_app.account
        # print(current_account)
        res = []
        search_batch = current_account.search('pins', query)
        while len(search_batch) > 0 and len(res) < 100:
            res += search_batch
            search_batch = current_account.search('pins', query=query)
        # res=current_account.search('pins',query)

        flask.current_app.current_res=res

       

        return flask.jsonify(res)
    else :
        return render_template("user.html",data=flask.current_app.user_info)

@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == 'POST':
        query = request.form['query']
        imgs = request.form.getlist('doc_imgs[]')

        path=query
        path=path.replace(" ","_")
        time=datetime.now().strftime('%Y%m%d%H%M%S')
        print(path)
        user_name = flask.current_app.user_info['username']

        print("now entering the download path")

        # print(request.form)
        # print(user_name)


        
        if not os.path.exists('static/Pics'):
            os.mkdir('static/Pics')

        FOLDER_NAME = user_name+'_'+path+"_"+time
    
        ORIG_PATH = 'static/Pics/' + FOLDER_NAME
        NEWPATH = ORIG_PATH
        # n = 0
        # while os.path.exists(NEWPATH):
        #     n = n+1
        #     NEWPATH = ORIG_PATH + '_' + str(n)

        os.mkdir(NEWPATH)
        
        JS_ORIG_PATH = 'static/Jsons/' + FOLDER_NAME+ '.json'
        JS_NEWPATH = JS_ORIG_PATH
        # n = 0
        # while os.path.exists(NEWPATH):
        #     n = n+1
        #     NEWPATH = 'static/Jsons/' + str(flask.current_app.user_info['username'])+ '_' + str(query)+ '_' + str(n)+'.json'

        with open(JS_NEWPATH, 'w') as f:
            json.dump(flask.current_app.current_res, f)


        print('downloading pictures')
        for i in imgs:
            img_name=re.search(pattern='[0-9a-z]*.jpg',string=i).group()
            # print('/'+path+'/'+img_name)  
            req.urlretrieve(i, NEWPATH+'/'+img_name)
        print('download succes')


         #if file already exists
        

        return  "susscess"


@app.route('/account', methods=['POST', 'GET'])
def account():
    if request.method == 'GET':
        user_info = flask.current_app.user_info

        with open(user_info['username']+'.json', 'w') as f:
            json.dump(user_info, f)
        print('account info')
        return flask.send_file(user_info['username']+'.json', attachment_filename= user_info['username']+'.json', as_attachment = True)

@app.route('/down_account', methods=['POST', 'GET'])
def down_account():
    user_info = flask.current_app.user_info
    console.log('downaccount')
    return flask.send_file(user_info['username']+'.json', attachment_filename= user_info['username']+'.json', as_attachment = True)


@app.route('/analysis', methods=['POST','GET'])
def analysis():
    if request.method == 'GET':
        user_info = flask.current_app.user_info
        dirs=os.listdir('static/Pics')
        new_dirs = []
        for folder in dirs:
            if folder.startswith(user_info['username']):
                new_dirs.append(folder)

        return render_template('analysis.html',data=new_dirs)


@app.route('/download_folder', methods=['POST'])
def download_folder():
    if request.method == 'POST':
         folder = request.form['folder']
         folder= folder.strip()
         print(folder)

         filename= folder+'.zip'
         print(filename)
         zipf = zipfile.ZipFile(filename,'w', zipfile.ZIP_DEFLATED)

         for root,dirs, files in os.walk('static/Pics/'+folder):
             for file in files:
                 zipf.write('static/Pics/'+folder+'/'+file)
        
         zipf.write('static/Jsons/'+folder+".json")
         zipf.close()
         print('sending file')
         return flask.send_file(filename, mimetype = 'zip',attachment_filename= folder+'.zip', as_attachment = True)


@app.route('/download_analysis_res', methods=['POST'])
def download_analysis_res():
    if request.method == 'POST':
         folder = request.form['folder']
         folder= folder.strip()
         print(folder)

         filename= folder+'_analysis'+'.zip'
         print(filename)
         zipf = zipfile.ZipFile(filename,'w', zipfile.ZIP_DEFLATED)

         for root,dirs, files in os.walk('static/image_outputs/'+folder):
             for file in files:
                 zipf.write('static/image_outputs/'+folder+'/'+file)
         zipf.close()
         print('sending file')
         return flask.send_file(filename, mimetype = 'zip',attachment_filename= folder+'.zip', as_attachment = True)
         
@app.route('/get_folder', methods=['GET'])
def get_folder():
     if request.method == 'GET':
         
         folder = flask.request.args.get('name')
         folder= folder.strip()
         res={}
         res['summary']=os.stat('static/Pics/'+folder)
         res['array']=os.listdir('static/Pics/'+folder)
         flask.current_app.folder_name = folder

        

        # So the variable res['array'] contains all the file names you need to use.
        # You could continue coding from here
        # This method should generate things that could possibly return to the html page (analysis.html)


         return jsonify(result=res)

@app.route('/getfile', methods=['GET'])
def getfile():
    if request.method == 'GET':
        return "success"

# ANALYSIS BUTTON
@app.route('/run_analysis', methods=['GET'])
def run_analysis():
    if request.method == 'GET':
        STOP_WORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',"you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself','yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her','hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them','their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom','this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are','was', 'were', 'be', 'been', 'being', 'have', 'has', 'had','having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and','but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at','by', 'for', 'with', 'about', 'against', 'between', 'into','through', 'during', 'before', 'after', 'above', 'below', 'to','from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under','again', 'further', 'then', 'once', 'here', 'there', 'when','where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more','most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own','same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will','just', 'don', "don't", 'should', "should've", 'now', 'd', 'll','m', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn',"couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma','mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't",'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        FOLDER_NAME = flask.request.args.get('name')

        #TRIM WHITESPACE
        FOLDER_NAME = FOLDER_NAME.strip()

        SEARCH_TERM= str(re.split('_', FOLDER_NAME)[1])
        # USER_NAME = flask.current_app.user_info['username']
        # print(SEARCH_TERM + ' SEARCH TERM')
        # print(USER_NAME + ' current user')

        #GOOGLE_CRED = "static/uploads/" + USER_NAME + "_key.json"

        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= GOOGLE_CRED
        print(str(FOLDER_NAME) + ' FOLDER NAME')

        # make list of image paths
        img_paths = []

        MAX = 15
        i = 1
        directory = os.fsencode('static/Pics/' + FOLDER_NAME)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if (filename.endswith(".jpg") & (i <= MAX)): 
                img_str = 'static/Pics/' + FOLDER_NAME+ '/'+ str(filename)
                img_paths.append(img_str)
                i = i +1

        print(len(img_paths))
        print('paths gathered')
        # the picture folder name will only be 'static/image_outputs/FOLDER_NAME


        ORIG_PATH = 'static/image_outputs/' + FOLDER_NAME
        NEWPATH = ORIG_PATH
        # n = 0
        if not os.path.exists(NEWPATH):
            os.makedirs(NEWPATH)

        # LABEL WORDCLOUD
        #label_lists = vision_functions.get_label_lists(img_paths)
        #wordcloud = vision_functions.get_wordcloud(label_lists, SEARCH_TERM)
        #wordcloud.to_file(NEWPATH + '/label_wordcloud_' + FOLDER_NAME + '.png')
        #print('label_wordcloud saved')

        # LABEL COSSIM
        #label_vectors = vision_functions.get_label_vectors(label_lists)
        #label_avg_cossim = str(vision_functions.get_avg_cosine_sim(label_vectors))
        #text_file = open((NEWPATH + "/label_cossim_" + FOLDER_NAME + ".txt"), "w")
        #text_file.write("%s" % label_avg_cossim)
        #text_file.close()
        #print('label cossim saved')

        # DESCRIPTION WORDCLOUD
        # if (n==0):
        #     json_path = 'static/Jsons/' + FOLDER_NAME + '.json'
        # else:
        json_path = 'static/Jsons/' + FOLDER_NAME + '.json'

        
        json_dict = vision_functions.get_json_dict(json_path)
        descripts = vision_functions.get_descripts(json_dict)
        STOP_WORDS.append(SEARCH_TERM)
        wordcloud = vision_functions.get_desc_wordcloud(descripts, STOP_WORDS)
        wordcloud.to_file(NEWPATH + '/description_wordcloud_' + FOLDER_NAME + '.png')
        print('decription_wordcloud saved')

        # DESCR COSSIM
        desc_vectors = vision_functions.get_label_vectors(descripts)
        desc_avg_cossim = str(vision_functions.get_avg_cosine_sim(desc_vectors))
        text_file = open((NEWPATH + "/descript_cossim_" + FOLDER_NAME + ".txt"), "w")
        text_file.write("%s" % desc_avg_cossim)
        text_file.close()
        print('description cossim saved')

        # DOMAIN WORDCLOUD
        domains = vision_functions.get_domains(json_dict)
        wordcloud = vision_functions.get_wordcloud(domains, SEARCH_TERM)
        wordcloud.to_file(NEWPATH + '/domian_wordcloud_' + FOLDER_NAME + '.png')
        print('domain_wordcloud saved')

        # DOMAIN COSSIM
        domain_vectors = vision_functions.get_label_vectors(domains)
        domain_avg_cossim = str(vision_functions.get_avg_cosine_sim(domain_vectors))
        text_file = open((NEWPATH + "/domain_cossim_" + FOLDER_NAME + ".txt"), "w")
        text_file.write("%s" % domain_avg_cossim)
        text_file.close()
        print('domain cossim saved')

        # BOARD WORDCLOUD
        boards = vision_functions.get_boards(json_dict)
        wordcloud = vision_functions.get_wordcloud(boards, SEARCH_TERM)
        wordcloud.to_file(NEWPATH + '/board_wordcloud_' + FOLDER_NAME + '.png')
        print('board_wordcloud saved')

        # BOARD COSSIM
        boards_vectors = vision_functions.get_label_vectors(boards)
        boards_avg_cossim = str(vision_functions.get_avg_cosine_sim(boards_vectors))
        text_file = open((NEWPATH + "/board_cossim_" + FOLDER_NAME + ".txt"), "w")
        text_file.write("%s" % boards_avg_cossim)
        text_file.close()
        print('board cossim saved')

        # PROMOTER WORDCLOUD
        promoters = vision_functions.get_promoters(json_dict)
        wordcloud = vision_functions.get_wordcloud(promoters, SEARCH_TERM)
        wordcloud.to_file(NEWPATH + '/promoter_wordcloud_' + FOLDER_NAME + '.png')
        print('promoter_wordcloud saved')

        # PROMOTER COSSIM
        prom_vectors = vision_functions.get_label_vectors(promoters)
        prom_avg_cossim = str(vision_functions.get_avg_cosine_sim(prom_vectors))
        text_file = open((NEWPATH + "/promoter_cossim_" + FOLDER_NAME + ".txt"), "w")
        text_file.write("%s" % prom_avg_cossim)
        text_file.close()
        print('promoter cossim saved')

        # CREATED AT GRAPH
        dates = vision_functions.get_dates(json_dict)
        date_fig = vision_functions.get_date_graph(dates)
        date_fig.savefig(NEWPATH + "/date_graph_" + FOLDER_NAME + ".png")
        print('date graph saved')

        # DETECT COLOR PROPERTIES
        # df_list = []
        # for path in img_paths:
        #     df_list.append(vision_functions.get_properties_df(path))

        # prop_json = str(vision_functions.get_properties_json(df_list))
        # intro_str = """Highcharts.chart('container', {chart: {type: 'packedbubble',height: '80%'},title: {text: 'Simple packed bubble'},tooltip: {useHTML: true,pointFormat: '<b>{point.name}:</b> {point.y}</sub>'},plotOptions: {packedbubble: {dataLabels: {enabled: true,format: '{point.name}',style: {color: 'black',textOutline: 'none',fontWeight: 'normal'}},minPointSize: 0}},series: ["""
        # full_str = intro_str + prop_json + ']});'
        # text_file = open((NEWPATH + "/color_json_" + FOLDER_NAME + ".js"), "w")
        # text_file.write(full_str)
        # text_file.close()
        print('properties json saved')
        print('analysis complete')

        returns = []
        #returns.append(NEWPATH + '/label_wordcloud_' + FOLDER_NAME + '.png')
        returns.append(NEWPATH + '/description_wordcloud_' + FOLDER_NAME + '.png')
        returns.append(NEWPATH + '/domian_wordcloud_' + FOLDER_NAME + '.png')
        returns.append(NEWPATH + '/board_wordcloud_' + FOLDER_NAME + '.png')
        returns.append(NEWPATH + '/promoter_wordcloud_' + FOLDER_NAME + '.png')
        returns.append(NEWPATH + "/date_graph_" + FOLDER_NAME + ".png")

        
        print('ready to send the thing')
        print(returns)
        # return flask.jsonify(res=returns)
        return flask.jsonify(res=returns)


# @app.route('/showana',methods=['GET']
# def showana():
#     if request.method == 'GET':


####
#UPLOAD CODE
####

ALLOWED_EXTENSIONS = set(['json'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = flask.current_app.user_info['username'] + '_key.json'
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/analysis')
		else:
			flash('Allowed file type is .json')
			return redirect('/analysis')




if __name__ == '__main__':
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host="0.0.0.0", port=8080,debug=True, use_reloader=True)