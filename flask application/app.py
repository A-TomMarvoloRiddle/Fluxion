from flask import Flask, render_template, jsonify
from weather.vc import start_system

app = Flask(__name__)

@app.route('/get_state', methods=['GET'])
def get_system_state():
    state = {
        'green_light_times': start_system()
    }
    return jsonify(state)

# Flask route for the web interface
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/data')
def data():
    return render_template('data.html')
@app.route('/video')
def video():
    return render_template('video.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
