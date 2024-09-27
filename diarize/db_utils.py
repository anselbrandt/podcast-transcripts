import sqlite3


def getAllFiles(dbFile):
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()

    c.execute("""SELECT * FROM files WHERE status='waiting'""")

    results = c.fetchall()

    conn.commit()
    conn.close()

    return results


def updateStatus(dbFile, file, status):
    (id, audio_path, filename, showname, episode, title, duration, prevStatus) = file
    print(f"{filename} {status}.")
    conn = sqlite3.connect(dbFile)
    c = conn.cursor()

    c.execute(
        """UPDATE files SET status=? WHERE id=?""",
        (
            status,
            id,
        ),
    )

    conn.commit()
    conn.close()
