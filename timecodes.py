import whisper_timestamped as whisper


def get_timestamped(file_path, language='ru'):
    audio = whisper.load_audio(file_path)

    model = whisper.load_model("base", device="cpu")

    result = whisper.transcribe(model, audio, language=language)

    word_list = []
    for segment in result.get('segments'):
        for word in segment.get('words'):
            word_list.append(word)
    return word_list


def get_sentences(word_list):
    sentences = []
    my_dict = {
        'text': '',
        'start': '',
        'end': ''
    }
    str1 = ''
    start = 0
    end = 0
    new_sentence = True
    for word in word_list:
        if word.get('text')[-1] == '.':
            str1 += word.get('text')
            end = word.get('end')
            my_dict['text'] = str1
            my_dict['start'] = start
            my_dict['end'] = end
            str1 = ''
            start = 0
            end = 0
            new_sentence = True
            sentences.append(my_dict.copy())
        else:
            str1 += word.get('text') + ' '
            if new_sentence:
                start = word.get('start')
                new_sentence = False
            
    return sentences