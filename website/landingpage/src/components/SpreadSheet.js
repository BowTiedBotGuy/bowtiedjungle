import React from 'react';
import Navbar from './NavBar';

const SpeadSheet = () => {
  const iframeSrc = "https://docs.google.com/spreadsheets/d/1cQ0rZ7nDSJlfIPNZ97le52M3mcvZdRsn3t4QAV13Eos/pubhtml?gid=0&amp;single=true&amp;widget=true&amp;headers=false";

  return (
    <div>
      <Navbar />
      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <a href='https://docs.google.com/spreadsheets/d/1cQ0rZ7nDSJlfIPNZ97le52M3mcvZdRsn3t4QAV13Eos/edit?usp=sharing'
           style={{ fontSize: '24px', color: 'blue', textDecoration: 'none', fontWeight: 'bold' }}
           target="_blank" rel="noopener noreferrer">
          Editable Version
        </a>
      </div>
    <div style={{ width: '100%', height: '500px', overflow: 'hidden' }}>
      <iframe title="BowTiedList"
        src={iframeSrc}
        width="100%"
        height="100%"
        style={{ border: 'none' }}
        allowFullScreen
      ></iframe>
    </div>
    </div>
  );
};

export default SpeadSheet;

