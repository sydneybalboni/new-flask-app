from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
import random

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/start', methods=['GET'])
def start_game():
    session['number'] = random.randint(1, 100)  # Random number between 1 and 100
    session['attempts'] = 0
    session['is_active'] = True
    session['guess_history'] = []
    return jsonify({'message': 'Game started! Guess a number between 1 and 100.'})

@app.route('/guess', methods=['POST'])
def guess():
    if not session.get('is_active'):
        return jsonify({'message': 'Start a new game first.'})
    
    data = request.get_json()
    guess = data.get('number')
    session['attempts'] += 1
    
    session['guess_history'].append(guess)
    
    if guess < session['number']:
        return jsonify({'message': 'Too low!', 'attempts': session['attempts'], 'history': session['guess_history']})
    elif guess > session['number']:
        return jsonify({'message': 'Too high!', 'attempts': session['attempts'], 'history': session['guess_history']})
    else:
        session['is_active'] = False
        return jsonify({'message': 'Congratulations! You guessed it right.', 'attempts': session['attempts'], 'history': session['guess_history']})

@app.route('/status', methods=['GET'])
def status():
    if session.get('is_active'):
        return jsonify({'message': 'Game is in progress.', 'attempts': session['attempts'], 'history': session['guess_history']})
    else:
        return jsonify({'message': 'Game is not active. Start a new game.', 'history': session['guess_history']})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Set debug to False for production


