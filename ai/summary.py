from transformers import pipeline

summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")


def summarize(passage):
    word_count = len(passage.split())
    print('\n' + passage)
    summary = (summarizer(passage, min_length=5, max_length=word_count, do_sample=False))
    return summary[0]["summary_text"]
