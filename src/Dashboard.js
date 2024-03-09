// Dashboard.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard(userProfile) {
    const [games, setGames] = useState([]);
    const [followed, setFollow] = useState(false);

    const toggleFollow = () => {
        setFollow(current => !current);
      };

    useEffect(() => {
        axios.get('http://localhost:8000/api/get-nhl',
        {
            params:{
                followed: followed,
                user_id: userProfile.userProfile.user_id,
            },
            headers: {
                "Authorization": `Bearer ${userProfile.userProfile.token}`, // Bearer scheme
                "Content-Type": "application/json"
              }

        })
            .then(response => {
                if (JSON.stringify(response.data) !== '{}'){
                    setGames(response.data);
                }else{
                    setGames([]);
                }
            
            })
            .catch(error => console.error('Error fetching data:', error));
    }, [followed]);

    const updateTeam = async (teamName) => {
        const url = 'http://localhost:8000/api/add-fav'; // Your API endpoint
        const sessionToken = userProfile.userProfile.token; // The session token you have
        console.log(userProfile.userProfile.token);

        try {
          const response = await axios.put(url, {
            name: teamName, // Assuming your backend expects the team name in the body
          }, {
            headers: {
              'Authorization': `Bearer ${sessionToken}`, // Include the session token in the Authorization header
            }
          });
          
          console.log('Update successful', response.data);
        } catch (error) {
          console.error('Error updating team', error);
        }
      };
      

    return (
        <div>
            <h1>Game Dashboard</h1>
            {games.map((game) => {
                //console.log(game.status)
                return(
                    <div key={game?.id}>
                        <div>
                            <p>You are {followed ? 'currently' : 'not'} following.</p>
                            <button onClick={toggleFollow}>
                                {followed ? 'Unfollow' : 'Follow'}
                            </button>
                        </div>
                        <h2>{game?.name}</h2>
                        <p>Game Clock: Period {game.status['period']}: {game.status['displayClock']}</p>
                        <p>Home Team: {game?.home_team} -- Score: {game?.home_score}</p>
                        <p>Record {game?.ht_record}</p>
                        <p>Away Team: {game?.away_team} -- Score: {game?.away_score}</p>
                        <p>Record {game?.at_record}</p>
                        {/* Add more game details as needed */}
                    </div>
                )
            })}
        </div>
    );
}

export default Dashboard;
