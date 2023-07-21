from fastapi.testclient import TestClient
from main import tag_sentence
from main import app

def test_tag_sentence():
    result = tag_sentence("This is a test")
    assert len(result) == 4
    assert result[0]['token_text'] == 'This'
    assert result [0]['token_tag'] == 'PRON'
    assert result[1]['token_text'] == 'is'
    assert result [1]['token_tag'] == 'AUX'
    assert result[2]['token_text'] == 'a'
    assert result [2]['token_tag'] == 'DET'
    assert result[3]['token_text'] == 'test'
    assert result [3]['token_tag'] == 'NOUN'
    
def test_post_words_route():
    result = TestClient(app).post("/words", json={"words": "This is a test"})
    assert result.status_code == 200
    result = result.json()
    assert len(result) == 4
    assert result[0]['token_text'] == 'This'
    assert result [0]['token_tag'] == 'PRON'
    assert result[1]['token_text'] == 'is'
    assert result [1]['token_tag'] == 'AUX'
    assert result[2]['token_text'] == 'a'
    assert result [2]['token_tag'] == 'DET'
    assert result[3]['token_text'] == 'test'
    assert result [3]['token_tag'] == 'NOUN'