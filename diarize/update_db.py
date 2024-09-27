import os
import librosa
import sqlite3


def exists(dbFile, file):
    path, filename, showname, episode, title, duration = file
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()

    c.execute("""SELECT * FROM files WHERE episode=? AND title=?""", (episode, title))

    result = c.fetchone()

    conn.commit()
    conn.close()

    if result:
        return True
    else:
        return False


def insert(dbFile, file):
    path, filename, showname, episode, title, duration = file
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()
    c.execute(
        "INSERT INTO files VALUES (null, ?, ?, ?, ?, ?, ?, ?)",
        (path, filename, showname, episode, title, duration, "waiting"),
    )

    conn.commit()
    conn.close()


def updateDb(dbFile, inputDir):
    print(f"updating {dbFile}")
    root = os.getcwd()
    input_dir = os.path.join(root, inputDir)
    dirs = [
        (os.path.join(input_dir, dir), dir)
        for dir in os.listdir(input_dir)
        if os.path.isdir(os.path.join(input_dir, dir))
    ]
    files = [
        (
            os.path.join(dir, file),
            file,
            showname,
            file.split("_-_")[0],
            file.split("_-_")[1].replace(".wav", "").replace("_", " "),
            librosa.get_duration(path=os.path.join(dir, file)),
        )
        for dir, showname in dirs
        for file in os.listdir(dir)
        if os.path.isfile(os.path.join(dir, file))
        if ".DS_Store" not in file
    ]

    for file in files:
        if exists(dbFile, file):
            continue
        else:
            insert(dbFile, file)
