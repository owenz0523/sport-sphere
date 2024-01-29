import React from "react";
import GoogleLogin from "react-google-login";

const responseGoogle = (response) => {
    console.log(response);
}

const GoogleSignInButton = () => {
    return (
        <GoogleLogin
            clientId="418085492874-ko7ds0pjnuf90fr6ujl8vpbp3g4rbu4u.apps.googleusercontent.com"
            buttonText="Sign in with Google"
            onSuccess={responseGoogle}
            onFailure={responseGoogle}
            cookiePolicy={"single_host_origin"}
        />
    )
}
export default GoogleSignInButton;