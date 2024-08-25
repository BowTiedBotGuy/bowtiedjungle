import React from 'react';

function App() {
  const experts = [
    { id: 1, name: "John Doe", expertise: "Web Development", twitter: "@johndoe" },
    { id: 2, name: "Jane Smith", expertise: "Data Science", twitter: "@janesmith" },
  ];

  return (
    <div className="App">
      <header className="bg-blue-500 text-white p-4 font-bold text-lg">
        Expert List
      </header>
      <div className="p-4">
        {experts.map(expert => (
          <div key={expert.id} className="border p-4 rounded mb-2 shadow">
            <h2 className="text-xl font-bold">{expert.name}</h2>
            <p>{expert.expertise}</p>
            <p>{expert.twitter}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

