from flask import Flask, render_template, request
import pandas as pd


app = Flask(__name__)



'''The Public Good Game is a social dilemma game where multiple players
have to decide whether to contribute their own resources to a shared 
public good or to keep them for themselves. In this case, the game involves 
four contributors and one judge, and each contributor starts with 20 units 
of resources. The contributors can choose how much to contribute to the 
public good, and their contributions
will be multiplied by two and divided among all four contributors.'''

@app.route('/humen', methods=['GET','POST'])
def human():
    player = 1
    if request.method == 'POST':
        punished_by = request.form.get('pns')
        contribution = request.form.get('money')
        num_player = request.form.get('player')
        
    return render_template('humen.html')

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)