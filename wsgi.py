# fmt: off
from gevent import monkey; monkey.patch_all() # this will make the app async # noqa: E702 
import psycogreen.gevent; psycogreen.gevent.patch_psycopg() # noqa: E702
# fmt: on

from dotenv import load_dotenv

from app.app import create_app


load_dotenv()

app = create_app("production")
