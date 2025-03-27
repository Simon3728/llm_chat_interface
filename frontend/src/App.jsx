import { useState, useEffect } from 'react'
import axios from 'axios'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [backendMessage, setBackendMessage] = useState('Loading...')
  const [error, setError] = useState(null)
  const [apiInfo, setApiInfo] = useState({})

  useEffect(() => {
    // Get API URL from environment variables
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    // Log for debugging
    console.log('Using API URL:', apiUrl);
    setApiInfo({ url: apiUrl });

    const fetchBackendData = async () => {
      try {
        const response = await axios.get(`${apiUrl}/api/health`);
        setBackendMessage(response.data.status);
        setError(null);
      } catch (err) {
        console.error('Error fetching from backend:', err);
        setBackendMessage('Failed to connect');
        setError(`${err.message}`);
      }
    };
  
    fetchBackendData();
  }, [])

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          Count is Hurensohn {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      
      <div className="backend-status">
        <h2>Backend Status:</h2>
        <p>{backendMessage}</p>
        <p>API URL: {apiInfo.url}</p>
        {error && <p className="error">Error: {error}</p>}
      </div>
      
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App