import React, { useState, useRef } from 'react';
import './TaggerForm.css';

const TaggerForm = () => {
  const [inputValue, setInputValue] = useState('');
  let [bubbleColor, setBubbleColor] = useState([]);
  let [posTags, setPosTags] = useState([]);
  const inputRef = useRef(null);
  const lastQueriedWordsRef = useRef(null);

  const lexical_class_colors = {
    "DET": '#996633',
    "ADJ": '#ff00ff',
    "NOUN": '#ff6600',
    "PRON": '#cc3300',
    "PROPN": '#ffff00',
    "AUX": '#00ffcc',
    "VERB": '#3399ff',
    "ADV": '#00cc00',
    "ADP": '#9933ff',
    "CCONJ": '#ff3399',
    "SCONJ": '#ff8080',
    "PART": '#66ff33',
    "INTJ": '#ff99ff',
    "PUNCT": '',
    "X": ''
  }

  const getTags = async (words) => {
    console.log(words);
    try {
      const response = await fetch("http://127.0.0.1:8000/words", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"words": words}),
      });
      const responseData = await response.json();
      console.log('Response:', responseData);
      for (let i = 0; i < responseData.length; i++) {
        posTags[i] = responseData[i]['token_tag'];
        bubbleColor[i] = lexical_class_colors[responseData[i]['token_tag']];
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleInputChange = async (e) => {
    bubbleColor = new Array(e.target.value.split(" ").length).fill('#ff0000');
    posTags = new Array(e.target.value.split(" ").length).fill('POS');
    setInputValue(e.target.value);
    adjustInputHeight();
    if (lastQueriedWordsRef.current !== e.target.value) {
        await getTags(e.target.value);
    }
    lastQueriedWordsRef.current = e.target.value;
    console.log(bubbleColor, posTags);
    setBubbleColor(bubbleColor);
    setPosTags(posTags);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Input value:', inputValue);
  };

  const adjustInputHeight = () => {
    const inputElement = inputRef.current;
    if (inputElement) {
     inputElement.style.height = 'auto';
     inputElement.style.height = `${inputElement.scrollHeight}px`;
    }
  };

  const renderWordBubbles = () => {
    const wordsa = inputValue.split(' ');
    let words = []
    for (let i = 0; i < wordsa.length; i++){
        if(wordsa[i] !== "") {
            words.push(wordsa[i]);
        }
    }
    return words.map((word, index) => (
      <div key={index} className="word-bubble" style={{ backgroundColor: bubbleColor[index] }}>
        <span className="word-label">{word}</span>
        <div className="upos-label">
          <span>{posTags[index]}</span>
        </div>
      </div>
    ));
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="tagger-form">
          <label htmlFor="inputField">Enter Text:</label>
          <br />
          <textarea
            ref={inputRef}
            type="text"
            id="inputField"
            value={inputValue}
            style={{ textAlign: 'center' }}
            onChange={handleInputChange} 
          />
        <div className="word-container">{renderWordBubbles()}</div>
      </form>
    </div>
  );
};

export default TaggerForm;
