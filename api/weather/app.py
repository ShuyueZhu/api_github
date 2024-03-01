from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = 'http://api.weatherstack.com/'
API_KEY = '2f12d2ddfd1ff996ea97b0a97e1b0f05'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/current_weather', methods=['POST'])
def current_weather():
    city = request.form['city']
    response = requests.get(f"{BASE_URL}current?access_key={API_KEY}&query={city}").json()
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
