from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, json, make_response
import build
import os
import json

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
    recv_data = json.loads(request.get_data('data'))
    result = build.build(recv_data)
    message = {"code": 200, "argument": recv_data, "logs": result[1], "filename": result[0]}
    print(recv_data)
    return json.dumps(message)

@app.route('/files/<file_name>', methods=['GET'])
def get_file(file_name):
    directory = "./"
    try:
        response = make_response(send_from_directory(directory,file_name,as_attachment=True))
        return response
    except Exception as e:
        return(jsonify({"code":"403", "message": "{}".format(e)}))

if __name__ == '__main__':
    app.run(debug=True)