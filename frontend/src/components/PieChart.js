import React from 'react';
import './PieChart.css';
import { PieChart } from 'react-minimal-pie-chart';

const MyPieChart = ({greenPercent, redPercent, orangePercent}) => (
    <div className='pieWrapper'>
        <PieChart className='pie'
            data={[
            { title: 'Green', value: greenPercent, color: '#2ecc71' },
            { title: 'Orange', value: orangePercent, color: '#d98c00' },
            { title: 'Red', value: redPercent, color: '#e74c3c' },
            ]}
        />
    </div>
);

export default MyPieChart;