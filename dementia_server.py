from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    return "Dementia Server access succeed"

app.run(host="0.0.0.0", port=5000, debug=True)
