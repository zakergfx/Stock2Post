import { useContext, useEffect, useState } from 'react'
import "../styles/login.scss"
import * as Api from "../utils/Api.js"
import FacebookLoginButton from '../components/FacebookLoginButton.js'
import { AuthContext } from '../context/AuthContext.js'
import Alert from '../components/Alert.js'
import { useNavigate } from 'react-router-dom';

function LoginPage() {
    const navigate = useNavigate();

    const { step, loginStep1, loginStep2 } = useContext(AuthContext)
    const [email, setEmail] = useState()
    const [code, setCode] = useState()


    async function handleLoginStep2(){
        const response = await loginStep2(email, code)
        if (response.success){
            navigate("/profil")
        }

    }
 

    return (<div className="LoginPage">
        <div className="Content">
            <h1>Page de connexion</h1>
            {step == 1 ? <>
                <label htmlFor="mail">Adresse mail</label>
                <input key="2" placeholder="abc@example.com" id="mail" value={email} onChange={(e) => setEmail(e.target.value)}></input>
                <button className="Primary" onClick={() => loginStep1(email)}>Recevoir un code par mail</button>

            </> : <>
                <label htmlFor="code">Code</label>
                <input min="0" type="number" key="1" placeholder="------" id="code" value={code} onChange={(e) => setCode(e.target.value)}></input>
                <button className="Primary" onClick={handleLoginStep2}>Se connecter</button>
            </>
            }

        </div>
    </div>)

}

export default LoginPage