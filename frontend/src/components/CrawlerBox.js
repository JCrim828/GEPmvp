import React from 'react';
import './CrawlerBox.css';

const CrawlerBox = ({ crawler, date_accessed, frequency, tone }) => {
    return (
        <div className='crawlerBox'>
            <div className='crawlerColumn'>{crawler}</div>
            <div>{date_accessed}</div>
            <div>{frequency}</div>
            <div>
                <span className={`toneDot ${tone}`}></span>
            </div>
            <div className='moreColumn'>
                <a href="#">More &gt;</a>
            </div>
        </div>
    );
};

export default CrawlerBox;