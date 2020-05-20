#formula for detecting speaker: 29 spaces + capital letter

import re
import string
caps_exclusions = ['OK']

class Line:
    def __init__(self, speaker, words):
        self.speaker = speaker
        self.words = words

def get_lines(file):
    with open(file) as f:
        script = f.read()

    # get rid of everything inside () and []
    script = re.sub(r'\([^)]*\)', ' ', script)
    script = re.sub(r'\[[^)]*\]', ' ', script)

    # replace all punctuation besides ' with whitespace
    punc = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\n'
    script = script.translate(str.maketrans(punc, ' '*len(punc)))

    # split into words
    words = script.split()

    # print(words)

    data = []
    speaker = ''
    speech = []
    for word in words:
        if word.isupper() and len(word) > 1 and word not in caps_exclusions:
            if len(speech) > 0:
                data.append(Line(speaker,speech))
                speech = []
                speaker = word.lower()
            else:
                speaker += word.lower()
        else:
            speech.append(word.lower())
    data.append(Line(speaker,speech))
    return data

if __name__ == "__main__":
    data = get_lines('./Seinfeld Scripts/S01E01.txt')
    class Speaker:
        def __init__(self,name):
            self.name = name
            self.count = 1
    speakers = []
    for line in data:
        found = False
        for speaker in speakers:
            if speaker.name == line.speaker:
                speaker.count += 1
                found = True
                continue
        if found:
            continue
        else:
            speakers.append(Speaker(line.speaker))

    for speaker in speakers:
        print(speaker.name,':',speaker.count)
