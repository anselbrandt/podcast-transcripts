import os
import librosa
import sqlite3

def createDb(dbFile, inputDir):
    print(f"creating {dbFile}")
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

    conn = sqlite3.connect(dbFile)

    c = conn.cursor()

    c.execute(
        """CREATE TABLE files (
            id integer primary key,
            path text,
            filename text,
            showname text,
            episode text,
            title text,
            duration real,
            status text
            )"""
    )

    conn.commit()

    for path, filename, showname, episode, title, duration in files:
        c.execute(
            "INSERT INTO files VALUES (null, ?, ?, ?, ?, ?, ?, ?)",
            (path, filename, showname, episode, title, duration, "waiting"),
        )

    conn.commit()
    conn.close()