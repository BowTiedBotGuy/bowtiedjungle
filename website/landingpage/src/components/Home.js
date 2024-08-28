import React , {useState} from 'react';
import Navbar from './NavBar';
import Hero from './Hero';
import BowTiedList from './BowTiedList'


const Home = () => {
    const [searchInput, setSearchInput] = useState('');

    const handleSearchChange = (input) => {
    setSearchInput(input);
    };

    return (
        <div>
        <Navbar onSearchChange={handleSearchChange}/>
        <Hero />
        <BowTiedList searchInput={searchInput} />
        </div>
    );
};

export default Home