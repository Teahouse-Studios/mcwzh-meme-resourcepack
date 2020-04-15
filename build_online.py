from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, json, make_response
import build
import os
import time
import json
from threading import Lock
from pathlib import Path
import subprocess

app = Flask(__name__, template_folder='./views/',
            static_folder="static", static_url_path="/static")
app.config['TEMPLATES_AUTO_RELOAD'] = True
nt = 0
lock = Lock()


@app.route('/')
def generate_website():
    mods = set()
    enmods = set()
    optionals = set()
    figures = set()
    mods.update(["mods/" + file for file in os.listdir('mods')])
    enmods.update(["en-mods/" + file for file in os.listdir('en-mods')])
    optionals.update(["optional/" + str(file.relative_to('optional/').as_posix())
                      for file in Path('optional').iterdir() if not file.is_dir()])
    figures.update(["optional/" + str(file.relative_to('optional/').as_posix())
                    for file in Path('optional').iterdir() if file.is_dir()])
    header_existence = os.path.exists("./views/custom/header.html")
    footer_existence = os.path.exists("./views/custom/footer.html")
    return render_template("index.html", mods=list(mods), enmods=list(enmods), optionals=list(optionals),
                           figures=list(figures), header_existence=header_existence, footer_existence=footer_existence)


@app.route('/ajax', methods=['POST'])
def ajax():
    global nt
    lock.acquire(timeout=60)
    try:
        recv_data = json.loads(request.get_data('data'))
        logs = ""
        if nt + 60 <= time.time():
            nt = time.time()
            p = subprocess.Popen(["git", "pull", "origin", "master"],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
            p.wait()
            logs += str(p.communicate()[0], 'utf-8', 'ignore')
        else:
            logs += 'Skipping the repository update because there\'s an available cache within 60 seconds.\n'
        result = build.build(recv_data)
        logs += result[1]
        message = {"code": 200, "argument": recv_data,
                   "logs": logs, "filename": result[0]}
        print(recv_data)
    finally:
        lock.release()
    return json.dumps(message)


@app.route('/files/<file_name>', methods=['GET'])
def get_file(file_name):
    directory = "./"
    try:
        response = make_response(send_from_directory(
            directory, file_name, as_attachment=True))
        return response
    except Exception as e:
        return jsonify({"code": "500", "message": "{}".format(e)})


if __name__ == '__main__':
    app.run()
