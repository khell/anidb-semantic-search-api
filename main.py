from flask import Flask, request
from anidb_query_tool import AnidbIdQueryTool
from logger import logger

app = Flask(__name__)
if __name__ != '__main__':
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

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
