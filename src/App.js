import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate, useNavigate } from 'react-router-dom';
import SignInPage from './SignInPage';
import Dashboard from './Dashboard';

function App() {
    const [userProfile, setUserProfile] = useState(null);

    const handleSignIn = (profile) => {
        // Save the user profile data in state
        setUserProfile(profile);
        // Redirect to the dashboard
    };

    return (
        <Router>
            <Routes>
                <Route path="/signin" element={<SignInPage onSignIn={handleSignIn} />} />
                <Route path="/dashboard" element={userProfile ? <Dashboard userProfile={userProfile} /> : <Navigate replace to="/signin" />} />
                <Route path="*" element={<Navigate replace to="/signin" />} />
            </Routes>
        </Router>
    );
}

export default App;
