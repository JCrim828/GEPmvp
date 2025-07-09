import React, { useState, useEffect } from 'react';
import './CrawlerDetails.css';
import Navbar from '../components/Navbar';
import MyPieChart from '../components/PieChart';
import Legend from '../components/Legend';

const CrawlerDetails = () => {

    const [gPercent, setgPercent] = useState(58);
    const [rPercent, setrPercent] = useState(43);
    const [oPercent, setoPercent] = useState(32);
    const total = rPercent + gPercent + oPercent;

    return (
        <div>
            <Navbar></Navbar>
            <div className='twoColumnContainer'>
                <div className='leftContainer'>
                    <div className='overviewBox'>
                        <h1>overview</h1>
                    </div>
                    <div className='pieChartBox'>
                        <h1 className='toneHeader'>Tone Data</h1>
                        <div className='legendContainer'>
                            <Legend 
                                rPercent={(rPercent / total * 100).toFixed(2)} 
                                oPercent={(oPercent / total * 100).toFixed(2)} 
                                gPercent={(gPercent / total * 100).toFixed(2)} 
                            />
                        </div>
                        <MyPieChart className='pieChart' greenPercent={gPercent} redPercent={rPercent} orangePercent={oPercent} />
                    </div>
                </div>
                <div className='rightContainer'>
                    <div className='rawTextBox'>
                        <h1>raw text</h1>
                    </div>
                </div>

            </div>
        </div>
    )
}

export default CrawlerDetails;