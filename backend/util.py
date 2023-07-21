#from flair.data import Sentence
import re, os

def get_cha_files_in_dir(directory):
    result = []
    for obj_name in os.listdir(directory):
        obj_absolute_path = directory + "/" + obj_name
        is_dir = len(obj_name.split('.')) == 1 # no . in the name means it is a folder not a file
        if is_dir:
            cha_files = get_cha_files_in_dir(obj_absolute_path)
            for cha_file in cha_files:
                result.append(cha_file)
        elif obj_name.split('.')[-1] == "cha": # if file extension is cha
            result.append(obj_absolute_path)
    return result

def preprocess_sentence_from_cha(line):
    if line[0] == "@": # comments start with @ in .cha
        return
    else:
        try:
            original_text = line.split("*PAR:\t")[1] # our project spec denotes each utterance begins with *PAR:
            preprocessed_text = original_text
            #preprocess out excluded material denoted as <> [e]
            preprocessed_text = re.sub(r'<.*?>\s*\[e\]', '', preprocessed_text)
            # preprocess out pause markers
            if re.search("(\([.]+\))", preprocessed_text):
                text = ""
                for part in re.split("(\([.]+\))", original_text):
                    if not re.search("(\([.]+\))", part):
                        text += part[:-1] # [:-1] to strip off extra space from regex splot
                preprocessed_text = text
            # remove parentheses that fill in incomplete words since the model wasn't trained on this formatting
            while parentheses := re.search("\(.+?\)", preprocessed_text):
                preprocessed_text = preprocessed_text[0:parentheses.start()] + preprocessed_text[parentheses.start()+1:parentheses.end()-1] + preprocessed_text[parentheses.end():]
            while parentheses := re.search("\<.+?\>", preprocessed_text):
                preprocessed_text = preprocessed_text[0:parentheses.start()] + preprocessed_text[parentheses.start()+1:parentheses.end()-1] + preprocessed_text[parentheses.end():]
            # preprocess out coded items like &-uh and &=coughs
            preprocessed_text = re.sub(r'&-\w+', '', preprocessed_text)
            preprocessed_text = re.sub(r'&=\w+', '', preprocessed_text)
            # preprocess out anything inside brackets []
            preprocessed_text = re.sub(r'\[[^\]]*\]\s?', '', preprocessed_text)
            # preprocess out @s tags that are sometimes added to code switched text
            preprocessed_text = re.sub(r'@s', '', preprocessed_text)
            # preprocess out quotes symbols
            preprocessed_text = re.sub(r'\+"/', '', preprocessed_text)
            preprocessed_text = re.sub(r'\+"', '', preprocessed_text)
            # finally, use punctuation to hint removal of timestamps
            preprocessed_text = preprocessed_text.split(".")[0]
            preprocessed_text = preprocessed_text.split("?")[0]
            return preprocessed_text
        except:
            pass # print("failed to parse", line)

def parse_utterances_from_cha(input_filename):
    utterances = []
    with open(input_filename, 'r', errors="ignore") as inFile:
        raw_lines = [line for line in inFile]
        i = 0
        while i < len(raw_lines):
            line = raw_lines[i]
            if raw_lines[i][0] == "@":
                utterances.append(line)
                i+=1
            elif "*PAR:" in raw_lines[i][:10]: # each utterance by the participant starts with this marker
                if re.search(r'[0-9]_[0-9]', line):
                    i+=1
                else:
                    while not re.search(r'[0-9]_[0-9]', line): # CLAN forces a new line on long utterances, the timestamp is at the end of all utterances
                        i+=1
                        line += raw_lines[i]
                utterances.append(line)
            else:
                i+=1
    return utterances

def sentence_to_tsv(sentence, path):
    with open (path, 'w', 'utf-16') as stream:
        stream.write("word\t tag\n")
        for token in sentence:
            tag = token.get_label('upos')
            stream.write(token.text)
            stream.write("\t ")
            stream.write(tag.value)
            stream.write('\n')

def count_target_word_occurences(line:str, target_words:list, target_lexical_classes:str=None):
    """
    Inputs:
        - line: %pos tier line from a .cha file, the whole raw string
        - target_word: the word to look for
        - target_lexical_class: (optional) the word must also belong to this lexical class
    Outputs:
        The number of times the targe word appears in the input string
    """
    tokens = line.split(" ") # split up tokens by white space
    if tokens[0] != "%pos:":
        raise ValueError("count_target_word_occurences expects a %pos tier as input")
    del tokens[0] # now we can ignore that

    # now actually count occurances
    occurances = 0
    for token in tokens:
        word = token.split(".")[0]
        lexical_class = token.split(".")[1]
        if word in target_words and lexical_class in target_lexical_classes:
            occurances += 1
    return occurances

def convert_milliseconds_to_seconds(timestamp: str):
    # first filter out any "weird" characters
    milliseconds = ""
    for char in timestamp:
        if char.isalnum():
            milliseconds += char
    # Convert milliseconds to seconds and round to nearest integer
    total_seconds = round(float(milliseconds) / 1000.0)
    # Calculate minutes and seconds
    minutes, seconds = divmod(total_seconds, 60)
    # Return formatted string
    return f"{minutes}:{str(seconds).zfill(2)}"

def extract_occurances_and_times_from_cha(filepath: str, target_words:list, target_lexical_classes:list=None):
    """
    Inputs:
        - filepath: A path to a .cha file that has been annotated with %pos annotation tiers.
    Outputs:
        A list of tuples of the format (word_occurances, utterance_end_timestamp)
    """
    result = []
    with open(filepath, 'r', encoding='utf-8', errors="ignore") as cha_file:
        timestamp = 0
        for line in cha_file:
            if "%pos" in line[0:5]:
                try:
                    result.append((count_target_word_occurences(line, target_words, target_lexical_classes), convert_milliseconds_to_seconds(timestamp)))
                except:
                    print(line, timestamp, filepath)
            elif line[0] != '@' and "%pos" not in line:
                timestamp_maybe = (line.split(" ")[-1]).split("_")[-1] # the timestamp is at the very end of the line
                if re.match(r'\d+', timestamp_maybe):
                    timestamp = timestamp_maybe
                else:
                    timestamp_maybe
    return result