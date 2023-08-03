import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Tagger from './Tagger.js';
import Visualizer from './Visualizer.js'

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Visualizer />} />
          <Route path="/spanglish-tagger" element={<Tagger />} />
        </Routes>
      </BrowserRouter>
  );
}

export default App;