import React from 'react';
// import FacebookLogin from 'react-facebook-login';
import * as Api from "../utils/Api"
import { AuthContext } from '../context/AuthContext.js'
import { useContext } from 'react';
import Alert from '../components/Alert.js'
import { useNavigate } from 'react-router-dom';
import FacebookLogin from 'react-facebook-login/dist/facebook-login-render-props'
import "../styles/login.scss"

function FacebookLoginButton() {
  const navigate = useNavigate();

  const { setFbId, setPageToken, fbLogin } = useContext(AuthContext)


  function responseFacebook(response) {
    if (response.accessToken) {
      login(response.accessToken)
    }
  };

  async function login(userToken) {
    // récupération user id
    let response = await fetch(`https://graph.facebook.com/v22.0/me?access_token=${userToken}&fields=id,name`)


    const userId = (await response.json()).id


    // récupération long user token
    response = await fetch(`https://graph.facebook.com/v22.0/oauth/access_token?grant_type=fb_exchange_token&client_id=XXX&client_secret=XXX&fb_exchange_token=${userToken}`)
    const longUserToken = (await response.json()).access_token

    //récupération long page token
    response = await fetch(`https://graph.facebook.com/v22.0/${userId}/accounts?access_token=${longUserToken}`)
    const data = (await response.json()).data


    // vérification que l'user a choisi une seule page
    if (data.length === 1) {
      const longPageToken = data[0].access_token
      setPageToken(longPageToken)
      const response = await fbLogin(longPageToken)
      setFbId(data[0].id)



    }
    else {
      alert("Veuillez vous reconnecter en sélectionnant UNE PAGE")
    }
  }



  return (
    <div className="FbLogin">
      <FacebookLogin
        appId="REMOVED_FACEBOOK_APP_ID"  // Remplacez par votre App ID Facebook
        autoLoad={false}
        fields="name,email,picture"
        scope="email,pages_show_list,pages_read_engagement,pages_manage_posts,public_profile"
        callback={responseFacebook}
        render={renderProps => (
          <button className="FbButton" onClick={renderProps.onClick}>LIER VOTRE PAGE FACEBOOK</button>
        )}
        // icon="fa-facebook"
        // textButton="Lier votre page Facebook"
      />
    </div>
  );
};

export default FacebookLoginButton;
