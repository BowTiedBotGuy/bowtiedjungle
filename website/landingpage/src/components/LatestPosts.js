import React, { useEffect } from 'react';
import API from '../services/API';

const LatestPosts = () => {
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await API.get('/posts'); // Adjust the method if needed
                console.log(response.data);
            } catch (error) {
                console.error('Error fetching data: ', error);
            }
        };

        fetchData();
    }, []); // The empty array ensures this effect runs only once after the initial render

    return (
        <div>
            {/* Render your component UI here */}
        </div>
    );
};

export default LatestPosts;



