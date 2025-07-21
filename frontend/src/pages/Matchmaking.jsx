import React, { useEffect, useState } from 'react';
import { Loader2 } from 'lucide-react';
import "@fontsource/inter";

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
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-white px-4 font-sans">
      <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-300 to-green-400 mb-8 drop-shadow-lg">
        🎯 PFHub Matchmaking
      </h1>

      {loading ? (
        <div className="flex flex-col items-center gap-3 text-gray-400 animate-pulse">
          <Loader2 className="animate-spin w-10 h-10" />
          <p className="text-lg">Searching for your next debate...</p>
        </div>
      ) : matchData ? (
        <div className="bg-gradient-to-br from-[#121212] to-[#1a1a1a] border border-[#333] rounded-xl shadow-2xl px-8 py-6 w-full max-w-md transition hover:scale-105 duration-300">
          <p className="text-2xl mb-2"><span className="font-semibold text-eloGreen">✅ Status:</span> {matchData.status}</p>
          <p className="text-lg"><span className="font-semibold text-white">🧠 Opponent:</span> {matchData.opponent}</p>
          <p className="text-lg"><span className="font-semibold text-pfgold">📈 ELO Delta:</span> +{matchData.elo_change}</p>
        </div>
      ) : (
        <p className="text-red-500">❌ Could not fetch match. Please try again.</p>
      )}
    </div>
  );
}

export default Matchmaking;
