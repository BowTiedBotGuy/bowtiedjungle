import React from 'react';
import Navbar from './components/NavBar';
import Hero from './components/Hero';
import Card from './components/Card';

const cities = [
  { name: "BowTiedBull", image: "https://substackcdn.com/image/fetch/w_96,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F60b51132-7e25-4ce8-ad9c-fe7fae698621_140x140.png", description: "BowTiedBull" },
  // { name: "Berlin", image: "url-to-image", description: "Vibrant nightlife and deep history." },
  // Add more members as needed
];

const App = () => {
  return (
    <div>
      <Navbar />
      <Hero />
      <div className="container mx-auto flex flex-wrap justify-center">
        {cities.map(member => <Card key={member.name} member={member} />)}
      </div>
    </div>
  );
};

export default App;
