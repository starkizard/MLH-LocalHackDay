from flask import Flask, render_template
import chess
import chess.engine

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    global engine
    print(depth)
    print("Calculating...")
    board = chess.Board(fen)
    result = engine.play(board, chess.engine.Limit(depth=depth))
    print("Move found!", result.move)
    print()
    return str(result.move)


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester


if __name__ == '__main__':
    engine = chess.engine.SimpleEngine.popen_uci("/home/starkizard/botIntegration/BetaZeroV2Code/./BetaZero")
    app.run(debug=True)