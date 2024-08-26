import React, { useState } from 'react';

function App() {
  const [experts, setExperts] = useState([
    { id: 1, name: "John Doe", expertise: "Web Development", twitter: "@johndoe" },
    { id: 2, name: "Jane Smith", expertise: "Data Science", twitter: "@janesmith" },
  ]);

  const [newExpert, setNewExpert] = useState({
    name: '',
    expertise: '',
    twitter: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewExpert(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newId = experts.length ? experts[experts.length - 1].id + 1 : 1;
    setExperts([...experts, { ...newExpert, id: newId }]);
    setNewExpert({ name: '', expertise: '', twitter: '' }); // Reset form
  };

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
        <form onSubmit={handleSubmit} className="mt-4">
          <div className="mb-3">
            <label className="block font-bold mb-2">Name:</label>
            <input
              type="text"
              name="name"
              value={newExpert.name}
              onChange={handleInputChange}
              className="border p-2 w-full"
              required
            />
          </div>
          <div className="mb-3">
            <label className="block font-bold mb-2">Expertise:</label>
            <input
              type="text"
              name="expertise"
              value={newExpert.expertise}
              onChange={handleInputChange}
              className="border p-2 w-full"
              required
            />
          </div>
          <div className="mb-3">
            <label className="block font-bold mb-2">Twitter Handle:</label>
            <input
              type="text"
              name="twitter"
              value={newExpert.twitter}
              onChange={handleInputChange}
              className="border p-2 w-full"
            />
          </div>
          <button type="submit" className="bg-blue-500 text-white p-2 rounded">
            Add Expert
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
