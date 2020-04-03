from flask import Flask, render_template, request
import build
import os

app = Flask(__name__, template_folder='./', static_folder="", static_url_path="")

@app.route('/')
@app.route('/index')
def generate_website():
    mods = set()
    enmods = set()
    optionals = set()
    mods.update(["mods/" + file for file in os.listdir('mods')])
    enmods.update(["en-mods/" + file for file in os.listdir('en-mods')])
    optionals.update(["optional/" + file for file in os.listdir('optional')])
    return render_template("./index.html", mods = mods, enmods = enmods, optionals = optionals)

@app.route('/ajax',methods=['POST'])
def ajax():
    recv_data = request.get_data()
    print(recv_data)
    return recv_data

if __name__ == '__main__':
    app.run(debug=True)