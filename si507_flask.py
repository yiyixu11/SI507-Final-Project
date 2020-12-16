from flask import Flask, render_template, request
import sqlite3

# DB_name = 'final_project_DB.sqlite'

app = Flask(__name__)

def get_results_by_state(state):
    conn = sqlite3.connect('/Users/yiyixu/Desktop/SI507_final_project/final_project_DB.sqlite')
    cur = conn.cursor()
    q = "SELECT SpeciesName, SpeciesCode, Location, Date, HowMany FROM Obs WHERE State="
    extend = "'" + state + "'"
    results = cur.execute(q + extend).fetchall()
    conn.close()
    return results

def get_bird_info(code):
    conn = sqlite3.connect('/Users/yiyixu/Desktop/SI507_final_project/final_project_DB.sqlite')
    cur = conn.cursor()
    q = "SELECT Name, Description FROM Birds JOIN Obs ON Birds.Name = Obs.SpeciesName WHERE Obs.SpeciesCode="
    extend = "'" + code + "'"
    results = cur.execute(q + extend).fetchone()
    conn.close()
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    state = request.form["state"]
    results = get_results_by_state(state)
    return render_template('results.html', state=state, results=results)


@app.route('/results/info', methods=['POST'])
def info():
    codes = request.form["code"].replace(' ', '').split(',')
    l = []
    for code in codes:
        result = get_bird_info(code)
        l.append([result, code])
    return render_template('birds.html',  l=l)

if __name__ == '__main__':
    app.run(debug=True)

