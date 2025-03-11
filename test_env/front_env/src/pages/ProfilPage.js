import { useContext, useEffect, useState } from 'react'
import "../styles/profil.scss"
import * as Api from "../utils/Api.js"
import FacebookLoginButton from '../components/FacebookLoginButton.js'
import { AuthContext } from '../context/AuthContext.js'
import Alert from '../components/Alert.js'
import { useNavigate } from 'react-router-dom';

function ProfilPage() {
    const navigate = useNavigate();
    const [me, setMe] = useState()

    const { fbId } = useContext(AuthContext)

    useEffect(() => {

        async function me() {
            const response = await Api.fetchGet("/api/me")
            setMe(response.detail)
        }

        me()

    }, [fbId])


    if (me)
        return (<div className="ProfilPage">
            <div className="Content">

                <h1>Liaisons à vos réseaux sociaux</h1>

                <h2>Lier votre page Facebook</h2>
                {!me.fbPageName ? <>
                    <span>1. Connectez-vous avec Facebook</span>
                    <span>2. Sélectionnez votre page</span>
                    <span>3. C'est tout !</span></>
                    : <>
                        <span>Vous êtes connecté en tant que <b>{me.fbPageName}</b></span>
                        <span>Vous voulez changer de compte ? cliquez sur le bouton ci-dessous</span>
                    </>
                }
                <FacebookLoginButton />

                <h2>Lier votre page Instagram</h2>

                {!me.igPageName ? <>
                    <span>1. Connectez-vous avec votre compte Instagram</span>
                    <span>2. C'est tout !</span>
                </>
                    :
                    <>
                        <span>Vous êtes connecté en tant que <b>{me.igPageName}</b></span>
                        <span>Vous voulez changer de compte ? cliquez sur le bouton ci-dessous</span>
                    </>
                }
                {/* <button className="IgButton" onClick={() => window.location.replace(`https://www.instagram.com/oauth/authorize?enable_fb_login=0&force_authentication=1&client_id=REMOVED_INSTAGRAM_CLIENT_ID&redirect_uri=https://${process.env.REACT_APP_SERVERNAME}/iglogin&response_type=code&scope=instagram_business_basic%2Cinstagram_business_manage_messages%2Cinstagram_business_manage_comments%2Cinstagram_business_content_publish%2Cinstagram_business_manage_insights`)} >LIER VOTRE PAGE INSTAGRAM</button> */}
                <button className="IgButton" onClick={() => window.location.replace(`https://www.instagram.com/oauth/authorize?enable_fb_login=0&force_authentication=1&client_id=REMOVED_INSTAGRAM_CLIENT_ID&redirect_uri=https://${process.env.REACT_APP_SERVERNAME}/iglogin&response_type=code&scope=instagram_business_basic%2Cinstagram_business_content_publish`)} >LIER VOTRE PAGE INSTAGRAM</button>

            </div>
        </div >)

}

export default ProfilPage