import os
import shutil
import torch
from diarize.library import (
    transcribe_batched,
    transcribe,
    wav2vec2_langs,
    filter_missing_timestamps,
    create_config,
)
import whisperx
from nemo.collections.asr.models.msdd_models import NeuralDiarizer

# https://github.com/oliverguhr/deepmultilingualpunctuation/blob/main/deepmultilingualpunctuation/punctuationmodel.py


def diarize(file):
    (id, audio_path, filename, showname, episode, title, duration, status) = file
    print(f"processing {filename}...")
    vocal_target = audio_path

    whisper_model_name = "large-v3"
    suppress_numerals = True
    batch_size = 8
    language = "en"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Transcribe using Whisper and reallign timestamps using Wav2Vec2

    if device == "cuda":
        compute_type = "float16"
    else:
        compute_type = "int8"

    if batch_size != 0:
        whisper_results, language = transcribe_batched(
            vocal_target,
            language,
            batch_size,
            whisper_model_name,
            compute_type,
            suppress_numerals,
            device,
        )
    else:
        whisper_results, language = transcribe(
            vocal_target,
            language,
            whisper_model_name,
            compute_type,
            suppress_numerals,
            device,
        )

        # Align transcription with original audio using Wav2Vec2

    if language in wav2vec2_langs:
        device = "cuda"
        alignment_model, metadata = whisperx.load_align_model(
            language_code=language, device=device
        )
        result_aligned = whisperx.align(
            whisper_results, alignment_model, metadata, vocal_target, device
        )
        word_timestamps = filter_missing_timestamps(result_aligned["word_segments"])

        # clear gpu vram
        del alignment_model
        torch.cuda.empty_cache()
    else:
        assert (
            batch_size == 0
        ), (  # TODO: add a better check for word timestamps existence
            f"Unsupported language: {language}, use --batch_size to 0"
            " to generate word timestamps using whisper directly and fix this error."
        )
        word_timestamps = []
        for segment in whisper_results:
            for word in segment["words"]:
                word_timestamps.append(
                    {"word": word[2], "start": word[0], "end": word[1]}
                )

    # Copy file to temp directory for NeMo

    ROOT = os.getcwd()
    temp_path = os.path.join(ROOT, "temp_outputs")
    os.makedirs(temp_path, exist_ok=True)
    shutil.copyfile(audio_path, os.path.join(temp_path, "mono_file.wav"))

    # Diarize with NeMo MSSD

    msdd_model = NeuralDiarizer(
        cfg=create_config(temp_path, DOMAIN_TYPE="telephonic")
    ).to("cuda")
    msdd_model.diarize()

    del msdd_model
    torch.cuda.empty_cache()

    return word_timestamps
