import React from 'react';
import FacebookLogin from 'react-facebook-login';
import * as Api from "../utils/Api"
import { AuthContext } from '../context/AuthContext.js'
import { useContext } from 'react';


function FacebookLoginButton() {

  const { loginUser } = useContext(AuthContext)


  function responseFacebook(response) {
    if (response.accessToken) {
      getPageToken(response.accessToken)
    }
  };

  async function getPageToken(userToken){
    const response = await fetch("https://graph.facebook.com/v22.0/530119660189423?access_token="+userToken+"&fields=access_token")
    const data = await response.json()
    loginUser(data.access_token)
  }

  

  return (
    <div>
      <h2>Connexion avec Facebook</h2>
      <FacebookLogin
        appId="619463547153543"  // Remplacez par votre App ID Facebook
        autoLoad={false}
        fields="name,email,picture"
        scope="read_insights,pages_show_list,pages_read_engagement,pages_manage_posts"
        callback={responseFacebook}
        icon="fa-facebook"
        textButton="Se connecter avec Facebook"
      />
    </div>
  );
};

export default FacebookLoginButton;
