from flask import Flask, json, request
from flask_cors import CORS, cross_origin
import os
import main
import config
import uuid
import base64
import shutil
from datetime import datetime
import subprocess

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#CORS(app, max_age=3600, resources={r"*": {"origins": ["*","https://ban-sc.idc.tarento.com"]}})

def media_conversion(file_name, dir_name):   
    subprocess.call(["ffmpeg -i {} -ar {} -ac {} -bits_per_raw_sample {} -vn {}".format(file_name, 16000, 1, 16, os.path.join(dir_name,'input_audio.wav'))], shell=True) 


@app.route('/get_transcription',methods=['POST'])
@cross_origin()
def get_transcription():
    try:
        start_time=datetime.now()
        body = request.get_json()
        language = body["source"]
        base64_string = body["audioContent"]

        uniqueID=str(uuid.uuid1())
        temp_wav=uniqueID+'.wav'

        if not os.path.exists(uniqueID):
            os.makedirs(uniqueID)
        
        decoded_string = base64.b64decode(base64_string)
        wav_file = open(temp_wav, "wb")
        wav_file.write(decoded_string)

        input = os.path.join(uniqueID,'input_audio.wav')
        media_conversion(temp_wav,uniqueID)

        file_name=input
        lang=language
        result = main.flaskresponse(file_name,lang)
        total_time=datetime.now()-start_time
        try:
            os.remove(temp_wav)
            shutil.rmtree(uniqueID)
        except OSError:
            pass

        return json.dumps({"transcript":result,"prediction_time" :str(total_time)})

    except:
        return json.dumps({'response':'failed'})


if __name__ == '__main__':
    app.run(host = config.HOST_IP, port=config.HOST_PORT, debug=True)
