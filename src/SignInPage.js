import React from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const SignInPage = ({ onSignIn }) => {
    const navigate = useNavigate(); // Hook for navigation
    const login = useGoogleLogin({
        onSuccess: tokenResponse => {
            axios.post('http://localhost:8000/api/google-login', {
                token: tokenResponse.access_token,
            }).then(response => {
                // Assuming the backend sends back the user's profile info and session token
                console.log(response.data)
                onSignIn(response.data); // Save the user profile data
                navigate('/dashboard'); // Redirect to the dashboard
            }).catch(error => console.error('Error:', error));
        },
        onError: error => console.log('Login Failed:', error),
    });

    return (
        <div>
            <h2>Sign In with Google</h2>
            <button onClick={() => login()}>Sign in with Google 🚀</button>
        </div>
    );
};

export default SignInPage;
