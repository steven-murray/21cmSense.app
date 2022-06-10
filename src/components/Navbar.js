import React, { useState } from 'react';
//import { Button } from './Button';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
	const [click, setClick] = useState(false);
	//const [button, setButton] = useState(true);

	const handleClick = () => setClick(!click);
	const closeMobileMenu = () => setClick(false);

	// const showButton = () => {
	//     setButton(true);
	// };

	// useEffect(() => {
	//   showButton();
	// }, []);

	// window.addEventListener('resize', showButton);

	return (
	  <>
	    <nav className='navbar'>
		 <div className='navbar-container'>
		   <Link to='/' className='navbar-logo' onClick={closeMobileMenu}>
			21cmSense
		   </Link>
		   <div className='menu-icon' onClick={handleClick}>
			<i className={click ? 'fas fa-times' : 'fas fa-bars'} />
		   </div>
		 </div>
	    </nav>
	  </>
	);
   }

   export default Navbar;
