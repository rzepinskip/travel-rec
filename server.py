from flask import Flask, send_from_directory
import en_core_web_sm
import json
from travelrec.recommendations_pipeline import recommendations_pipeline

app = Flask(__name__)

nlp = en_core_web_sm.load()

debug = True

@app.route('/api/recommendations/<query>')
def api_recommendations(query):
    recs = recommendations_pipeline(query, nlp, debug)
    return json.dumps(recs)

@app.route('/app/<path:path>')
def app_path(path):
    print(path)
    return send_from_directory('web', path)

if __name__ == "__main__":
    app.run(debug=debug)
