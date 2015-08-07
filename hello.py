import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<html><body><a target="_blank" href="https://www.google.com/calendar/event?action=TEMPLATE&tmeid=OXA1bDFmMzl1azlvczB0bXNkdjg4OTU1c28ga3JpdmljaC5la2F0ZXJpbmFAbQ&tmsrc=krivich.ekaterina%40gmail.com"><img border="0" src="https://www.google.com/calendar/images/ext/gc_button1_en.gif"></a></body></html>'
