import torch
import speech_recognition as sr

def text_with_punctuation(text):
    model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                      model='silero_te')
    return apply_te(text, lan='ru')

def speech_to_text(audio) -> str:
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    return text_with_punctuation(text)
