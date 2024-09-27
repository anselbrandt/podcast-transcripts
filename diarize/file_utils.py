import os
import pickle
import shutil
from diarize.create_db import createDb
from diarize.update_db import updateDb
from diarize.convert_to_mono import convertToMono


ROOT = os.getcwd()


def newFiles(inputDir, outputDir):
    root = os.getcwd()
    input_dir = os.path.join(root, inputDir)
    dirs = [
        (os.path.join(input_dir, dir), dir)
        for dir in os.listdir(input_dir)
        if os.path.isdir(os.path.join(input_dir, dir))
    ]

    if len(dirs):
        pass
    else:
        return False

    files = [
        (
            os.path.join(dir, file),
            os.path.join(dir, file)
            .replace(f"/{inputDir}/", f"/{outputDir}/")
            .replace(".mp3", ".wav"),
        )
        for dir, showname in dirs
        for file in os.listdir(dir)
        if os.path.isfile(os.path.join(dir, file))
        if ".DS_Store" not in file
    ]
    if len(files):
        return True
    else:
        return False


def preprocess(inputDir, outputDir, dbFile):
    convertToMono(inputDir, outputDir)

    if os.path.exists(dbFile):
        updateDb(dbFile, outputDir)
    else:
        createDb(dbFile, outputDir)


def saveOutput(file, srcDir, outputDir):
    (id, audio_path, filename, showname, episode, title, duration, status) = file
    transcript_dir = os.path.join(ROOT, outputDir, showname)
    os.makedirs(transcript_dir, exist_ok=True)
    path_srtfile_with_speakers = os.path.join(
        srcDir, showname, episode, f"{os.path.splitext(filename)[0]}.srt"
    )
    shutil.copyfile(
        path_srtfile_with_speakers,
        os.path.join(transcript_dir, f"{os.path.splitext(filename)[0]}.srt"),
    )


def saveToPkl(dir, filename, data):
    os.makedirs(dir, exist_ok=True)
    with open(
        os.path.join(dir, filename),
        "wb",
    ) as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def loadPkl(filepath):
    with open(filepath, "rb") as handle:
        data = pickle.load(handle)
    return data
