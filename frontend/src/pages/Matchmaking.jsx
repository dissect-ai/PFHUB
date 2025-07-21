import React, { useEffect, useState } from 'react';

function Matchmaking() {
  const [matchData, setMatchData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://pfhub-backend.onrender.com/match")
      .then(res => res.json())
      .then(data => {
        setMatchData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch match:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="text-center mt-16">
      <h1 className="text-4xl font-bold mb-6 text-gradient bg-gradient-to-r from-cyan-400 to-blue-500 inline-block">PFHub Matchmaking</h1>
      {loading ? (
        <p className="text-gray-400 text-lg animate-pulse">Looking for your next debate...</p>
      ) : matchData ? (
        <div className="bg-[#111] border border-gray-700 text-green-300 px-6 py-4 rounded-xl shadow-md inline-block">
          <p><strong>Status:</strong> {matchData.status}</p>
          <p><strong>Opponent:</strong> {matchData.opponent}</p>
          <p><strong>ELO Delta:</strong> +{matchData.elo_change}</p>
        </div>
      ) : (
        <p className="text-red-500">Failed to find a match. Try again later.</p>
      )}
    </div>
  );
}

export default Matchmaking;
