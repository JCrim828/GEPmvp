import './CrawlerPage.css';
import '../api';
import React, {useState, useEffect, useRef } from 'react'
import Navbar from '../components/Navbar';
import CrawlerBox from '../components/CrawlerBox'; 

const App = () => {

}


function CrawlerPage() {

  const [crawlers, setCrawlers] = useState([]);
  const crawlerData = [
      { crawler: "ChatGPT", date_accessed: "May 9 2025 : 14:55:43", frequency: 11, tone: "red" },
      { crawler: "ChatGPT", date_accessed: "May 9 2025 : 14:55:43", frequency: 11, tone: "red" },
      { crawler: "ChatGT", date_accessed: "May 7 2025 : 14:55:43", frequency: 19, tone: "green" },
      { crawler: "Gemini", date_accessed: "Apr 9 2020 : 14:55:43", frequency: 1, tone: "orange" }, 
      { crawler: "ChatGPT", date_accessed: "May 9 2025 : 14:55:43", frequency: 11, tone: "red" },
      { crawler: "ChatGPT", date_accessed: "May 9 2025 : 14:55:43", frequency: 11, tone: "red" },
      { crawler: "ChatGT", date_accessed: "May 7 2025 : 14:55:43", frequency: 19, tone: "green" },
      { crawler: "Gemini", date_accessed: "Apr 9 2020 : 14:55:43", frequency: 1, tone: "orange" }
    ];
  
  useEffect(() => {
    setCrawlers(crawlerData);
  }, []);

  

  return (
    <div>
      <Navbar></Navbar>

      <div className="crawlerPage">
        <div className='crawlerList'>
          <div className='crawlerHeaders'>
            <div className='crawlerColumn'>Crawler Name</div>
            <div>Date & Time Accessed</div>
            <div>Access Frequency</div>
            <div>Tone</div>
            <button>Filter &gt;</button>
          </div>

          {crawlers.map((c, index) => (
            <CrawlerBox
              key={index}
              crawler={c.crawler}
              date_accessed={c.date_accessed}
              frequency={c.frequency}
              tone={c.tone}
            />
          ))}

        </div>
      </div>
    </div>
  );
};

export default CrawlerPage;
