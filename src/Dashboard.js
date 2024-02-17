// Dashboard.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard(filter) {
    const [games, setGames] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/get-nhl',
        {
            params:{
                followed: "True",
            }

        })
            .then(response => {
                //console.log(response.data);
                setGames(response.data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div>
            <h1>Game Dashboard</h1>
            {games.map((game) => {
                //console.log(game.status)
                return(
                    <div key={game?.id}>
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
