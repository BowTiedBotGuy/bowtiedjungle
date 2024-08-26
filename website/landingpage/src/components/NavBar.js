import React, { useState } from 'react';
import Modal from './Modal';

// css
import '../Search.css'; 

const Navbar = () => {
  const [isModalOpen, setModalOpen] = useState(false);
  const [searchInput, setSearchInput] = useState('');

  const handleSearchChange = (event) => {
    setSearchInput(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    // Implement search logic or redirect to a search page with the query
    console.log("Searching for:", searchInput);
    // Redirect or update state with search results
  };

  return (
    <>
      <nav className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <a href="/" className="text-lg font-bold">BowTiedList</a>
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
          <div>
            {/* Use button instead of <a> for non-navigation actions */}
            <a href="/billing" className="ml-4">Billing</a>
            <button
            onClick={() => setModalOpen(true)}
            className="ml-4 bg-red-500 text-white cursor-pointer py-2 px-4 rounded">
            Sign Up
            </button>
          </div>
        </div>
      </nav>
      <Modal isOpen={isModalOpen} closeModal={() => setModalOpen(false)} />
    </>
  );
};

export default Navbar;
