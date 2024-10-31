import os
import csv
from datetime import timedelta
import tiktoken

ROOT = os.getcwd()


def getTranscriptFiles(transcriptDir):
    dirs = [
        (os.path.join(transcriptDir, dir), dir)
        for dir in sorted(os.listdir(transcriptDir))
        if ".DS_Store" not in dir
    ]

    files = [
        (os.path.join(dir, file), showname, file)
        for dir, showname in dirs
        for file in sorted(os.listdir(dir))
        if ".DS_Store" not in file
    ]
    return files


def aggregateSpeakers(transcript):
    aggregated = []
    idx, start, end, initial_speaker, line = transcript[0]
    prevspeaker = initial_speaker
    prevLine = ""
    for idx, start, end, speaker, line in transcript:
        if speaker == prevspeaker:
            prevLine = f"{prevLine}{'' if prevLine=='' else ' '}{line}"
        else:
            aggregated.append((prevspeaker, prevLine))
            prevspeaker = speaker
            prevLine = line
    aggregated.append((prevspeaker, prevLine))
    return aggregated


def filterSpeaker(transcript, speaker_to_keep):
    lines = [
        (idx, start, end, speaker, line)
        for idx, start, end, speaker, line in transcript
        if speaker_to_keep in speaker
    ]
    return lines


def loadSpeakerLabels(csvPath):
    speaker_labels = {"rotl": {}, "roadwork": {}}

    for showname, episode, speaker0, speaker1 in list(csv.reader(open(csvPath))):
        speaker_labels[showname].update(
            {episode: {"Speaker 0": speaker0, "Speaker 1": speaker1}}
        )
    return speaker_labels


def reverseLookupJohn(csvPath):
    johnLabels = {"rotl": {}, "roadwork": {}}

    for showname, episode, speaker0, speaker1 in list(csv.reader(open(csvPath))):
        john = "Speaker 0" if "John" in speaker0 else "Speaker 1"
        johnLabels[showname].update({episode: john})
    return johnLabels


def labelTranscript(transcript, labels):
    lines = [
        (idx, start, end, labels[speaker], line)
        for idx, start, end, speaker, line in transcript
    ]
    return lines


def secondsToTime(seconds):
    result = timedelta(seconds=seconds)
    string = (
        str(timedelta(seconds=result.seconds))
        + ","
        + str(int(result.microseconds / 1000))
    )
    return string


def transcript_to_srt(transcript):
    lines = [
        f"{idx}\n{secondsToTime(start)} --> {secondsToTime(end)}\n{speaker}: {speech}"
        for idx, start, end, speaker, speech in transcript
    ]
    return "\n\n".join(lines)


def reindex(transcript):
    reindexed = [
        (str(index + 1), start, end, speaker, speech)
        for index, (idx, start, end, speaker, speech) in enumerate(transcript)
    ]
    return reindexed


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


encoding_name = "cl100k_base"


def token_count(string: str, encoding_name=encoding_name) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
