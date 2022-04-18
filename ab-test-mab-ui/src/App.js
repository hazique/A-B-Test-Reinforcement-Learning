import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';

function App() {

  var [time, setTime] = useState(0);

  useEffect(() => {

    const fetch_time = async () => {
      const response = await fetch('http://127.0.0.1:5000/');
      const data = await response.json();
      setTime(data.time);
    };

    fetch_time()
  }, [time]);

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
