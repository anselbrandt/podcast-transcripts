import nemo.collections.asr as nemo_asr
import logging
import random

logging.getLogger("nemo_logger").setLevel(logging.ERROR)

speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained(
    "nvidia/speakerverification_en_titanet_large"
)


def reference_likleyhood(reference, samples):
    results = 0
    for sample in samples:
        try:
            result = speaker_model.verify_speakers(reference, sample)
            results = results + result
        except:
            print(sample)
    return results / 10


def getReferenceLabel(reference_filepath, sample_filepaths):
    speaker0 = [file for file in sample_filepaths if "Speaker 0" in file]
    speaker1 = [file for file in sample_filepaths if "Speaker 1" in file]
    randomized0 = random.sample(speaker0, len(speaker0))[:10]
    randomized1 = random.sample(speaker1, len(speaker1))[:10]
    result0 = reference_likleyhood(reference_filepath, randomized0)
    result1 = reference_likleyhood(reference_filepath, randomized1)
    if result0 > result1:
        return "Speaker 0"
    else:
        return "Speaker 1"


def getSpeakerLabels(referenceLabel, speakers):
    mainSpeaker, secondarySpeaker = speakers
    if referenceLabel == "Speaker 0":
        return {"Speaker 0": mainSpeaker, "Speaker 1": secondarySpeaker}
    else:
        return {"Speaker 0": secondarySpeaker, "Speaker 1": mainSpeaker}
