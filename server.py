import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import credentials
import spotipy
from flask import Flask, request
import os

port = 8080
redirectURI = "https://gqp7jsnrfr.us-east-1.awsapprunner.com:8080/callback"
#authManager = SpotifyClientCredentials(client_id=credentials.CLIENT_ID, client_secret=credentials.CLIENT_SECRET)
#sp = spotipy.Spotify(auth_manager=authManager)
sp_oauth = SpotifyOAuth(redirect_uri=redirectURI, client_id=credentials.CLIENT_ID,
                        client_secret=credentials.CLIENT_SECRET, scope='user-read-recently-played')

auth_url = sp_oauth.get_authorize_url()
app = Flask(__name__)
@app.route("/")
def hello_world():
    return f'<a href="{auth_url}">login to spotify!</a>'

@app.route('/callback')
def callback():
    tracklist = []
    authorization_code = request.args.get('code')
    print(authorization_code)
    if authorization_code:
        # You have obtained the authorization code.
        print("Authorization Code:", authorization_code)
        access_token = sp_oauth.get_access_token(authorization_code,check_cache=False)
        print("Access Token:", access_token)
        sp = spotipy.Spotify()

        sp.set_auth(access_token['access_token'])
        results = sp.current_user_recently_played(limit=20)
        print(results)
        for item in results['items']:
            track_name = item['track']['name']
            print("Name:", track_name)
            tracklist.append(track_name)
    return tracklist


@app.route('/hi')
def test():
    return "TEST"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)




# from wsgiref.simple_server import make_server
# from pyramid.config import Configurator
# from pyramid.response import Response
# import os
#
# def hello_world(request):
#     name = os.environ.get('NAME')
#     if name == None or len(name) == 0:
#         name = "world"
#     message = "Hello, " + name + "!\n"
#     return Response(message)
#
# if __name__ == '__main__':
#     port = int(os.environ.get("PORT"))
#     with Configurator() as config:
#         config.add_route('hello', '/')
#         config.add_view(hello_world, route_name='hello')
#         app = config.make_wsgi_app()
#     server = make_server('0.0.0.0', port, app)
#     server.serve_forever()