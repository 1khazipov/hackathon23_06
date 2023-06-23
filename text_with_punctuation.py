import torch

def text_with_punctuation(text):
    model, example_texts, languages, punct, apply_te = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                      model='silero_te')
    return apply_te(text, lan='ru')
