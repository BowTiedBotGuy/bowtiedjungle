import React from 'react';
import Navbar from './NavBar';
import Hero from './Hero';
import Card from './Card';
import LatestPosts from './LatestPosts'

const members = [
  { name: "BowTiedBull", image: "https://substackcdn.com/image/fetch/w_96,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F60b51132-7e25-4ce8-ad9c-fe7fae698621_140x140.png", description: "BowTiedBull" },
  // Add more members as needed
];

const Home = () => {
  return (
    <div>
      <Navbar />
      <Hero />
      <div className="container mx-auto flex flex-wrap justify-center">
        {members.map(member => <Card key={member.name} member={member} />)}
      </div>
      <LatestPosts />
    </div>
  );
};

export default Home