import React, { useState } from 'react';
import Spreadsheet from 'react-spreadsheet';
import Navbar from './NavBar';

const SpreadsheetComponent = () => {
  // Initial data for the spreadsheet
  const initialData = [
    [{ value: "ID" }, { value: "Title" }, { value: "Count" }],
    [{ value: 1 }, { value: "Item 1" }, { value: 100 }],
    [{ value: 2 }, { value: "Item 2" }, { value: 200 }]
  ];

  const [data, setData] = useState(initialData);

  const handleSave = async () => {
    try {
      const response = await fetch('/api/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data }),
      });
      const result = await response.json();
      console.log(result.message);
    } catch (error) {
      console.error('Error saving data:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="p-4 md:p-8">
        <h1 className="text-xl font-semibold mb-4">My Spreadsheet</h1>
        <div className="bg-white shadow-md rounded-lg p-2">
          <Spreadsheet data={data} onChange={setData} />
          <button
            onClick={handleSave}
            className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default SpreadsheetComponent;
