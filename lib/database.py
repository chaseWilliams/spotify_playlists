from flask import g
from redis import Redis
from urllib.parse import urlparse
import sys

def get_db():
    if not hasattr(g, 'db'):
        if len(sys.argv) > 1 and sys.argv[1] == 'debug':
            g.db = Redis()
        else:
            url = urlparse(os.environ.get('REDISCLOUD_URL'))
            g.db = Redis(host=url.hostname, port=url.port, password=url.password)

    return g.db