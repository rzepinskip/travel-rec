from flask import Flask
import en_core_web_sm
import json
from travelrec.recommendations_pipeline import recommendations_pipeline

app = Flask(__name__)

nlp = en_core_web_sm.load()

@app.route('/api/recommendations/<query>')
def index(query):
    recs = recommendations_pipeline(query, nlp)
    return json.dumps(recs)

if __name__ == "__main__":
    app.run(debug=True)
