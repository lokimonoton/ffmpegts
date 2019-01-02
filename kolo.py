"""
Streaming FFmpeg to HTTP, via Python's Flask.
This is an incredibly simple example, which will yield issues due to inconsistant input and output rates.
If you're going to use this, VLC works okay as a client.
You really need to move FFmpeg into a separate thread, which should help stream audio more consistantly to the HTTP client.

Example by Anthony Eden (https://mediarealm.com.au)
"""

from flask import Flask
from flask import stream_with_context, request, Response
import subprocess
import time
import socket
import itertools
import math
import re
import time
from decimal import Decimal
from subprocess import Popen
import json
import os
def pecah(input,output):
    ffmpegcommand=r"ffmpeg -i {input} -map 0 -f ssegment -segment_list {output}.m3u8 -segment_list_flags +live -segment_time 10 static/{output}-out%03d.ts".format(input=input,output=output.replace("/",""))
    return ffmpegcommand
with open('streaming.json') as f:
    data = json.load(f)

# pprint(data['streams'])



SEGMENTS_IN_PLAYLIST = 10
app = Flask(__name__)
def read_file_durations(video):
    with open(video) as f:
        content = f.read()
    file_durations = re.findall(r"EXTINF:([\d\.]+),\s*\n([\w\.]+)", content, flags=re.M)
    return [(float(duration), filename) for duration, filename in file_durations]

# files_and_durations = read_file_durations()
# print files_and_durations
@app.route("/")
def panda():
    return "haha"
@app.route("/<string:id>")
def playlist(id):
    # yops=id.split("-")
    import re
    p=re.compile("\.(ts)")
    if p.search(id)!=None:
        f = open("static/{id}".format(id=id), "r")

        return Response(f.read(), mimetype="application/vnd.apple.mpegurl")
    else:
        f = open("{video}.m3u8".format(video=id), "r")
# print()
        return Response(f.read(), mimetype="application/vnd.apple.mpegurl")

        



if __name__ == "__main__":
    try:
        processes = [Popen(pecah(a['input'],a['output']), shell=True) for a in data['streams']]
        processes.append(Popen(app.run()))
# do other things here..
# wait for completion
        for p in processes: p.wait()
        # app.run()
    except Exception, e:
        print "yuyu"