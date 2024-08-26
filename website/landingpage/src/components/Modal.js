import React from 'react';

const Modal = ({ isOpen, closeModal }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={closeModal}>
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <button onClick={closeModal}>&times;</button>
        </div>
        <div className="modal-content">
          {/* Your modal content here */}
          <p>This is where your complex modal content would go.</p>
        </div>
      </div>
    </div>
  );
};

export default Modal;
