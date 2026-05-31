from flask import Flask, render_template, request, jsonify
from tracker import PoseTracker
from game import GameEngine, StatsRecorder
import threading

app = Flask(__name__)
tracker = PoseTracker()
stats = StatsRecorder()
game = GameEngine(stats)

lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    with lock:
        return jsonify(game.to_dict())

@app.route('/detect', methods=['POST'])
def detect():
    image_bytes = request.get_data()
    if not image_bytes:
        return jsonify({'success': False, 'message': 'No image data received.'}), 400
    label = tracker.process_image(image_bytes)
    if label:
        with lock:
            game.handle_action(label)
    return jsonify({'success': True, 'label': label or 'no_pose'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
