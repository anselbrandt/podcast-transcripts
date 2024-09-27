def datesDict(file):
    dates = {
        date: episode
        for date, episode in [
            (line.split(" - ")[0], line.split(" - ")[1])
            for line in open(file).read().splitlines()
        ]
    }
    return dates


def titlesDict(file):
    titles = {
        title: episode
        for title, episode in [
            (line.split(" - ")[0], line.split(" - ")[1])
            for line in open(file).read().splitlines()
        ]
    }
    return titles
