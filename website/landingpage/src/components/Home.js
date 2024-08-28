import React from 'react';
import Navbar from './NavBar';
import Hero from './Hero';
import BowTiedList from './BowTiedList'


const Home = () => {
  return (
    <div>
      <Navbar />
      <Hero />
      <BowTiedList />
    </div>
  );
};

export default Home