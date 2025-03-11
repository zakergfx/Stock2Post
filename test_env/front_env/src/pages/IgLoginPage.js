import { useContext, useEffect, useState } from 'react'
import * as Api from "../utils/Api.js"
import "../styles/iglogin.scss"
import { AuthContext } from '../context/AuthContext.js'
import Alert from '../components/Alert.js'
import { useNavigate } from 'react-router-dom';
import { useSearchParams } from "react-router-dom";

function IgLoginPage() {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const code = searchParams.get("code");

    useEffect(() => {

        async function sendCodeToBack(){
            const response = await Api.fetchGet("/api/instagramlink?code="+code)

            if (response.success){
                Alert.success("Page Instagram liée !")
                navigate("/profil")
            }
        }

        sendCodeToBack()
    }, [])

    return (<div className="IgLoginPage">
        <div className="Content">
        <h2>Redirection en cours...</h2>

        </div>
    </div >)

}

export default IgLoginPage