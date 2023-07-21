import React, { useRef, useState } from 'react';
import './VisualizerForm.css';

function VisualizerForm() {
    const possiblePOS = ["DET", "NOUN", "PRON", "PROPN", "VERB", "AUX", "ADV", "ADJ", "ADP", "CCONJ", "SCONJ", "PART", "INTJ", "NUM", "SYM", "PUNT", "X"];
    const possibleGroups = ["100", "200", "300", "400", "500", "600", "700"];
    
    // states
    const [groups, setGroups] = useState(possibleGroups);
    const [parts_of_speech, setPartsOfSpeech] = useState(possiblePOS);
    const [target_language, setTargetLanguage] = useState("both");
    const [plot_img, setPlotImg] = useState(null);

    // references
    const top_n_ref = useRef(null);

    // UI event handlers
    const onTargetLangButtonPressed = e => setTargetLanguage(e.target.value);
    const onGroupCheckboxPressed = e => {
        let tmp = [];
        for (let i = 0; i < groups.length; i++) {
            if (groups[i] === e.target.value)
                continue;
            else
                tmp.push(groups[i]);
        }
        if (tmp.length === groups.length)
            tmp.push(e.target.value);
        setGroups(tmp);
    };
    const isUsingGroup = (group) => {
        for (let i = 0; i < groups.length; i++) {
            if (groups[i] === group)
                return true;
        }
        return false;
    };
    const onPOSCheckboxPressed = e => {
        let tmp = [];
        for (let i = 0; i < parts_of_speech.length; i++) {
            if (parts_of_speech[i] === e.target.value)
                continue;
            else
                tmp.push(parts_of_speech[i]);
        }
        if (tmp.length === parts_of_speech.length)
            tmp.push(e.target.value);
        setPartsOfSpeech(tmp);
    };
    const isUsingPOS = (pos_tag) => {
        for (let i = 0; i < parts_of_speech.length; i++) {
            if (parts_of_speech[i] === pos_tag)
                return true;
        }
        return false;
    };

    const requestPlot = async () => {
        console.log(groups);
        console.log(parts_of_speech);
        console.log(target_language);
        console.log(top_n_ref.current.value);
        try {
            let top_n_param = top_n_ref.current.value === "" ? 0 : top_n_ref.current.value
            const response = await fetch("http://127.0.0.1:8000/viz", {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({"groups": groups, "target_language": target_language, "part_of_speech_filter": parts_of_speech,  "N_most_frequent": top_n_param}),
            });
            const responseData = await response.json();
            setPlotImg(responseData);
          } catch (error) {
            console.error('Error:', error);
        }
    }

    // HTML components to render
    const renderPlot = () => {
        if (plot_img !== null) {
            return <img src={"data:img/png;base64,"+plot_img} alt="barchart should go here" className="barchart"></img>;
        }
    };
    const renderGroupCheckboxes = () => {
        return possibleGroups.map((group, index) => (
            <div>
              <input type="checkbox" id={"group-"+{group}+"-checkbox"} value={group} onChange={onGroupCheckboxPressed} checked={isUsingGroup(group)}></input>
              <label>{group}</label>
            </div>
        ));
    };
    const renderPOSCheckboxes = () => {
        return possiblePOS.map((tag, index) => (
            <div key={index}>
              <input type="checkbox" value={tag} id={tag} onChange={onPOSCheckboxPressed} checked={isUsingPOS(tag)}></input>
              <label>{tag}</label>
            </div>
        ));
    };

    return (
    <div>
      <div>
        <label>Groups: </label>
        <div className="pos-boxes">
          {renderGroupCheckboxes()}
        </div>
      </div>
      <div>
        <label>Target Language: </label>
        <input type="radio" id="both_target_lang" name="both_lang" value="both" onChange={onTargetLangButtonPressed} checked={target_language === "both"}></input>
        <label htmlFor='both_target_lang'>Both</label>
        <input type="radio" id="eng_target_lang" name="english" value="eng" onChange={onTargetLangButtonPressed} checked={target_language === "eng"}></input>
        <label htmlFor='eng_target_lang'>English</label>
        <input type="radio" id="spa_target_lang" name="spanish" value="spa" onChange={onTargetLangButtonPressed} checked={target_language === "spa"}></input>
        <label htmlFor='spa_target_lang'>Spanish</label>
      </div>
      <div>
        <label>Parts of Speech: </label>
        <div className="pos-boxes">
          {renderPOSCheckboxes()}
        </div>
      </div>
      <div>
        <label>Only N most frequent: </label>
        <input id="N-most-frequent" ref={top_n_ref}></input>
      </div>
      <div>
        <button onClick={requestPlot}>Generate Plot</button>
      </div>
      <div>
        {renderPlot()}
      </div>
    </div>
    );
  }
  
  export default VisualizerForm