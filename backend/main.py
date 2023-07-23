from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
from flair.models import SequenceTagger
from flair.data import Sentence
from fastapi.middleware.cors import CORSMiddleware
from corpus_tool import Corpus, Transcript, Visualizer

app = FastAPI()

# CORS configuration
origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://146.190.141.184:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tagger = None #SequenceTagger.load('benevanoff/spanglish-upos')
corpus = Corpus('transcriptions')
visualizer = Visualizer(corpus)

class WordsRequest(BaseModel):
    words: str

class CorpusVizRequest(BaseModel):
    groups: List[int]
    target_language: Optional[str]
    part_of_speech_filter: Optional[List[str]]
    N_most_frequent: Optional[int]

def preprocess_viz_req(viz_request):
    print(viz_request.groups, viz_request.target_language, viz_request.N_most_frequent)
    viz_request.target_language = None if viz_request.target_language == "both" else viz_request.target_language
    viz_request.N_most_frequent = None if viz_request.N_most_frequent == 0 else viz_request.N_most_frequent
    return viz_request

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

def tag_sentence(sentence: list):
    """
    Take an input list of words and return a list of dictionaries
    with they keys "token_text" and "token_tag"
    """
    flair_sentence = Sentence(sentence)
    tagger.predict(flair_sentence)
    return [{"token_text":tok.text, "token_tag": tok.tag} for tok in flair_sentence]

@app.post("/words")
async def tag_words(request: Request, words_request: WordsRequest):
    words = words_request.words
    return tag_sentence(words_request.words.split(" "))

@app.post("/viz_barchart")
async def corpus_viz(request: Request, viz_request: CorpusVizRequest):
    viz_request = preprocess_viz_req(viz_request)
    return visualizer.word_freq_barchart_group(groups=viz_request.groups, target_lang=viz_request.target_language, top_N_most_frequent=viz_request.N_most_frequent, POS_filter=viz_request.part_of_speech_filter)

@app.post("/viz_mtld_boxplot")
async def corpus_viz_mtld_boxplot(request: Request, viz_request: CorpusVizRequest):
    viz_request = preprocess_viz_req(viz_request)
    return visualizer.mtld_boxplot(target_lang=viz_request.target_language)

@app.post("/viz_mattr_boxplot")
async def corpus_viz_mattr_boxplot(request: Request, viz_request: CorpusVizRequest):
    viz_request = preprocess_viz_req(viz_request)
    return visualizer.mattr_boxplot(target_lang=viz_request.target_language)

@app.post("/viz_word_cloud")
async def corpus_viz_word_cloud(request: Request, viz_request: CorpusVizRequest):
    viz_request = preprocess_viz_req(viz_request)
    return visualizer.gen_word_cloud(group_filter=viz_request.groups, target_lang_filter=viz_request.target_language, POS_filter=viz_request.part_of_speech_filter)