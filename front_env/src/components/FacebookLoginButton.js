import React from 'react';
import FacebookLogin from 'react-facebook-login';

function FacebookLoginButton() {
  function responseFacebook(response) {
    console.log('Facebook login response:', response);
    if (response.accessToken) {
      // L'utilisateur est connecté, vous pouvez utiliser response.name, response.email, etc.
      alert(`Bienvenue ${response.name}!`);
    }
  };

  return (
    <div>
      <h2>Connexion avec Facebook</h2>
      <FacebookLogin
        appId="REMOVED_FACEBOOK_APP_ID"  // Remplacez par votre App ID Facebook
        autoLoad={false}
        fields="name,email,picture"
        callback={responseFacebook}
        icon="fa-facebook"
        textButton="Se connecter avec Facebook"
      />
    </div>
  );
};

export default FacebookLoginButton;
