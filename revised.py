import re
import string
import os

class Speaker:
    def __init__(self,name):
        self.name = name
        self.lines = []

class Line:
    def __init__(self, speaker, speech):
        self.speaker = speaker
        self.speech = speech

class Episode:
    def __init__(self,season,episode,lines):
        self.season = season
        self.episode = episode
        self.lines = lines

def get_lines(file):
    speaker_pattern = re.compile("^\s{29}[A-Z\s\+]+$")

    with open(file) as f:
        script = f.read()

    # get rid of everything inside () and []
    script = re.sub(r'\([^)]*\)', ' ', script)
    script = re.sub(r'\[[^)]*\]', ' ', script)

    # replace all punctuation besides ' with whitespace.
    punc = '!"#$%&()*,-./:;<=>?@[\\]^_`{|}~' # removed '+' since it is sometimes used for multiple speakers, "Elaine + Jerry"
    script = script.translate(str.maketrans(punc, ' '*len(punc)))

    # for each line, check if its a speaker line. Turn something like "GEORGE AND JERRY" into "*GEORGE&JERRY*"
    # this step also eliminates white space
    words = []
    file_lines = script.split('\n')
    for line in file_lines:
        if speaker_pattern.match(line):
            speaker = '*'
            for word in line.split():
                if word == 'AND' or word == '+':
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
                    data.append(Line(subspeaker.title(),speech))
                speech = []
            speaker = word.lower().replace('*','').title()
        else:
            speech.append(word.lower())
    data.append(Line(speaker.title(),speech))
    return data

# returns an array of Episodes, each containing an array of Lines
def get_all():
    all = []
    for file in os.listdir('./Seinfeld Scripts'):
        data = get_lines(f"./Seinfeld Scripts/{file}")
        name = file.split('.')[0]
        episode = int(name.split('E')[1])
        season = int(name.split('E')[0].split('S')[1])
        all.append(Episode(season,episode,data))
    return all

# given a list of Episodes and optional season and episode numbers, returns the list of all Episodes that match
def get_episodes(episodes,s=False,e=False):
    selected = []
    for episode in episodes:
        if (episode.season == s) or not s:
            if (episode.episode == e) or not e:
                selected.append(episode)
    return selected

# accepts a list of Lines and a list of speakers, returns a list of all the Lines spoken by those speakers
def select_speakers_lines(lines,speakers):
    filtered = []
    for line in lines:
        if line.speaker in speakers:
            filtered.append(line.speech)
    return filtered

# turns a list of consecutive Lines into a list of Speakers, each having a name and a list of their lines
def lump_speakers(lines):
    speakers = []
    for line in lines:
        found = False
        for speaker in speakers:
            if speaker.name == line.speaker:
                speaker.lines.append(line.speech)
                found = True
                continue
        if found:
            continue
        else:
            speakers.append(Speaker(line.speaker))
            speakers[len(speakers) - 1].lines.append(line.speech)
    return speakers

def generate_plot_data(speakers=False, episodes=False, lump_seasons=False, total_word_count=False, total_line_count=False, word_frequency=False, percent=False):
    # print('**********')
    # print(percent)
    x_axis_labels = []
    if lump_seasons:
        for episode in episodes:
            if episode.season not in x_axis_labels:
                x_axis_labels.append(episode.season)
    else:
        for episode in episodes:
            x_axis_labels.append((episode.season,episode.episode))

    total = [0] * len(episodes)
    speakers_data = []
    if lump_seasons:
        pass
    else:
        for speaker in speakers:
            speaker_data = {'name':speaker,'values':[]}
            for episode in episodes:
                if total_word_count:
                    count = 0
                    lines = select_speakers_lines(episode.lines,[speaker])
                    for line in lines:
                        count += len(line)
                    if percent:
                        total_words = 0
                        for line in episode.lines:
                            total_words += len(line.speech)
                        percent_words = (count/total_words)*100
                        speaker_data['values'].append(percent_words)
                    else:
                        speaker_data['values'].append(count)
                elif total_line_count:
                    lines = select_speakers_lines(episode.lines,[speaker])
                    if percent:
                        total_lines = len(episode.lines)
                        percent_lines = (len(lines)/total_lines)*100
                        speaker_data['values'].append(percent_lines)
                    else:
                        speaker_data['values'].append(len(lines))
                elif word_frequency:
                    count = 0
                    lines = select_speakers_lines(episode.lines,[speaker])
                    for line in lines:
                        for word in line:
                            if word == word_frequency.lower():
                                count += 1
                    speaker_data['values'].append(count)

            speakers_data.append(speaker_data)
            for i in range(0,len(speaker_data['values'])):
                total[i] += speaker_data['values'][i]
        speakers_data.append({'name':'Everyone','values':total})
    return x_axis_labels, speakers_data

if __name__ == "__main__":
    data = get_all()

    s01e03 = get_episodes(data,s=1,e=3)

    speakers = lump_speakers(s01e03[0].lines)
