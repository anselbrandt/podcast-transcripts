import os
import shutil
import logging
import pickle
from diarize import (
    convertToMono,
    createDb,
    diarize,
    getAllFiles,
    realign,
    saveOutput,
    split_waveform_by_timestamps,
    srt_to_transcript,
    updateStatus,
    saveToPkl,
)

ROOT = os.getcwd()

logging.basicConfig(level=logging.ERROR, filename="test_errors.log")

os.makedirs("test_files/rotl", exist_ok=True)
shutil.copyfile("549 - Sample.mp3", "test_files/rotl/549 - Sample.mp3")

convertToMono("test_files", "test_mono")

createDb("test.db", "test_mono")

results = getAllFiles("test.db")


for file in results:
    try:
        idx, filepath, filename, showname, episode, title, duration, status = file
        word_timestamps = diarize(file)
        saveToPkl(
            os.path.join(ROOT, "test_output", showname, episode),
            filename.replace(".wav", ".pkl"),
            word_timestamps,
        )
        realign(file, "test_output", word_timestamps, 300)
        saveOutput(file, "test_output", "test_transcripts")
        srt_path = os.path.join(
            ROOT, "test_transcripts", showname, filename.replace(".wav", ".srt")
        )
        transcript = srt_to_transcript(srt_path)
        split_wavs_path = os.path.join(ROOT, "test_split_wavs", showname, episode)
        split_waveform_by_timestamps(
            filepath, split_wavs_path, transcript, showname, episode
        )
        updateStatus("test.db", file, "done")
    except Exception as error:
        print(error)
        logging.error(error, exc_info=True)
        logging.error(str(file))
        updateStatus("test.db", file, "failed")
