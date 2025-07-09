import React from 'react';
import './Legend.css';

const Legend = ({gPercent, oPercent, rPercent}) => {
  return (
    <div className="legend">
      <div className="legend-item">
        <div className="color-box green" />
        <span>{gPercent}%</span>
      </div>
      <div className="legend-item">
        <div className="color-box orange" />
        <span>{oPercent}%</span>
      </div>
      <div className="legend-item">
        <div className="color-box red" />
        <span>{rPercent}%</span>
      </div>
    </div>
  );
};

export default Legend;