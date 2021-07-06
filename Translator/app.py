from flask import Flask, request, redirect, render_template, jsonify, session, abort, redirect, url_for
import json
# from flask_ngrok import run_with_ngrok
import main
import detect_language
import speech
import speech_to_text
import interpreter
import generate_api

# login
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import os
import pathlib
from flask_dance.contrib.github import make_github_blueprint, github
import requests
import sqlite3

conn = sqlite3.connect('api_db.db', check_same_thread=False)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app = Flask(__name__)
app = Flask("Free API Translator")
app.secret_key = "freeapitranslator"
# run_with_ngrok(app)

@app.route('/')
def index():
      
    if "git_id" in session:
      return render_template("testing.html", is_login=True, name=session["name"], avatar=session["avatar_url"])
    elif "google_id" in session:
      return render_template("testing.html", is_login=True, name=session["name"], avatar=session['picture'])
    else:
      return render_template("testing.html", is_login=False)

@app.route('/api')
def api():
    api_generated = conn.execute('''SELECT api from normal_clients where username = ?''',[session['username']]).fetchone()
    if "git_id" in session:
      return render_template("api.html", api_key=api_generated[0], avatar=session["avatar_url"])
    elif "google_id" in session:
      return render_template("api.html", api_key=api_generated[0], avatar=session['picture'])
    # api_generated = conn.execute('''SELECT api from normal_clients where username = ?''',[session['username']]).fetchone()
    # print(api_generated[0])
    # return render_template("api.html", api_key=api_generated[0], avatar=[if picture in session else avatar_url in session])
  
# @app.route('/signin')
# def signin():
#     api_generated = generate_api.generate()
#     return render_template("signin.html")

@app.route('/translate', methods = ['POST',"GET"])
def translate():
  form_data=request.get_json(force = True)
  ta_src_lang = form_data['ta_src_lang']
  src_lang = form_data['src_lang']
  if src_lang=="detect":
    candidate_langs = detect_language.detect_lang(ta_src_lang)
    # source_lang = candidate_langs[0]["language"]
    src_lang = candidate_langs
  dest_lang = form_data['dest_lang']
  # trans_text=ta_src_lang
  trans_text = main.translate(src_lang,dest_lang, ta_src_lang)
  response=json.dumps({"src_lang": src_lang,"dest_lang": dest_lang,"ta_src_lang": ta_src_lang,"ta_dest_lang":trans_text})
  return response


@app.route('/text_to_speech', methods = ['POST'])
def text_to_speech():
  form_data = request.get_json(force = True)
  dest_lang = form_data['dest_lang']
  ta_dest_lang = form_data['ta_dest_lang']
  path = speech.play_text(ta_dest_lang,dest_lang)
  response=json.dumps({"dest_lang": dest_lang,"ta_dest_lang":ta_dest_lang,"path":path})
  return response

@app.route('/text_to_speech_src', methods = ['POST'])
def text_to_speech_src():
  form_data = request.get_json(force = True)
  src_lng = form_data['src_lang']
  ta_src_lang = form_data['ta_src_lang']
  path = speech.play_text(ta_src_lang,src_lng)
  response=json.dumps({"dest_lang": src_lng,"ta_dest_lang":ta_src_lang,"path":path})
  return response

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']
      f.save(('uploads/file1.txt'))
      with open("uploads/file1.txt", "r") as f:
        content = f.readlines()
      # for i in content:
      #   content1 = main.translate(src_lang,dest_lang, ta_src_lang)
      return render_template('display_file.html', txt = content)

@app.route('/speechToText', methods = ['GET','POST'])
def speechToText():
  form_data=request.get_json(force = True)
  print(form_data)
  src_lang = form_data['src_lang']
  if src_lang=="detect":
    response=json.dumps({"error": "Choose a specific language to enable voice input"})
    return response
  print(src_lang)
  text_recognized = speech_to_text.speech_to_text(src_lang)
  # trans_text = main.translate(src_lang,dest_lang, ta_src_lang)
  response=json.dumps({"text_recognized": text_recognized})
  return response

