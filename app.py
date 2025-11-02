from flask import Flask, render_template, request
from googletrans import Translator
from gtts import gTTS
import os
import time

app = Flask(__name__)

# ✅ Available languages (short code → full name)
languages = {
    'en': 'English',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-cn': 'Chinese',
    'ar': 'Arabic'
}

@app.route("/", methods=["GET", "POST"])
def index():
    translated_text = ""
    audio_file = None

    if request.method == "POST":
        text = request.form["text"]
        src_lang = request.form["src_lang"]
        dest_lang = request.form["dest_lang"]

        # Translate text
        translator = Translator()
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        translated_text = result.text

        # Generate speech from translated text
        if translated_text.strip():
            if not os.path.exists("static"):
                os.makedirs("static")

            filename = f"static/output_{int(time.time())}.mp3"
            tts = gTTS(translated_text, lang=dest_lang)
            tts.save(filename)
            audio_file = filename

    return render_template("index.html",
                           languages=languages,
                           translated_text=translated_text,
                           audio_file=audio_file)

if __name__ == "__main__":
    app.run(debug=True)
