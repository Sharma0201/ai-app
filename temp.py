import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

device = torch.device('cuda:0')
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small").to(device)


def summarize(passage):
    print('\n' + passage)
    # preprocess_text = passage.strip().replace("\n", "")
    preprocess_text = passage
    t5_prepared_Text = "summarize: " + preprocess_text
    word_count = len(t5_prepared_Text.split())
    input_ids = tokenizer(t5_prepared_Text, return_tensors='pt').to(device).input_ids
    outputs = model.generate(input_ids, num_beams=6,
                             no_repeat_ngram_size=2,
                             min_length=5,
                             max_length=word_count,
                             early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

