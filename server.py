import spotipy.oauth2
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from flask import Flask, request


# CLIENT_ID = "679be63979e04cc496a45c75d2afa493"
# CLIENT_SECRET = "6ecdc388b44a4c4fb9adf33afb833fb9"
port = 8000
# redirectURI = "http://127.0.0.1:5000/callback"
# sp_oauth = SpotifyOAuth(redirect_uri=redirectURI, client_id=CLIENT_ID,
#                         client_secret=CLIENT_SECRET, scope='user-read-recently-played')
#
# auth_url = sp_oauth.get_authorize_url()
auth_url = 'youtube.com'
app = Flask(__name__)
@app.route("/")
def hello_world():
    return f'<a href="{auth_url}">login to spotify!</a>'

# @app.route('/callback')
# def callback():
#     tracklist = []
#     authorization_code = request.args.get('code')
#     print(authorization_code)
#     if authorization_code:
#         #print("Authorization Code:", authorization_code)
#         access_token = sp_oauth.get_access_token(authorization_code,check_cache=False)
#         #print("Access Token:", access_token)
#         sp = spotipy.Spotify()
#
#         sp.set_auth(access_token['access_token'])
#         results = sp.current_user_recently_played(limit=20)
#         #print(results)
#         for item in results['items']:
#             track_name = item['track']['name']
#             #print("Name:", track_name)
#             tracklist.append(track_name)
#     return tracklist

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

