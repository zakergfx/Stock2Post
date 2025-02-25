import { useContext, useEffect, useState } from 'react'
import "../styles/login.scss"
import * as Api from "../utils/Api.js"
import FacebookLoginButton from '../components/FacebookLoginButton.js'
import { AuthContext } from '../context/AuthContext.js'
import Alert from '../components/Alert.js'
import { useNavigate } from 'react-router-dom';

function LoginPage() {
    const navigate = useNavigate();

    const { loginUser, isRegisterInProgress, setIsRegisterInProgress, pageToken, fbId } = useContext(AuthContext)
    const [dealers, setDealers] = useState([])
    const [selectedDealer, setSelectedDealer] = useState("")

    async function handleSyncButtonClick() {
        if (selectedDealer != "") {
            const data = { "dealer": selectedDealer, "fbId": fbId, "pageToken": pageToken }
            const response = await Api.fetchPost("/api/register/", data, false)
            setIsRegisterInProgress(false)

            // login
            const success = (await loginUser(pageToken)).success
            if (success) {
                Alert.success("Connecté !")
                navigate("/main")
            }
            else {
                Alert.error("Erreur lors de la connexion")
            }
            navigate("/main")


        }
        else {
            alert("Veuillez sélectionner une page autoscout")
        }

    }

    useEffect(() => {
        if (isRegisterInProgress) {
            getFreeDealers()
        }

        async function getFreeDealers() {
            const response = await Api.fetchGet("/api/dealers", false)
            console.log(response)
            setDealers(response.detail)
        }


    }, [isRegisterInProgress])

    return (<div className="LoginPage">
        <div className="Content">
            <h1>Connexion</h1>
            <h2>Etapes</h2>
            <ul>
                <li>Connectez-vous avec Facebook</li>
                <li>Sélectionnez la page que vous souhaitez lier à l'outil</li>
                <li>Sélectionnez le stock autoscout que vous voulez synchroniser avec votre page</li>
            </ul>
            <FacebookLoginButton />
            <p>Une fois connecté vous serez redirigé vers la page d'administration vous permettant de gérer vos posts Facebook.</p>
            {isRegisterInProgress && dealers ?
                <div className="RegisterProgress">
                    Choisissez une page à sync :
                    <select value={selectedDealer} onChange={(e) => setSelectedDealer(e.target.value)}>
                        <option value="">-- Sélectionnez --</option>
                        {dealers.map((value, index) => <option key={index}>{value.name}</option>)}
                    </select>
                    <button onClick={handleSyncButtonClick}>Confirmer</button>
                </div>
                : null
            }
        </div>
    </div>)

}

export default LoginPage