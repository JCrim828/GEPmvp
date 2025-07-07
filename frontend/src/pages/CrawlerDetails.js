import React from 'react';
import './CrawlerDetails.css';
import Navbar from '../components/Navbar';

const CrawlerDetails = () => {
    return (
        <div>
            <Navbar></Navbar>
            <div className='twoColumnContainer'>
                <div className='leftContainer'>
                    <div className='overviewBox'>
                        <h1>overview</h1>
                    </div>
                    <div className='pieChartBox'>
                        <h1>pie chart</h1>
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