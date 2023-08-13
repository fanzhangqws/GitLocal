from app import app
from api import app as app2
import logging
import json

# with open('logging.json', 'r') as f:
#     logging.config.dictConfig(json.load(f))

app.run(host="0.0.0.0", port=8088, debug=True)
# app2.run(host="0.0.0.0", port=8087, debug=True)
