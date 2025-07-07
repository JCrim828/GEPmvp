import './CrawlerPage.css';
import '../api';
import React, {useState, useEffect} from 'react'
import Navbar from '../components/Navbar';
import CrawlerBox from '../components/CrawlerBox'; 

const App = () => {

}

function crawlerPage() {
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
          <CrawlerBox
            crawler="ClaudeBot"
            date_accessed="May. 28 2025 : 11:22:29"
            frequency={11}
            tone="red"
          />
          <CrawlerBox
            crawler="GPTBot"
            date_accessed="June. 9 2025 : 14:20:59"
            frequency={6}
            tone="green"
          />
          <CrawlerBox
            crawler="Google Gemini"
            date_accessed="May. 20 2025 : 01:35:44"
            frequency={8}
            tone="orange"
          />
          <CrawlerBox
            crawler="GPTBot"
            date_accessed="May. 2 2025 : 16:20:40"
            frequency={4}
            tone="green"
          />
          <CrawlerBox
            crawler="ClaudeBot"
            date_accessed="May. 28 2025 : 11:22:29"
            frequency={11}
            tone="orange"
          />
          <CrawlerBox
            crawler="ClaudeBot"
            date_accessed="May. 28 2025 : 11:22:29"
            frequency={11}
            tone="green"
          />

        </div>
      </div>
    </div>
  );
};

export default crawlerPage;
