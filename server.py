from flask import Flask, send_from_directory
from flask_cors import CORS
import en_core_web_sm
import json
from travelrec.recommendations_pipeline import recommendations_pipeline

app = Flask(__name__)
CORS(app)

nlp = en_core_web_sm.load()

debug = True

@app.route('/api/recommendations/<query>')
def api_recommendations(query):
    recs = recommendations_pipeline(query, nlp, debug)
    return json.dumps(recs)

@app.route('/app/<path:path>', methods=['GET'])
def app_path(path):
    return send_from_directory('travelrec-web/dist/travelrec-web/', path)

@app.route('/app/')
def app_path_index():
    return send_from_directory('travelrec-web/dist/travelrec-web/', 'index.html')

if __name__ == "__main__":
    app.run(debug=debug)
