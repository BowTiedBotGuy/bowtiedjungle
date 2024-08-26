import React from 'react';
import '../Modal.css';  // Ensure your CSS file is correctly linked

const Modal = ({ isOpen, closeModal }) => {
  if (!isOpen) return null;

  const handleJoinClick = () => {
    // Here, integrate with Stripe or navigate to a Stripe payment page
    console.log("Proceeding to Stripe Checkout...");
  };

  return (
    <div className="modal-overlay" onClick={closeModal}>
      <div className="modal-container" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <button onClick={closeModal} className="modal-close-btn">&times;</button>
          <h2>Join Our Community</h2>
        </div>
        <div className="modal-body">
          <div className="features">
            <h3>Features</h3>
            <ul>
              <li>Access to detailed analytics</li>
              <li>Exclusive member content</li>
              <li>Direct support from experts</li>
            </ul>
          </div>
          <div className="divider"></div>
          <div className="form-section">
            <h3>Sign Up</h3>
            <input type="email" placeholder="Enter your email" className="input-field" />
            <input type="text" placeholder="Twitter handle" className="input-field" />
            <button onClick={handleJoinClick} className="join-button">Join Now</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
