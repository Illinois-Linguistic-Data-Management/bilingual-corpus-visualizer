from corpus_tool import Corpus, Transcript
from trankit import Pipeline

def thing():
        corpus = Corpus('transcriptions')
        pipeline = Pipeline("spanish")
        with open('clitics.csv', 'w') as file:
                data = {}
                for transcript in corpus.transcripts:
                        print(transcript.participant_id, transcript.main_lang)
                        if transcript.main_lang != "spa":
                                continue
                        group_id = str(transcript.participant_id)[0]
                        try:
                                for utterance in transcript.utterances:
                                        eng_toks = [x for x in utterance['tokens'] if x.split(".")[2] == "eng"]
                                        spa_toks = [x.split(".")[0] for x in utterance['tokens'] if x.split(".")[2] == "spa"]
                                        utt_lang = "eng" if len(eng_toks) > len(spa_toks) else "spa"
                                        if utt_lang == "spa":
                                                tokens = pipeline.tokenize(" ".join(spa_toks), is_sent=True)['tokens']
                                                for token in tokens:
                                                        if "expanded" in token:
                                                                print(token['text'], token['expanded'])
                                                                exp_tok_text = token['expanded'][1]['text']
                                                                if exp_tok_text in ['lo', 'los', 'la', 'las', 'le', 'les']:
                                                                        print(token)
                                                                        file.write(f"{transcript.participant_id}, {token['expanded'][1]['text']}")
                                                                        file.write("\n")
                        except:
                                print("error!!", transcript.participant_id)

if __name__ == "__main__":
        thing()