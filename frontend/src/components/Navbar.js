import React from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className='gepLogo'>*GEP LOGO*</div>
            <ul className='navLinks'>
                <Link to="/">Crawlers</Link>
                <Link to="/details">Details *testing only*</Link>
                <text>*Account*</text>
            </ul>
        </nav>
    );
};

export default Navbar;