import React, { useState } from 'react';
import Modal from './Modal';

const Navbar = () => {
  const [isModalOpen, setModalOpen] = useState(false);

  return (
    <>
      <nav className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <a href="/" className="text-lg font-bold">Site Name</a>
          <div>
            <a href="/about" className="ml-4">About</a>
            {/* Use button instead of <a> for non-navigation actions */}
            <a href="/billing" className="ml-4">Billing</a>
            <button onClick={() => setModalOpen(true)} className="ml-4 bg-transparent border-none text-white cursor-pointer">
              Shill
            </button>
          </div>
        </div>
      </nav>
      <Modal isOpen={isModalOpen} closeModal={() => setModalOpen(false)} />
    </>
  );
};

export default Navbar;
