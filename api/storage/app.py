from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

DDOWNLOAD_API_KEY = '386789puyv5r8kkoors0tz'
DDOWNLOAD_API_ENDPOINT = 'https://api-v2.ddownload.com/api/upload/server'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        response = requests.get(f"{DDOWNLOAD_API_ENDPOINT}?key={DDOWNLOAD_API_KEY}")
        if response.status_code == 200:
            data = response.json()
            if 'result' in data:
                server_url = data['result']
                sess_id = data['sess_id']
                return render_template('upload.html', server_url=server_url, sess_id=sess_id)
            else:
                return jsonify({'msg': 'No server available', 'status': response.status_code})
        else:
            return jsonify({'msg': 'Error', 'status': response.status_code})
    except Exception as e:
        return jsonify({'msg': str(e), 'status': 500})

@app.route('/submit', methods=['POST'])
def submit():
    try:
        endpoint = request.form.get('endpoint')
        sess_id = request.form.get('sess_id')
        utype = request.form.get('utype', 'prem')
        file = request.files['file']
        response = requests.post(endpoint, data={'sess_id': sess_id, 'utype': utype}, files={'file': file})
        if response.status_code == 200:
            upload_response = response.json()
            return jsonify(upload_response)
        else:
            return jsonify({'msg': 'Error', 'status': response.status_code})
    except Exception as e:
        return jsonify({'msg': str(e), 'status': 500})

if __name__ == '__main__':
    app.run(debug=True)
