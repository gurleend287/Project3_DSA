<H1> Project 3: Mood to Music </h1>

# Project Description

## Overview

Our team, **DSA Dingos**, embarked on a mission to address the challenge faced by many music enthusiasts: the difficulty of finding a playlist that aligns with their current mood. 
A common issue many music listeners have is finding a playlist curated solely based on their current mood and no other factors. While users can create their own ‘sadness symphony’ or ‘cheerful chords’ playlist over time, there’s not really a unique playlist algorithmically generated based on mood alone. Using musical factors correlating to different moods, we are able to match mood to music. Many music streaming platforms implement complex algorithms built upon past listening behavior, connections between artists, and even more factors. With so many factors, it may be hard to find a playlist that fits your current mood instead of overall listening history. We were inspired by a lacking feature in Spotify. For example, Spotify’s ‘Daily Mixes’ features songs selected based on all of those complex factors. After listening to a lot of upbeat and happier music for a week, Spotify would only recommend positive and upbeat songs. However, when the mood shifted after a bad exam, none of the Spotify generated mixes matched my mood. It took a couple of days for the recommended playlists to adjust to my mood. Thus, the need for Mood to Music was born. Our interface is quite straightforward and simple. We give a qualitative description to each mood level. First, the user enters their current mood on a scale of 1 to 5 (where 1 is more depressed and 5 is happier) on a sliding scale. Then, they enter their desired playlist size into a text box, and lastly select a BFS algorithm or DFS algorithm. The graph based on our multi-level criteria (explained below) is then created after parsing through the dataset to find matches to that mood level. A new CSV file is created with the unique playlist generated by BFS/DFS which is read into the React app. It is displayed in a numbered list of each song, its artists, and other distinguishing features.



## Contributors 
Team Members + Github user names: 

- Gayatri Baskaran - bgayatri3
- Gurleen Dhillon - gurleen287
- Shravya Sama - shrav-bot

## Running the Project Locally 

Some intial installs:

- [Node.js](https://nodejs.org/en/)
- [VS Code](https://code.visualstudio.com/) (recommended text editor)
- [Python](https://www.python.org/)

### Command-Line Installs

### Frontend

- npm install
- npm install react react-dom
- npm install semantic-ui-react semantic-ui-css

### Backend

- pip3 install python-dotenv
- pip3 install pandas
- pip3 install scikit-learn
- pip3 install flask

## Usage 

In a text editor like VSCode, clone the repository from GitHub. 
Make sure everything is installed and you are in the project directory.
Create two terminals:
- In one terminal:
  1. cd flask_server
  2. python server.py
  This runs the frontend server, you should not have any local host automatically open at this point. 
- In the other terminal:
  1. cd to the project directory (different, depends where you have saved it)
  2. cd client
  3. npm start (make sure you have ran npm install)

