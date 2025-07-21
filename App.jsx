// PFHub Frontend Entry - Full Feature-Packed Experience UI with Modern Aesthetics

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Matchmaking from './pages/Matchmaking';
import CaseCollector from './pages/CaseCollector';
import DebateRoom from './pages/DebateRoom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import FloatingStars from './components/FloatingStars';
import PageTransition from './components/PageTransition';
import ScrollToTop from './components/ScrollToTop';
import KeyboardShortcuts from './components/KeyboardShortcuts';
import ParticleGlow from './components/ParticleGlow';
import MotionDiv from './components/MotionDiv';

/*
  ⚔️ Mandatory Case Disclosure Enforcement:
  - All users must disclose at least one case before joining matchmaking.
  - Users above 1500 ELO must disclose both Pro and Con.
  - This is checked and enforced in the /matchmaking page and backend queue system.
*/

function App() {
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-black via-[#0d0d0d] to-[#1b1b1b] text-white font-sans antialiased overflow-hidden">
      {/* Ambient FX */}
      <FloatingStars />
      <ParticleGlow />
      <KeyboardShortcuts />

      <Router>
        <ScrollToTop />
        <Navbar />
        <main className="px-4 sm:px-6 md:px-8 py-10 max-w-screen-2xl mx-auto animate-fade-in">
          <Toaster position="top-center" toastOptions={{ style: { background: '#222', color: '#fff', border: '1px solid #333' } }} />
          <PageTransition>
            <Routes>
              <Route path="/" element={<MotionDiv><Home /></MotionDiv>} />
              <Route path="/matchmaking" element={<MotionDiv><Matchmaking /></MotionDiv>} />
              <Route path="/cases" element={<MotionDiv><CaseCollector /></MotionDiv>} />
              <Route path="/debate/:id" element={<MotionDiv><DebateRoom /></MotionDiv>} />
            </Routes>
          </PageTransition>
        </main>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
