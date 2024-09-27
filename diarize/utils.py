import os
from datetime import timedelta
import torchaudio
import tiktoken

ROOT = os.getcwd()


def timeToSeconds(time):
    hhmmss = time.split(",")[0]
    ms = time.split(",")[1]
    hh = hhmmss.split(":")[0]
    mm = hhmmss.split(":")[1]
    ss = hhmmss.split(":")[2]
    seconds = timedelta(
        hours=int(hh), minutes=int(mm), seconds=int(ss), milliseconds=int(ms)
    )
    return seconds.total_seconds()


encoding_name = "cl100k_base"


def token_count(string: str, encoding_name=encoding_name) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def split_waveform_by_timestamps(input_file, output_dir, transcript, showname, episode):
    mono_waveform, sample_rate = torchaudio.load(input_file)
    os.makedirs(output_dir, exist_ok=True)

    for idx, start, end, speaker, speech in transcript:
        start_frame = int(start * sample_rate)
        end_frame = int(end * sample_rate)
        segment = mono_waveform[0:, start_frame:end_frame]
        output_file = os.path.join(
            output_dir, f"{showname}_{episode}_{start}_{end}_{speaker}.wav"
        )

        torchaudio.save(output_file, segment, sample_rate)


def split_waveform_filenames(output_dir, transcript, showname, episode):
    filenames = [
        f"{output_dir}/{showname}_{episode}_{start}_{end}_{speaker}.wav"
        for idx, start, end, speaker, speech in transcript
    ]
    return filenames


def split_waveform_filenames_JSON(output_dir, transcript, showname, episode):
    fileStr = '"file"'
    textStr = '"text"'
    lines = [
        "{"
        + f"{fileStr}: `{output_dir}/{showname}_{episode}_{start}_{end}_{speaker}.wav`, {textStr}: `{speech}`,"
        + "},"
        for idx, start, end, speaker, speech in transcript
    ]
    return "[" + "\n".join(lines) + "]"
