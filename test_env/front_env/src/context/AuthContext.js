import { createContext, useState, useEffect } from 'react'
import { jwtDecode } from "jwt-decode";
import * as Var from "../utils/Var"
import * as Api from "../utils/Api"
import { useNavigate } from 'react-router-dom';
import Alert from '../components/Alert';

export const AuthContext = createContext()

export function AuthProvider({ children }) {

    const navigate = useNavigate();
    const [step, setStep] = useState(1)
    const [access, setAccess] = useState(() => localStorage.getItem("access") ? localStorage.getItem("access") : null)
    const [refresh, setRefresh] = useState(() => localStorage.getItem("refresh") ? localStorage.getItem("refresh") : null)
    const [user, setUser] = useState(() => localStorage.getItem("access") ? jwtDecode(localStorage.getItem("access")) : null)
    const [loading, setLoading] = useState(true)

    const [pageToken, setPageToken] = useState()
    const [fbId, setFbId] = useState()

    async function fbLogin(pageToken){
        const body = {"pageToken": pageToken}
        const response = await Api.fetchPost("/api/facebooklink/", body)

        if (response.success){
            Alert.success("Page Facebook liée !")
        }
        else{
            Alert.error("Impossible de lier la page Facebook")
        }
    }

    async function loginStep1(email) {
        if (email) {
            const body = { "step": 1, "email": email }
            const response = await Api.fetchPost("/api/login/", body, false)

            if (response.success) {
                Alert.success("Vous avez reçu un code par mail")
                setStep(2)
            }
            else {
                Alert.error("Votre adresse mail est incorrect")
            }
        }
        else {
            Alert.error("Veuillez entrer une adresse mail")
        }

    }

    async function loginStep2(email, code) {
        if (code) {
            const body = { "step": 2, "email": email, "code": code }
            const response = await Api.fetchPost("/api/login/", body, false)

            if (response.success) {
                const data = response.detail
                setAccess(data.access)
                setRefresh(data.refresh)
                setUser(jwtDecode(data.access))

                localStorage.setItem("access", data.access)
                localStorage.setItem("refresh", data.refresh)

                Alert.success("Connecté !")
                return { "success": true }

            }
            else {
                Alert.error("Erreur lors de la connexion")
                return { "success": false }

            }
        }
        else {
            Alert.error("Veuillez entrer le code")
            return { "success": false }
        }

    }

    function logoutUser() {
        console.log("logout")
        setAccess(null)
        setRefresh(null)
        setUser(null)
        localStorage.removeItem("access")
        localStorage.removeItem("refresh")
        navigate("/login")

    }

    async function updateToken() {
        if (localStorage.getItem("access")) {
            let response = await fetch(Var.backendUrl + "/api/token/refresh/", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'refresh': refresh })
            })


            try {
                let data = await response.json()

                if (response.status === 200) {
                    setAccess(data.access)

                    setUser(jwtDecode(data.access))
                    localStorage.setItem("access", data.access)
                }
                else {

                    logoutUser()
                }
            }
            catch {
                logoutUser()
            }

        }


        if (loading) {
            setLoading(false)
        }

    }

    let contextData = {
        user: user,
        loginStep1: loginStep1,
        loginStep2: loginStep2,
        fbLogin: fbLogin,
        step: step,
        logoutUser: logoutUser,
        pageToken: pageToken,
        setPageToken: setPageToken,
        fbId: fbId,
        setFbId: setFbId
    }


    useEffect(() => {

        if (loading) {
            updateToken()
        }

        let interval = setInterval(() => {
            if (access) {
                updateToken()
            }

        }, 240000)

        return () => clearInterval(interval)
    }, [access, refresh, loading])

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
    )
}
