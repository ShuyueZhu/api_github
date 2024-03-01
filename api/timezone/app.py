from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

WORLD_TIME_API_URL = 'http://worldtimeapi.org/api/timezone/'
API_KEY = 'fRucZ9ARZX'  # 这是你的 API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_time', methods=['POST'])
def get_time():
    city = request.form['city']
    try:
        response = requests.get(f"{WORLD_TIME_API_URL}{city}", params={'token': API_KEY})
        if response.status_code == 200:
            time_info = response.json()
            return jsonify(time_info)
        else:
            return jsonify({'msg': 'Error', 'status': response.status_code})
    except Exception as e:
        return jsonify({'msg': str(e), 'status': 500})

if __name__ == '__main__':
    app.run(debug=True)
