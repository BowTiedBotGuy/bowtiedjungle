import React from 'react';

const Navbar = () => {
    return (
      <nav className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <div>
            <a href="/" className="text-lg font-bold">BowTiedList Clone</a>
          </div>
          <div>
            <a href="/about" className="ml-4">About</a>
            <a href="/services" className="ml-4">Services</a>
            <a href="/contact" className="ml-4">Contact</a>
          </div>
        </div>
      </nav>
    );
  };

export default Navbar
  