import React from 'react';

const Trigger = ({ triggerText, buttonRef, showModal, buttonClass }) => {
  return (
    <button
      className={buttonClass}
      ref={buttonRef}
      onClick={showModal}
    >
      {triggerText}
    </button>
  );
};
export default Trigger;