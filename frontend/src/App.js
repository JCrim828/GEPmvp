import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import CrawlerPage from './pages/CrawlerPage';
import CrawlerDetails from './pages/CrawlerDetails';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CrawlerPage />} />
        <Route path="/details" element={<CrawlerDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
