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

The diarization pipeline only has a few requirements, unfortunately they demand specific versions, which are likely overridden by `nemo` having unpinned dependencies.

```
pip install setuptools wheel cython

pip install -r requirements.txt --no-deps
```

The `--no-deps` is very important!`

Or follow the manual installation below:

### Manual Installation

```
pip install --upgrade pip
pip install wheel
pip install setuptools
pip install cython
pip install unidecode
pip install torch==2.3
pip install torchaudio==2.3
pip install torchvision==0.18
pip install faster-whisper
pip install pyannote.audio
pip install demucs
pip install tiktoken

pip install "nemo_toolkit[asr]"

pip uninstall huggingface_hub
pip uninstall transformers
pip uninstall datasets
pip uninstall ctranslate2

pip install huggingface_hub==0.22.0
pip install ctranslate2==4.4.0
pip install transformers==4.39.2
pip install datasets==3.0.1

pip install chromadb
pip install sentence-transformers==3.1.1

pip install ipykernel ipywidgets ipython
```

### `Error: “Chunk size too large, text got clipped”`

https://githubissues.com/oliverguhr/deepmultilingualpunctuation/4