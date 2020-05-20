import re
import string
import os

def get_lines(file):
    class Line:
        def __init__(self, speaker, speech):
            self.speaker = speaker
            self.speech = speech

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
                    data.append(Line(subspeaker,speech))
                speech = []
            speaker = word.lower().replace('*','')
        else:
            speech.append(word.lower())
    data.append(Line(speaker,speech))
    return data

# returns an array of Episodes, each containing an array of Lines
def get_all():
    class Episode:
        def __init__(self,season,episode,lines):
            self.season = season
            self.episode = episode
            self.lines = lines

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
            filtered.append(line)
    return filtered

# turns a list of consecutive Lines into a list of Speakers, each having a name and a list of their lines
def lump_speakers(lines):
    class Speaker:
        def __init__(self,name):
            self.name = name
            self.lines = []

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

def generate_plot_data(speakers=False, episodes=False, lump_seasons=False, total_word_count=False, total_line_count=False, word_frequency=False):
    x_axis_labels = []
    if lump_seasons:
        for episode in episodes:
            # str = 'Season ' + episode.season
            if episode.season not in x_axis_labels:
                x_axis_labels.append(episode.season)
    else:
        for episode in episodes:
            # x_axis_labels.append('S' + str(episode.season) + ' E' + str(episode.episode))
            x_axis_labels.append((episode.season,episode.episode))


    for speaker in speakers:


    return x_axis_labels

if __name__ == "__main__":
    # gets a list of Episodes
    data = get_all()

    # gets a LIST of matches, still a list even if length 1
    s01e03 = get_episodes(data,s=1,e=3)

    speakers = lump_speakers(s01e03[0].lines)

    print(generate_plot_data(episodes=data))
    # for speaker in speakers:
    #     print('\t',speaker.name,':',len(speaker.lines))







    # class Speaker:
    #     def __init__(self,name):
    #         self.name = name
    #         self.count = 1
    #
    # for episode in s01:
    #     episode_data = episode.lines
    #     speakers = []
    #     for line in episode_data:
    #         found = False
    #         for speaker in speakers:
    #             if speaker.name == line.speaker:
    #                 speaker.count += 1
    #                 found = True
    #                 continue
    #         if found:
    #             continue
    #         else:
    #             speakers.append(Speaker(line.speaker))
    #     print(episode.season,'-',episode.episode,':')
    #     for speaker in speakers:
    #         if speaker.name == 'george':
    #             print('\t',speaker.name,':',speaker.count)
