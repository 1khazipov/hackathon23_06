import math

import torch
import numpy as np
from deep_translator import GoogleTranslator

def text_with_punctuation(text):
    model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                      model='silero_te')
    return apply_te(text, lan='ru')

def rev_sigmoid(x:float)->float:
    return (1 / (1 + math.exp(0.5*x)))

def activate_similarities(similarities:np.array, p_size=10)->np.array:
    x = np.linspace(-10,10,p_size)
    y = np.vectorize(rev_sigmoid)
    activation_weights = np.pad(y(x),(0,similarities.shape[0]-p_size))
    diagonals = [similarities.diagonal(each) for each in range(0,similarities.shape[0])]
    diagonals = [np.pad(each, (0,similarities.shape[0]-len(each))) for each in diagonals]
    diagonals = np.stack(diagonals)
    diagonals = diagonals * activation_weights.reshape(-1,1)
    activated_similarities = np.sum(diagonals, axis=0)
    return activated_similarities

def make_paragraphs(text):
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    sentences = translated.split('. ')
    model = SentenceTransformer('all-mpnet-base-v2')
    sentece_length = [len(each) for each in sentences]
    long = np.mean(sentece_length) + np.std(sentece_length) *2
    short = np.mean(sentece_length) - np.std(sentece_length) *2
    translated_text = ''
    for each in sentences:
        if len(each) > long:
            comma_splitted = each.replace(',', '.')
        else:
            translated_text+= f'{each}. '
    sentences = translated_text.split('. ')
    translated_text = ''
    for each in sentences:
        if len(each) < short:
            translated_text+= f'{each} '
        else:
            translated_text+= f'{each}. '

    sentences = translated_text.split('. ')
    embeddings = model.encode(sentences)
    similarities = cosine_similarity(embeddings)
    activated_similarities = activate_similarities(similarities, p_size=10)
    minmimas = argrelextrema(activated_similarities, np.less, order=2)
    split_points = [each for each in minmimas[0]]

    sentences = text.split('. ')
    print(sentences[:-1])
    text = ''
    for num, each in enumerate(sentences[:-1]):
        if num in split_points:
            text += f'\n\n {each}. '
        else:
            text += f'{each}. '

    return text

def make_formal_text(text: str) -> str:
    text = text_with_punctuation(text)
    return make_paragraphs(text)
