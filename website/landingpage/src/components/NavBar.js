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
        <div className="container mx-auto flex flex-col md:flex-row justify-between items-center">
          {/* Home Link */}
          <div className="w-full md:w-auto mb-2 md:mb-0">
            <Link to="/" className="text-lg font-bold block text-center md:text-left">BowTiedList</Link>
          </div>
          {/* Search Form */}
          <form onSubmit={handleSearchSubmit} className="w-full md:w-auto mb-2 md:mb-0 flex justify-center md:justify-start">
            <input
              type="text"
              value={searchInput}
              onChange={handleSearchChange}
              placeholder="Search categories/members"
              className="w-full md:w-64 p-2 text-black rounded"
            />
          </form>
          {/* Spreadsheet Link */}
          <Link
            to="/spreadsheet"
            className="w-full md:w-auto bg-red-500 text-white cursor-pointer py-2 px-4 rounded text-center"
          >
            Spreadsheet
          </Link>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
