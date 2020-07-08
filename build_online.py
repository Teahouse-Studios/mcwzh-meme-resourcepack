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
    mods = ["mods/" + file for file in os.listdir('mods')]
    enmods = ["en-mods/" + file for file in os.listdir('en-mods')]
    language_modules = [
        "modules/" + module for module in build.module_checker().get_module_list('language')]
    resource_modules = [
        "modules/" + module for module in build.module_checker().get_module_list('resource')]
    header_existence = os.path.exists("./views/custom/header.html")
    footer_existence = os.path.exists("./views/custom/footer.html")
    return render_template("index.html", mods=mods, enmods=enmods, language=language_modules, resource=resource_modules,
                           header_existence=header_existence, footer_existence=footer_existence)


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
        builder = build.builder()
        builder.set_args(recv_data)
        builder.build()
        logs += builder.get_logs()
        message = {"code": 200, "argument": recv_data,
                   "logs": logs, "filename": builder.get_filename()}
        print(recv_data)
    finally:
        lock.release()
    return json.dumps(message)


@app.route('/builds/<file_name>', methods=['GET'])
def get_file(file_name):
    directory = "./builds"
    try:
        response = make_response(send_from_directory(
            directory, file_name, as_attachment=True))
        return response
    except Exception as e:
        return jsonify({"code": "500", "message": "{}".format(e)})


if __name__ == '__main__':
    app.run()
