import os
import glob

import requests
from flask import Flask, request
import tarfile
import asyncio

app = Flask(__name__)

identificators = {}
id = 0


def remove_archive_data(archiveid):
    identificators.remove(archiveid)
    os.removedirs(str(archiveid))


def unpack_archive(archiveid):
    identificators[archiveid] = "unpacking"
    os.mkdir(str(archiveid))
    tarfile.open(str(archiveid) + ".tar.gz").extractall(str(id))
    identificators[id] = "ok"
# http://download.ispsystem.com/OSTemplate/new/latest/Debian-7-i386-5.57-20170910000.tar.gz

def download_archive(url, archiveid):

    response = requests.get(url)
    open(str(archiveid) + ".tar.gz", "wb").write(response.content)
    unpack_archive(archiveid)


@app.route('/archive', methods=["POST"])
def archive():
    app.logger.debug("start archiving archive")
    global id
    id += 1
    identificators[id] = "downloading"
    download_archive(request.get_json()["url"], id)
    return {
        "id": id
    }


@app.route('/archive/<archiveid>', methods=["GET", "DELETE"])
def status(archiveid):
    if request.method == "GET":
        print(identificators)
        if int(archiveid) in identificators.keys():
            app.logger.debug("found id...")
            if identificators[int(archiveid)] != "ok":
                return {
                    "status": identificators[int(archiveid)]
                }
            else:
                return {
                    "status": "ok",
                    "files": glob.glob("./" + archiveid + "/**", recursive=True)
                }
    elif request.method == "DELETE":
        os.remove()
        remove_archive_data(archiveid)
