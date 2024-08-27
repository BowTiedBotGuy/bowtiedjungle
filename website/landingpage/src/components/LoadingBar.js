import React from 'react';

const LoadingBar = () => {
    return (
        <div className="w-full bg-gray-200">
            <div className="bg-blue-500 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded" style={{ width: '50%' }}>Loading...</div>
        </div>
    );
};

export default LoadingBar;
