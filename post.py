import sys
import config
from pytumblr import TumblrRestClient

client = TumblrRestClient(config.consumer_key, config.consumer_secret,
                          config.oauth_token, config.oauth_secret)
client.create_text(config.blogname, body=sys.stdin.read())
