from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = 'doc2query/msmarco-russian-mt5-base-v1'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def create_title(
        para,
        num_return_sequences=2,
        num_beams=2
):
    input_ids = tokenizer.encode(para, return_tensors='pt')
    with torch.no_grad():
        beam_outputs = model.generate(
            input_ids=input_ids,
            max_length=256,
            num_beams=num_beams,
            no_repeat_ngram_size=4,
            num_return_sequences=num_return_sequences,
            early_stopping=True
        )

    output = []
    for i in range(len(beam_outputs)):
        output.append(tokenizer.decode(
            beam_outputs[i], skip_special_tokens=True))

    return output
