import sys
from requests_oauthlib import OAuth1Session
import config

API_ROOT = 'https://api.tumblr.com/v2/'

client = OAuth1Session(
    client_key=config.consumer_key,
    client_secret=config.consumer_secret,
    resource_owner_key=config.oauth_token,
    resource_owner_secret=config.oauth_secret)
client.post(
    f'{API_ROOT}/blog/{config.blogname}/posts',
    json={
        'content': [{
            'type': 'text',
            'text': sys.stdin.read()
        }],
        'send_to_twitter': True
    })
