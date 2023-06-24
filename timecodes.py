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
