"""from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)



game_state = {
    'question': '',
    'players': {
        'P1': {'score': 0},
        'P2': {'score': 0}
    },
    'J_log': []
}

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    
    game_state['question'] = ''
    game_state['players']['P1']['score'] = 0
    game_state['players']['P2']['score'] = 0
    game_state['J_log'] = []
    
   
    game_state['question'] = 'When was the war of 1812?'
    return render_template('submit_answer.html')

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    player_name = request.form.get('player')
    answer = request.form.get('answer')
    
    if answer == 'June 18, 1812':
        game_state['players'][player_name]['score'] += 1
        game_state['J_log'].append(f"[{get_current_time()}] {player_name} answered correctly.")
        return 'OK'
    else:
        game_state['J_log'].append(f"[{get_current_time()}] {player_name} answered incorrectly.")
    
    
    if len(game_state['J_log']) >= 4:
        return 'NO'
    
    return 'Waiting for other player'

def get_current_time():
    
    return datetime.now().strftime('%H:%M:%S')

if __name__ == '__main__':
    app.run()
"""

from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

class Game:
    def __init__(self, p1, p2, J, max_attempts, max_points):
        self.p1 = p1
        self.p2 = p2
        self.J = J
        self.max_attempts = max_attempts
        self.max_points = max_points
        self.p1_score = max_points
        self.p2_score = max_points
        self.current_question = None
        self.attempts = 0
        self.log = []

    def start_question(self, question):
        self.current_question = question
        self.attempts = 0

    def submit_answer(self, player, answer):
        if self.current_question is None:
            return "No active question."
        
        if self.attempts >= self.max_attempts:
            return "Maximum attempts reached."
        
        self.attempts += 1
        
        if player == self.p1:
            if answer == self.current_question:
                self.p1_score += 1
                self.log.append([datetime.datetime.now(), player, answer, "OK"])
                return "Correct answer! Player 1 gets 1 point."
            else:
                self.log.append([datetime.datetime.now(), player, answer, "NO"])
                return "Incorrect answer. Player 1 has {} attempts remaining.".format(
                    self.max_attempts - self.attempts
                )
        
        elif player == self.p2:
            if answer == self.current_question:
                self.p2_score += 1
                self.log.append([datetime.datetime.now(), player, answer, "OK"])
                return "Correct answer! Player 2 gets 1 point."
            else:
                self.log.append([datetime.datetime.now(), player, answer, "NO"])
                return "Incorrect answer. Player 2 has {} attempts remaining.".format(
                    self.max_attempts - self.attempts
                )
        
        else:
            return "Invalid player."

    def restart_game(self):
        self.p1_score = self.max_points
        self.p2_score = self.max_points
        self.current_question = None
        self.attempts = 0
        self.log.clear()


game = None

@app.route("/", methods=["GET", "POST"])
def index():
    global game

    if request.method == "POST":
        if "start_game" in request.form:
            player1 = request.form["p1"]
            player2 = request.form["p2"]
            judge = request.form["judge"]
            max_points = int(request.form["max_points"])
            max_attempts = int(request.form["max_attempts"])

            game = Game(player1, player2, judge, max_attempts, max_points)

        elif "submit_answer" in request.form:
            player = request.form["player"]
            answer = request.form["answer"]
            result = game.submit_answer(player, answer)
            return render_template("index.html", game=game, result=result)

        elif "restart_game" in request.form:
            game.restart_game()

    if game and not game.current_question:
        game.start_question("Where is the Alamo?")

    return render_template("index.html", game=game, result=None)



if __name__ == "__main__":
    app.run(debug=True)
