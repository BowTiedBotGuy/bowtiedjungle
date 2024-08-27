import React from 'react';
import Navbar from './NavBar';
import Hero from './Hero';
import LatestPosts from './LatestPosts'


const Home = () => {
  return (
    <div>
      <Navbar />
      <Hero />
      <LatestPosts />
    </div>
  );
};

export default Home