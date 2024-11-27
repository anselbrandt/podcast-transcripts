# Podcast Transcripts

Podcast transcription, diarization and speaker labeling pipeline.

### Input files folder structure
```
files
├──<showname>
    ├──001 - <episode name>.mp3
    ├──002 - <episode name>.mp3
├──<showname>
    ├──001 - <episode name>.mp3
    ├──002 - <episode name>.mp3
```

### Run Pipeline
```
python run_pipeline.py
```

### Faster Whisper

Make sure the following is in path in `.bashrc`:

```
export PATH=/usr/local/cuda-12.6/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64\${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}:${PYENV_ROOT}/versions/3.10.15/lib/python3.10/site-packages/nvidia/cublas/lib:${PYENV_ROOT}/versions/3.10.15/lib/python3.10/site-packages/nvidia/cudnn/lib
```

### Installation

```
sudo apt install ffmpeg
```

```
pip install -c contraints.txt -r requirements.txt
```

### Chunking and Embedding Requirements

```
pip install chromadb
pip install sentence-transformers==3.1.1

```

### `Error: “Chunk size too large, text got clipped”`

https://githubissues.com/oliverguhr/deepmultilingualpunctuation/4