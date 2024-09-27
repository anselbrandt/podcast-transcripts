from diarize.utils import timeToSeconds


def filter_extra_speakers(transcript):
    lines = [
        (idx, start, end, speaker, line)
        for idx, start, end, speaker, line in transcript
        if "Speaker 2" not in speaker
    ]
    return lines


def srt_to_transcript(filepath):
    srt = open(filepath, encoding="utf-8-sig").read().replace("\n\n", "\n").splitlines()
    grouped = [srt[i : i + 3] for i in range(0, len(srt), 3)]
    transcript = [
        (
            idx,
            timeToSeconds(times.split(" --> ")[0]),
            timeToSeconds(times.split(" --> ")[1]),
            speech.split(": ")[0],
            speech.split(": ")[1],
        )
        for idx, times, speech in grouped
        if timeToSeconds(times.split(" --> ")[1])
        > timeToSeconds(times.split(" --> ")[0])
    ]
    no_extra_speakers = filter_extra_speakers(transcript)
    return no_extra_speakers
