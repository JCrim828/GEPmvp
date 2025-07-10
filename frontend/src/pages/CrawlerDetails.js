import React, { useState, useEffect } from 'react';
import './CrawlerDetails.css';
import Navbar from '../components/Navbar';
import MyPieChart from '../components/PieChart';
import Legend from '../components/Legend';
import pieChart from '../assets/pieChart.png'

const CrawlerDetails = () => {

    const [gPercent, setgPercent] = useState(58);
    const [rPercent, setrPercent] = useState(43);
    const [oPercent, setoPercent] = useState(32);
    const total = rPercent + gPercent + oPercent;
    const testRawText = 'Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text Raw Text.';

    return (
        <div>
            <Navbar></Navbar>
            <div className='twoColumnContainer'>

                <div className='leftContainer'>
                    <div className="overviewBox">
                        <div className="overviewHeaderRow">
                            <div className="leftContainerMini">
                                <h1>GPTBot</h1>
                            </div>
                            <div className="rightContainerMini">
                                <a href='https://chat.openai.com/' target='_blank' rel="noopener noreferrer">
                                    https://chat.openai.com/
                                </a>
                            </div>
                        </div>
                        <div className="overviewBody">
                            <p>Accessed on: June 6, 2025 at 21:46:23</p>
                            <p>Access Count: 3</p>
                        </div>
                    </div>
                    <div className='pieChartBox'>
                        <div className='position-relative'>
                            <h1 className='toneHeader'>Tone Data</h1>
                            <img src={pieChart} alt='pieLogo' className='pieLogo' />
                        </div>
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
                        <h1>Summary</h1>
                        <p>{ testRawText }</p>
                    </div>
                </div>

            </div>
        </div>
    )
}

export default CrawlerDetails;