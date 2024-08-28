import React, { useState, useEffect } from 'react';
import API from '../services/API'; // Ensure this path is correct for your API service
import LoadingBar from './LoadingBar'; // Ensure this path is correct for your LoadingBar component

const MemberCard = ({ member }) => (
  <div className="bg-white p-4 rounded-lg shadow-md flex flex-col space-y-2">
    <h2 className="text-lg font-semibold">{member.name}</h2>
    <a href={member.x_handle} className="text-blue-500">
      {member.x_handle}
    </a>
    {member.substack && (
      <a href={member.substack} className="text-blue-500">
        Substack
      </a>
    )}
    {member.product_service && (
      <a href={member.product_service} className="text-blue-500">
        Product
      </a>
    )}
    <p className="text-sm text-gray-500">{member.categories}</p>
  </div>
);

const BowTiedList = ({ searchInput }) => {
  const [list, setList] = useState([]);
  const [isLoading, setIsLoading] = useState(true); // Add a loading state

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true); // Set loading to true before fetching data
        const response = await API.get('/bowtiedlist');
        setList(response.data); // Access the nested 'data' array
      } catch (error) {
        console.error('Error fetching data: ', error);
      } finally {
        setIsLoading(false); // Set loading to false after fetching data
      }
    };

    fetchData();
  }, []);

  const filteredList = list.filter((member) =>
    searchInput === '' || 
    member.name.toLowerCase().includes(searchInput.toLowerCase()) ||
    member.categories.toLowerCase().includes(searchInput.toLowerCase())
  );

  return (
    <div className="p-4">
      {isLoading ? ( // Show loading bar while loading
        <LoadingBar />
      ) : (
        <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {filteredList.map((member) => (
            <MemberCard key={member.id} member={member} />
          ))}
        </div>
      )}
    </div>
  );
};

export default BowTiedList;
