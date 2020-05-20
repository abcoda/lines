import re
import string

speaker_pattern = re.compile("^\s{29}[A-Z\s]+$")

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

    # replace all punctuation besides ' with whitespace.
    punc = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
    script = script.translate(str.maketrans(punc, ' '*len(punc)))

    # for each line, check if its a speaker line. Turn something like "GEORGE AND JERRY" into "*GEORGE&JERRY*"
    # this step also eliminates white space
    words = []
    file_lines = script.split('\n')
    for line in file_lines:
        if speaker_pattern.match(line):
            speaker = '*'
            for word in line.split():
                if word == 'AND':
                    speaker += '&'
                else:
                    speaker += word
            speaker += '*'
            words.append(speaker)
        else:
            words += line.split()

    # Turn list of words into an array of Line objects, each with a speaker and an array of spoken words
    # If a line has multiple speakers, a seperate line is added for each speaker
    data = []
    speaker = ''
    speech = []
    for word in words:
        if '*' in word:
            if len(speech) > 0:
                for subspeaker in speaker.split('&'):
                    data.append(Line(subspeaker,speech))
                speech = []
            speaker = word.lower().replace('*','')
        else:
            speech.append(word.lower())
    data.append(Line(speaker,speech))
    return data

if __name__ == "__main__":
    data = get_lines('./Seinfeld Scripts/S01E01.txt')
    # for line in data:
    #     print(line.speaker,':',line.words)
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
