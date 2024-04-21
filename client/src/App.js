import React, { useState, useEffect } from 'react';
import { Input, Button } from 'semantic-ui-react'; // Import Input and Button from Semantic UI React
import './App.css';

function App() {
  const [data, setData] = useState({});
  const [inputValue, setInputValue] = useState('');
  const [response, setResponse] = useState('');

  // Fetch initial data from Flask API
  useEffect(() => {
    fetch("/members")
      .then(res => res.json())
      .then(data => {
        setData(data);
        console.log(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const handleSubmit = async () => {
    try {
      const response = await fetch('/send_input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: inputValue })
      });

      const responseData = await response.json();
      setResponse(responseData.response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      {/* Input Box */}
      <Input
        placeholder="Enter your input"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        action={
          <Button
            content="Submit"
            primary
            onClick={handleSubmit}
          />
        }
      />

      {/* Display Response */}
      {response && <p>Response from Flask: {response}</p>}

      {/* Display Members */}
      {typeof data.members === 'undefined' ? (
        <p>Loading...</p>
      ) : (
        data.members.map((member, i) => (
          <p key={i} style={{ backgroundColor: 'blue', padding: '10px' }}>
            {member}
          </p>
        ))
      )}
    </div>
  );
}

export default App;
