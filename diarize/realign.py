import os
import shutil
import re
from diarize.library import (
    get_words_speaker_mapping,
    get_realigned_ws_mapping_with_punctuation,
    get_sentences_speaker_mapping,
    get_speaker_aware_transcript,
    write_srt,
)
from diarize.predict import predict

# Map Speakers to senteces with timestamps


def realign(file, outputDir, word_timestamps, initial_chunk_size):
    (id, audio_path, filename, showname, episode, title, duration, status) = file
    speaker_ts = []
    ROOT = os.getcwd()
    temp_path = os.path.join(ROOT, "temp_outputs")
    with open(os.path.join(temp_path, "pred_rttms", "mono_file.rttm"), "r") as f:
        lines = f.readlines()
        for line in lines:
            line_list = line.split(" ")
            s = int(float(line_list[5]) * 1000)
            e = s + int(float(line_list[8]) * 1000)
            speaker_ts.append([s, e, int(line_list[11].split("_")[-1])])

    wsm = get_words_speaker_mapping(word_timestamps, speaker_ts, "start")

    words_list = list(map(lambda x: x["word"], wsm))

    labled_words = None
    chunk_size = initial_chunk_size
    while labled_words is None:
        try:
            labled_words = predict(words_list, chunk_size)
        except:
            chunk_size = chunk_size - 10
            print(f"retrying with chunk size: {chunk_size}")
            pass

    ending_puncts = ".?!"
    model_puncts = ".,;:!?"

    is_acronym = lambda x: re.fullmatch(r"\b(?:[a-zA-Z]\.){2,}", x)

    for word_dict, labeled_tuple in zip(wsm, labled_words):
        word = word_dict["word"]
        if (
            word
            and labeled_tuple[1] in ending_puncts
            and (word[-1] not in model_puncts or is_acronym(word))
        ):
            word += labeled_tuple[1]
            if word.endswith(".."):
                word = word.rstrip(".")
            word_dict["word"] = word

    wsm = get_realigned_ws_mapping_with_punctuation(wsm)
    ssm = get_sentences_speaker_mapping(wsm, speaker_ts)

    # Cleanup

    output_path = os.path.join(outputDir, showname, episode)

    os.makedirs(output_path, exist_ok=True)

    shutil.rmtree("temp_outputs", output_path)

    path_textfile_with_speakers = os.path.join(
        output_path, f"{os.path.splitext(filename)[0]}.txt"
    )
    path_srtfile_with_speakers = os.path.join(
        output_path, f"{os.path.splitext(filename)[0]}.srt"
    )

    with open(path_textfile_with_speakers, "w", encoding="utf-8-sig") as f:
        get_speaker_aware_transcript(ssm, f)

    with open(path_srtfile_with_speakers, "w", encoding="utf-8-sig") as srt:
        write_srt(ssm, srt)

    # Format results

    with open(path_textfile_with_speakers, "r") as f:
        lines = f.readlines()
        lines = [
            re.sub(" +", " ", line.strip("\ufeff").strip())
            for line in lines
            if line != "\n"
        ]

    with open(path_textfile_with_speakers, "w", encoding="utf-8-sig") as f:
        for i, line in enumerate(lines):
            if i < len(lines) - 1:
                f.write(f"{line}\n\n")
            else:
                f.write(f"{line}")
