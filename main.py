from flask import Flask, request, redirect, jsonify , render_template
from deep_translator import GoogleTranslator
import json 
from pytesseract import *
import cv2 
import os

app = Flask(__name__)

languages = json.load(open("./data/languages.json","r"))

pytesseract.tesseract_cmd = "/usr/bin/tesseract"



@app.get("/")
def home():
    return "server is running"

@app.route('/translate')
def trans():
    line = request.args.get("sentence")
    # fro = request.args.get("from")
    to = request.args.get("to")
    translated = GoogleTranslator(source='auto', target='ta').translate(line)
    return translated

@app.route('/main', methods=["GET","POST"])
def translate():
    if request.method == "GET":
        return render_template("page.html" , data=languages)
    if request.method == "POST" :
        file = request.files['file']
        print(file)
        language = request.form.get("language")
        if os.path.isdir("temp/"):
            file_path = "temp/" + file.filename
        else: 
            os.mkdir("temp")
            file_path = "temp/" + file.filename
        file.save(file_path)

        # Read the image using OpenCV
        images = cv2.imread(file_path) 
        os.remove(file_path)
        rgb = cv2.cvtColor(images, cv2.COLOR_BGR2RGB) 
        results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
        all_text = []
        for i in range(0, len(results["text"])): 
            
            text = results["text"][i] 
            conf = int(results["conf"][i]) 
            
                
            text = "".join(text).strip() 
            all_text.append(text)
                
        line = " ".join(all_text)

        translated = GoogleTranslator(source='auto', target=language).translate(line)

        return translated
    

if __name__ == '__main__':
    app.run(debug=True)
