from flask import Flask, render_template, request
from googletrans import Translator, LANGUAGES
from gtts import gTTS

app = Flask(__name__)

# Initialize the translator
translator = Translator()

# Get a list of supported languages and their codes
supported_languages = LANGUAGES

@app.route('/', methods=['GET', 'POST'])
def index():
    source_language = request.form.get('source_language', 'en')  # Default source language is English
    target_language = request.form.get('target_language', 'en')  # Default target language is English

    if request.method == 'POST':
        text_to_translate = request.form['text_to_translate']

        try:
            translated_text = translator.translate(text_to_translate, src=source_language, dest=target_language).text

            # Generate speech from translated text and save it as an audio file
            tts = gTTS(text=translated_text, lang=target_language)
            audio_file = "translated_audio.mp3"
            tts.save(audio_file)

            # Serve the audio file
            audio_url = "/" + audio_file
        except Exception as e:
            translated_text = f"Translation Error: {str(e)}"
            audio_url = None

        return render_template('index.html', translation=translated_text, languages=supported_languages, source_language=source_language, target_language=target_language, audio_url=audio_url)

    return render_template('index.html', translation=None, languages=supported_languages, source_language=source_language, target_language=target_language)

if __name__ == '__main__':
    app.run(debug=True)
