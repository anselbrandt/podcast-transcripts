import os
import shutil
import logging
from diarize import (
    diarize,
    getAllFiles,
    newFiles,
    preprocess,
    realign,
    saveOutput,
    split_waveform_by_timestamps,
    updateStatus,
    saveToPkl,
)
from transcriptTools import srt_to_transcript

ROOT = os.getcwd()

logging.basicConfig(level=logging.ERROR, filename="errors.log")

if not (newFiles("files", "mono")) and not os.path.exists("roderick.db"):
    print("Put files in /files/<showname>/<000 - episode name.mp3>")
    exit()

if newFiles("files", "mono"):
    preprocess("files", "mono", "roderick.db")

results = getAllFiles("roderick.db")

print(f"processing {len(results)} files")

for file in results:
    try:
        idx, filepath, filename, showname, episode, title, duration, status = file
        word_timestamps = diarize(file)
        saveToPkl(
            os.path.join(ROOT, "output", showname, episode),
            filename.replace(".wav", ".pkl"),
            word_timestamps,
        )
        realign(file, "output", word_timestamps, 300)
        saveOutput(file, "output", "transcripts")
        srt_path = os.path.join(
            ROOT, "transcripts", showname, filename.replace(".wav", ".srt")
        )
        transcript = srt_to_transcript(srt_path)
        split_wavs_path = os.path.join(ROOT, "split_wavs", showname, episode)
        split_waveform_by_timestamps(
            filepath, split_wavs_path, transcript, showname, episode
        )
        updateStatus("roderick.db", file, "done")
        print("success")
    except Exception as error:
        updateStatus("roderick.db", file, "failed")
        print(error)
        logging.error(error, exc_info=True)
        logging.error(str(file))
        shutil.rmtree("temp_outputs")
