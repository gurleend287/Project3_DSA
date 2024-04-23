import React, { useState, useEffect } from 'react';
import { Button, Rating, Form, Radio, List } from 'semantic-ui-react';
import './App.css';
import { Card } from 'semantic-ui-react';
import { Image } from 'semantic-ui-react';

function App() {
  const [data, setData] = useState({});
  const [rating, setRating] = useState(0);
  const [textInput, setTextInput] = useState('');
  const [radioOption, setRadioOption] = useState('option1');
  const [response, setResponse] = useState('');
  const [csvData, setCsvData] = useState([]);
  const [averageDifference, setAverageDifference] = useState(0);


  const handleSubmit = async () => {
    try {
      const response = await fetch('/send_rating', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          rating: rating,
          textInput: textInput,
          radioOption: radioOption
        })
      });

      const responseData = await response.json();
      setResponse(responseData.response);
      setAverageDifference(responseData.average_difference); // Add this line to set the average difference

    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleFetchCsvData = async () => {
    try {
      const csvResponse = await fetch(`/get_csv_data`);
      const csvData = await csvResponse.json();
      setCsvData(csvData);

    } catch (error) {
      console.error('Error fetching CSV data:', error);
    }
  };


  const handleGetPlaylist = async () => {
    try {
      await handleSubmit(); // wait for handleSubmit to finish
      await handleFetchCsvData(); // fetch after handleSubmit finishes
    } catch (error) {
      console.error('Error fetching playlist data:', error);
    }
  };


  return (
    <div className="App">
      {/* Website Header */}
      <header className="App-header">
        <h1> 😭 Mood to Music 😁  </h1>
      </header>

      {/* Rating Component */}
      <div>
        {/* Rating Descriptions */}
        <div className="rating-descriptions">
          <p>
            Moods: <br />
            1 - Super Sad<br />
            2 - Sad<br />
            3 - Neutral<br />
            4 - Happy<br />
            5 - Super Happy
          </p>
        </div>
        <label>Rate your mood: {rating}</label>
        <input
          type='range'
          min={1}
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
      <p> </p>
      {/* Text Input */}
      <Form.Input
        label='Enter Playlist Size (1-100)'
        placeholder='Enter text'
        value={textInput}
        onChange={(e) => setTextInput(e.target.value)}
      />
      <p> </p>
      {/* Radio Button Options */}
      <Form.Group inline>
        <label>Select a search algorithm (Breath-First Search or Depth-First Search):</label>
        <Form.Field
          control={Radio}
          label='BFS'
          value='option1'
          checked={radioOption === 'option1'}
          onChange={() => setRadioOption('option1')}
        />
        <Form.Field
          control={Radio}
          label='DFS'
          value='option2'
          checked={radioOption === 'option2'}
          onChange={() => setRadioOption('option2')}
        />
      </Form.Group>

      {/* Fetch CSV Data Button */}
      <Button
        content="Get my Playlist"
        color="teal"
        onClick={handleGetPlaylist}
        style={{ marginTop: '20px' }}  // Add some margin at the top
      />

      {/* Display Response */}
      {response && <p>Playlist below!</p>}

      {/* Display Members */}
      {typeof data.members === 'undefined' ? (
        <p></p>
      ) : (
        <div>
          <h3>Members:</h3>
          {data.members.map((member, i) => (
            <p key={i} style={{ backgroundColor: 'white', padding: '10px' }}>
              {member}
            </p>
          ))}
        </div>
      )}
    
    {/* Display Average Difference */}
    {averageDifference !== 0 && <p>Average Difference: {averageDifference.toFixed(2)}</p>}

    {/* Display Cards  */}
    <div className="card-container">
    {csvData.slice(1, textInput + 1).map((row, index) => (
        <div className="card" key={index}>
        <img src={row[0]} alt="Track cover" className="image" />
        <Card.Description className="card-description">
            Track: {row[1]} <br />
            Artist: {row[2]} <br />
        </Card.Description>
        </div>
    ))}
    </div>

    </div >
  );
}

export default App;
