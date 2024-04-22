import React, { useState, useEffect } from 'react';
import { Button, Rating } from 'semantic-ui-react';
import './App.css';

function App() {
  const [data, setData] = useState({});
  const [rating, setRating] = useState(0);
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
        const response = await fetch('/send_rating', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ rating: rating })
        });

      const responseData = await response.json();
      setResponse(responseData.response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      {/* Rating Component */}
      <div>
        <label>Rating: {rating}</label>
        <input
          type='range'
          min={0}
          max={5}
          value={rating}
          onChange={(e) => setRating(parseInt(e.target.value, 10))}
        />
        <Rating 
          icon='star' 
          maxRating={5} 
          rating={rating} 
          onRate={(e, { rating }) => setRating(rating)} 
        />
      </div>

      {/* Submit Rating Button */}
      <Button 
        content="Submit Rating" 
        primary 
        onClick={handleSubmit} 
      />

      {/* Display Response */}
      {response && <p>Response from Flask: {response}</p>}

      {/* Display Members */}
      {typeof data.members === 'undefined' ? (
        <p>Loading...</p>
      ) : (
        <div>
          <h3>Members:</h3>
          {data.members.map((member, i) => (
            <p key={i} style={{ backgroundColor: 'blue', padding: '10px' }}>
              {member}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