@app.route('/manual_speech_src', methods = ['GET','POST'])
def manual_speech_src():
  form_data=request.get_json(force = True)
  # print(form_data)
  src_lang = form_data['src_lang']
  if src_lang=="detect":
    response=json.dumps({"error": "Choose a specific language to enable voice input"})
    return response
  dest_lang = form_data['dest_lang']
  text_recognized = speech_to_text.speech_to_text(src_lang)
  # trans_text = main.translate(src_lang,dest_lang, ta_src_lang)
  # if text_recognized==
  path = speech.play_text(text_recognized,dest_lang)
  response=json.dumps({"text_recognized": text_recognized})
  return response

@app.route('/manual_speech_trg', methods = ['GET','POST'])
def manual_speech_trg():
  form_data=request.get_json(force = True)
  # print(form_data)
  src_lang = form_data['src_lang']
  if src_lang=="detect":
    response=json.dumps({"error": "Choose a specific language to enable voice input"})
    return response
  dest_lang = form_data['dest_lang']
  text_recognized = speech_to_text.speech_to_text(dest_lang)
  # trans_text = main.translate(src_lang,dest_lang, ta_src_lang)
  path = speech.play_text(text_recognized,src_lang)
  response=json.dumps({"text_recognized": text_recognized})
  return response

@app.route('/text_ready', methods = ['POST','GET'])
def text_ready():
  form_data=request.get_json(force = True)
  print(form_data)
  src_lang = form_data['src_lang']
  dest_lang = form_data['dest_lang']
  src_interpreter_lang = interpreter.interpreter_lang_name(src_lang)
  trg_interpreter_lang = interpreter.interpreter_lang_name(dest_lang)
  src_interpreter_greet = interpreter.interpreter_lang_text(src_lang)
  trg_interpreter_greet = interpreter.interpreter_lang_text(dest_lang)

  print(src_interpreter_lang, trg_interpreter_lang, src_interpreter_greet, trg_interpreter_greet)
  response=json.dumps({"src_lang": src_lang,"dest_lang": dest_lang,'src_interpreter_lang':src_interpreter_lang, 'trg_interpreter_lang':trg_interpreter_lang,'src_interpreter_greet':src_interpreter_greet,'trg_interpreter_greet':trg_interpreter_greet})
  return response  

# Google Login setup
GOOGLE_CLIENT_ID = "838358975296-asom39nuri91fi7engvr02h5m3o52cl7.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5001/callback"
)

#Github Login setup
github_blueprint = make_github_blueprint(client_id='32ae764bdb60c0d2e0e6',
                                         client_secret='8f016eec05a8155a910dffe9e8d393f866a476e4')
app.register_blueprint(github_blueprint, url_prefix='/github_login')

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session or "git_name" not in session:
            return abort(401)   # Authorization required
        else:
            return function()
    return wrapper
  
@app.route("/login_google")
def login_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session['username'] = id_info.get("email")
    session['picture'] = id_info.get("picture")
    session['email'] = id_info.get("email")
    
    # return redirect('/')
    if conn.execute("SELECT 1 FROM normal_clients WHERE email = ?",[session['username']]).fetchone():
    # return id_info
        return redirect('/')
    else:
      generate_api.generate(session,'google')
      return redirect('/')
      

@app.route('/github_login')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        session.clear()
        if account_info.ok:
            account_info_json = account_info.json()
            session['git_id'] = account_info_json['id']
            session['name'] = account_info_json['name']
            session['username'] = account_info_json['login']
            session["email"] = account_info_json['email']
            session['avatar_url'] = account_info_json['avatar_url']
            print(session['username'])
            return account_info_json
            if conn.execute("SELECT 1 FROM normal_clients WHERE username = ?",[session['username']]).fetchone():
              return redirect('/')
            else:
              generate_api.generate(session,'github')
              return redirect('/')
    return abort(500)

@app.route("/logout")
def logout():
    session.clear()
    return "Your logged out"
    # return redirect("/")

@app.route("/protected_area")
# @login_is_required
def protected_area():

    if "google_id" in session:
        return redirect('/')
    elif "git_name" in session:
        return redirect('/')
      
@app.route("/login")
def login():
    return "<a href='/login_google'><button>Google Login</button></a><br><a href='/github_login'><button>Github Login</button></a>"

if __name__ == "__main__":
    app.run(debug=True, port=5001)
