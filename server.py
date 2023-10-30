import spotipy.oauth2
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from flask import Flask, request, session, render_template


CLIENT_ID = "679be63979e04cc496a45c75d2afa493"
CLIENT_SECRET = "6ecdc388b44a4c4fb9adf33afb833fb9"
port = 5000
#port = 8000
redirectURI = "https://wfbjw6avrv.us-east-1.awsapprunner.com/callback"
#redirectURI = "http://127.0.0.1:8000/callback"
sp_oauth = SpotifyOAuth(redirect_uri=redirectURI, client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET, scope='user-read-recently-played user-top-read')

auth_url = sp_oauth.get_authorize_url()
sp = spotipy.Spotify()
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
@app.route("/")
def hello_world():
    return f'<a href="{auth_url}">login to spotify test 2!</a>'


@app.route('/callback')
def callback():
     tracklist = []
     authorization_code = request.args.get('code')
     session['authorization_code'] = authorization_code
     if authorization_code:
         access_token = sp_oauth.get_access_token(authorization_code,check_cache=False)
         sp.set_auth(access_token['access_token'])
         session['session_access_token'] = access_token['access_token']
     return render_template("top_track.html")

def getTopTrack(term):
    print("Sessiontest", session['session_access_token'])
    sp.set_auth(session['session_access_token'])
    topTracks = sp.current_user_top_tracks(limit=10, time_range=term)
    return topTracks


@app.route('/toptracks', methods=['GET', 'POST'])
def topTracks():
    access_token = session['access_token']
    if not access_token:
        authorization_code = session['authorization_code']
        if authorization_code:
            access_token = sp_oauth.get_access_token(authorization_code, check_cache=False)
            sp.set_auth(access_token['access_token'])
            session['session_access_token'] = access_token['access_token']
    topTrack = []
    tracklist = []
    if request.method == 'POST':
        topTrack = getTopTrack(request.form.get('action'))  # do something
        for item in topTrack['items']:
            print(item)
            track_name = item['name']
            tracklist.append(track_name)
        return render_template('result.html', tracknamelist=tracklist)
    elif request.method == 'GET':
        return render_template('top_track.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)




