import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../Search.css'; 

const Navbar = ({ onSearchChange }) => {
  const [searchInput, setSearchInput] = useState('');

  const handleSearchChange = (event) => {
    const input = event.target.value;
    setSearchInput(input);
    onSearchChange(input); // Call the prop function to lift the state up
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    console.log("Searching for:", searchInput);
    // Additional logic to handle search submit
  };

  return (
    <>
      <nav className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <div>
            <Link to="/" className="text-lg font-bold mr-4">BowTiedList</Link>
          </div>
          <form onSubmit={handleSearchSubmit} className="search-form">
            <input
              type="text"
              value={searchInput}
              onChange={handleSearchChange}
              placeholder="Search categories/members"
              className="search-input"
            />
            <button type="submit" className="search-button">Search</button>
          </form>
          <Link to="/spreadsheet" className="ml-4 bg-red-500 text-white cursor-pointer py-2 px-4 rounded">Spreadsheet</Link>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
