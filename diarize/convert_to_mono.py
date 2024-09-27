import os
import shutil
import torch
import torchaudio

ROOT = os.getcwd()


def convertToMono(inputDir, outputDir):

    print("converting to mono")
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
            os.path.join(dir, file)
            .replace(f"/{inputDir}/", f"/{outputDir}/")
            .replace(".mp3", ".wav")
            .replace(" ", "_")
            .replace("..", ".")
            .replace("._", "_")
            .replace("!", ""),
        )
        for dir, showname in dirs
        for file in os.listdir(dir)
        if os.path.isfile(os.path.join(dir, file))
        if ".DS_Store" not in file
    ]

    output_dir = os.path.join(root, outputDir)
    os.makedirs(output_dir, exist_ok=True)

    for dir in dirs:
        show_dir, showname = dir
        output_show_dir = os.path.join(output_dir, showname)
        os.makedirs(output_show_dir, exist_ok=True)

    for file in files:
        input, output = file

        return_code = os.system(
            f'python3 -m demucs.separate -n htdemucs --two-stems=vocals "{input}" -o "demucs_output"'
        )

        if return_code != 0:
            audio_path = input
        else:
            audio_path = [
                os.path.join(ROOT, "demucs_output", "htdemucs", dir, "vocals.wav")
                for dir in os.listdir(os.path.join(ROOT, "demucs_output", "htdemucs"))
            ][0]
        waveform, sample_rate = torchaudio.load(audio_path)
        mono_waveform = torch.mean(waveform, dim=0, keepdim=True)
        torchaudio.save(output, mono_waveform, sample_rate)

        os.remove(input)
        if os.path.exists("demucs_output"):
            shutil.rmtree("demucs_output")
