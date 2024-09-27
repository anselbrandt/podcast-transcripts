import os
import shutil

for entry in ["test.db", "test_errors.log"]:
    if os.path.exists(entry):
        print(f"deleing {entry}")
        os.remove(entry)

for entry in [
    "test_files",
    "test_mono",
    "test_output",
    "test_transcripts",
    "test_split_wavs",
    "temp_outputs",
]:
    if os.path.exists(entry):
        print(f"deleing {entry}")
        shutil.rmtree(entry)
