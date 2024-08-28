import React, { useState, useEffect } from 'react';
import API from '../services/API'; // Ensure this path is correct for your API service
import LoadingBar from './LoadingBar'; // Ensure this path is correct for your LoadingBar component

const GroupCard = ({ group }) => (
  <div className="bg-white p-4 rounded-lg shadow-md flex flex-col space-y-2">
    <h2 className="text-lg font-semibold">{group.name}</h2>
    <a href={`https://x.com/${group.x_handle}`} className="text-blue-500">
      {group.x_handle}
    </a>
    {group.substack && (
      <a href={group.substack} className="text-blue-500">
        Substack
      </a>
    )}
    {group.product_service && (
      <a href={group.product_service} className="text-blue-500">
        Product
      </a>
    )}
    <p className="text-sm text-gray-500">{group.categories}</p>
  </div>
);

const BowTiedList = () => {
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

  return (
    <div className="p-4">
      {isLoading ? ( // Show loading bar while loading
        <LoadingBar />
      ) : (
        <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {list.map((group) => (
            <GroupCard key={group.id} group={group} />
          ))}
        </div>
      )}
    </div>
  );
};

export default BowTiedList;
