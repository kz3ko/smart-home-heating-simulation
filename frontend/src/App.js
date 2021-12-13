import logo from './logo.svg';
import './App.css';
import {useState} from "react";

function App() {
  const [message, setMessage] = useState('Waiting for response from API...')

  fetch('/home')
    .then(response => response.json())
    .then(jsonResponse => {
      setMessage(jsonResponse['message'])
    })

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          {message}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
