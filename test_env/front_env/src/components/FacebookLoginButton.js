import React from 'react';
import FacebookLogin from 'react-facebook-login';
import * as Api from "../utils/Api"
import { AuthContext } from '../context/AuthContext.js'
import { useContext } from 'react';
import Alert from '../components/Alert.js'
import { useNavigate } from 'react-router-dom';


function FacebookLoginButton() {
  const navigate = useNavigate();

  const { loginUser, setIsRegisterInProgress, setFbId, setPageToken } = useContext(AuthContext)


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
    response = await fetch(`https://graph.facebook.com/v22.0/oauth/access_token?grant_type=fb_exchange_token&client_id=619463547153543&client_secret=cf4ad9d1e6a0f5b315bbd17d7e407e00&fb_exchange_token=${userToken}`)
    const longUserToken = (await response.json()).access_token

    //récupération long page token
    response = await fetch(`https://graph.facebook.com/v22.0/${userId}/accounts?access_token=${longUserToken}`)
    const data = (await response.json()).data

    console.log(data)

    // vérification que l'user a choisi une seule page
    if (data.length === 1) {
      const longPageToken = data[0].access_token
      setPageToken(longPageToken)
      setFbId(data[0].id)
      const isRegistered = (await Api.fetchPost("/api/isregistered/", { "token": longPageToken })).detail.isRegistered

      if (!isRegistered) {
        setIsRegisterInProgress(true)
      }
      else {
        const success = (await loginUser(longPageToken)).success
        if (success) {
          Alert.success("Connecté !")
          navigate("/main")
        }
        else {
          Alert.error("Erreur lors de la connexion")
        }
      }


    }
    else {
      alert("Veuillez vous reconnecter en sélectionnant UNE PAGE")
    }
  }



  return (
    <div className="FbLogin">
      <FacebookLogin
        appId="619463547153543"  // Remplacez par votre App ID Facebook
        autoLoad={false}
        fields="name,email,picture"
        scope="email,pages_show_list,pages_read_engagement,pages_manage_posts,public_profile"
        callback={responseFacebook}
        icon="fa-facebook"
        textButton="Se connecter avec Facebook"
      />
    </div>
  );
};

export default FacebookLoginButton;
