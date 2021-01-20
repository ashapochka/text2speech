"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import json
import sys
from datetime import datetime
from pathlib import Path

from google.cloud import texttospeech


class Text2Speech:
    # noinspection PyTypeChecker
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-D",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def text2speech(self, text=None, ssml=None, mp3file=None):
        if text:
            synthesis_input = texttospeech.SynthesisInput(text=text)
        elif ssml:
            synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
        else:
            return False
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=self.voice,
            audio_config=self.audio_config
        )
        if mp3file:
            with open(mp3file, "wb") as out:
                out.write(response.audio_content)
        return True


if __name__ == '__main__':
    try:
        what_to_convert = sys.argv[1]
    except IndexError:
        print('nothing is selected for conversion')
        exit(1)
    else:
        with open('config.json') as config_file:
            config = json.load(config_file)
        inputs = config['inputs']
        parent_dir = Path(config['workdir'])
        in_dir = parent_dir / 'inputs'
        out_dir = parent_dir / 'outputs'
        out_timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        t2s = Text2Speech()
        for i in inputs[what_to_convert]:
            input_file = in_dir / f'{i}.ssml'
            ssml_text = input_file.read_text()
            mp3_file = out_dir / f'{i}-{out_timestamp}.mp3'
            t2s.text2speech(ssml=ssml_text, mp3file=mp3_file)
            print(f'Audio content written to file {mp3_file}')
