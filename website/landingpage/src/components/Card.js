import React from 'react';

const Card = ({ member }) => {
    return (
      <div className="max-w-sm rounded overflow-hidden shadow-lg m-4">
        {/* <img className="w-full" src={member.image} alt={member.name} /> */}
        <div className="px-6 py-4">
          <div className="font-bold text-xl mb-2">{member.name}</div>
          <p className="text-gray-700 text-base">
            {member.description}
          </p>
        </div>
      </div>
    );
  };

export default Card
  