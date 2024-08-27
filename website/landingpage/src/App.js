import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Spreadsheet from './components/SpreadSheet';

function App() {
  return (
    <Router>
      <div>
        <Routes> {/* Updated from Switch to Routes */}
          <Route path="/spreadsheet" element={<Spreadsheet />} /> {/* Updated Route syntax */}
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
