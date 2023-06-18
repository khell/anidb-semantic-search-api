from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
from anidb_query_tool import AnidbIdQueryTool
from logger import logger
import os

app = Flask(__name__)
if __name__ != '__main__':
  app.logger.handlers = logger.handlers
  app.logger.setLevel(logger.level)

if (os.getenv("TRUST_X_FORWARDED", None)):
  proxy_depth = int(os.environ["TRUST_X_FORWARDED"])
  app.wsgi_app = ProxyFix(app.wsgi_app, x_for=proxy_depth)
  app.logger.info(f"Trusting proxy depth to {proxy_depth}")

tool = AnidbIdQueryTool()
tool.load_all()

@app.route('/api/anidb/id', methods=['GET'])
def get_anidb_id():
  name = request.args.get('name', None)
  if name is None:
    return { "error": "Missing query parameter `name` "}, 400
  
  match = tool.get_anidb_id(name)
  app.logger.info(f"[{request.remote_addr}] Matched `{name}` with {match}")
  return match, 200

@app.route('/healthcheck', methods=['GET'])
def get_healthcheck():
  return "OK", 200