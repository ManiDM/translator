import os
import pathlib
from flask_dance.contrib.github import make_github_blueprint, github
import requests
from flask import Flask, session, abort, redirect, request, url_for, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask("Free API Translator")
app.secret_key = "freeapitranslator"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

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
def login():
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
    session['picture'] = id_info.get("picture")
    # return id_info
    return redirect("/protected_area")

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
            session['git_name'] = account_info_json['login']
            session["name"] = account_info_json['name']
            session['avatar_url'] = account_info_json['avatar_url']
            return redirect("/protected_area")
    return abort(500)

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

@app.route("/login")
def index():
    is_login = False
    return "<a href='/login_google'><button>Google Login</button></a><br><a href='/github_login'><button>Github Login</button></a>"

@app.route("/protected_area")
# @login_is_required
def protected_area():

    if "google_id" in session:
        return render_template("img.html", user_name=session['name'], avatar=session['picture'])
    elif "git_name" in session:
        if "name" in session:
            return render_template("img.html", user_name=session['name'], avatar=session['avatar_url'])
        return render_template("img.html", user_name=session['git_name'], avatar=session['avatar_url'])

if __name__ == "__main__":
    app.run(debug=True, port=5001)