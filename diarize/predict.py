from transformers import pipeline


def overlap_chunks(lst, n, stride=0):
    """Yield successive n-sized chunks from lst with stride length of overlap."""
    for i in range(0, len(lst), n - stride):
        yield lst[i : i + n]


def predict(words, chunk_size):
    overlap = 5
    if len(words) <= chunk_size:
        overlap = 0

    batches = list(overlap_chunks(words, chunk_size, overlap))

    # if the last batch is smaller than the overlap,
    # we can just remove it
    if len(batches[-1]) <= overlap:
        batches.pop()

    pipe = pipeline(
        "ner",
        model="kredor/punctuate-all",
        aggregation_strategy="none",
        device=0,
    )
    tagged_words = []
    for batch in batches:
        # use last batch completely
        if batch == batches[-1]:
            overlap = 0
        text = " ".join(batch)
        # hides error: You seem to be using the pipelines sequentially on GPU. In order to maximize efficiency please use a dataset
        # see https://github.com/huggingface/transformers/issues/22387
        pipe.call_count = 0
        result = pipe(text)
        assert len(text) == result[-1]["end"], "chunk size too large, text got clipped"

        char_index = 0
        result_index = 0
        for word in batch[: len(batch) - overlap]:
            char_index += len(word) + 1
            # if any subtoken of an word is labled as sentence end
            # we label the whole word as sentence end
            label = "0"
            while (
                result_index < len(result) and char_index > result[result_index]["end"]
            ):
                label = result[result_index]["entity"]
                score = result[result_index]["score"]
                result_index += 1
            tagged_words.append([word, label, score])

    assert len(tagged_words) == len(words)
    return tagged_words
