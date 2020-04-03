from flask import Flask, render_template
import build
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def generate_website():
    mods = set()
    enmods = set()
    optionals = set()
    mods.update(["mods/" + file for file in os.listdir('mods')])
    enmods.update(["mods/" + file for file in os.listdir('en-mods')])
    optionals.update(["optional/" + file for file in os.listdir('optional')])
    return render_template("index.html")

@app.route('/ajax',methods=['POST'])
def ajax():
    pass

if __name__ == '__main__':
    app.run(debug=True)