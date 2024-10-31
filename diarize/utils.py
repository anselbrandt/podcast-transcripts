import os
import torchaudio

ROOT = os.getcwd()


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


def split_waveform_speechmaps(output_dir, transcript, showname, episode):
    filenames = [
        f"{output_dir}/{showname}_{episode}_{start}_{end}_{speaker}.wav_-_{speech}"
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
