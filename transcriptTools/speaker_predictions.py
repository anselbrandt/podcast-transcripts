def most_frequent(lst):
    return max(set(lst), key=lst.count)


def prediction_algo(names, occurences):
    if len(occurences):
        return [
            uppername
            for uppername, lowername in names
            if most_frequent(occurences) not in uppername
        ][0]
    else:
        return None


def speakerPredictions(transcript_with_timestamps, speaker_names):
    names = [(name, name.lower()) for name in speaker_names]

    matches = {"Speaker 0": [], "Speaker 1": []}

    for idx, start, end, speaker, line in transcript_with_timestamps:
        for uppername, lowername in names:
            if lowername + "." in line.lower():
                matches[speaker].append(uppername)
            if lowername + " " in line.lower():
                matches[speaker].append(uppername)

    initial_predictions = {}

    for key in matches:
        initial_predictions[key] = prediction_algo(names, matches[key])

    predictions = {}

    if initial_predictions["Speaker 0"]:
        predictions["Speaker 0"] = initial_predictions["Speaker 0"]
        predictions["Speaker 1"] = [
            uppername
            for uppername, lowername in names
            if initial_predictions["Speaker 0"] not in uppername
        ][0]

    if initial_predictions["Speaker 1"]:
        predictions["Speaker 1"] = initial_predictions["Speaker 1"]
        predictions["Speaker 0"] = [
            uppername
            for uppername, lowername in names
            if initial_predictions["Speaker 1"] not in uppername
        ][0]

    return predictions
