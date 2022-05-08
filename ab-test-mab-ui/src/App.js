import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';
import { useCookies } from 'react-cookie';

function App() {

  var [time, setTime] = useState(0);
  const [cookies, setCookie] = useCookies(['rl_subid', 'rl_config']);

  useEffect(() => {

    const interval = setInterval( async () => {
      const response = await fetch('http://127.0.0.1:5000/');
      const data = await response.json();
      setTime(data.time);
    }, 1000);

    if (cookies.rl_subid || cookies.rl_config){
      // Handle case where the user has already completed the Test
      console.log("debug cookies here");
    }
    else{
      console.log("Cookie not found");
    }


    // useEffect may return "cleanup function"
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <br/>
        <p>Backend API test: Current Machine time is {time}</p>
      </header>
    </div>
  );
}

export default App;
