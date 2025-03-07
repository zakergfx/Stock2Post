import { createContext, useState, useEffect } from 'react'
import { jwtDecode } from "jwt-decode";
import * as Var from "../utils/Var"
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext()

export function AuthProvider({ children }) {

    const navigate = useNavigate();

    const [access, setAccess] = useState(() => localStorage.getItem("access") ? localStorage.getItem("access") : null)
    const [refresh, setRefresh] = useState(() => localStorage.getItem("refresh") ? localStorage.getItem("refresh") : null)
    const [user, setUser] = useState(() => localStorage.getItem("access") ? jwtDecode(localStorage.getItem("access")) : null)
    const [loading, setLoading] = useState(true)

    const [isRegisterInProgress, setIsRegisterInProgress] = useState(false)
    const [pageToken, setPageToken] = useState()
    const [fbId, setFbId] = useState()


    async function loginUser(token) {
        let response = await fetch(Var.backendUrl + "/api/login/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'token': token})
        })
        let data = await response.json()

        if (response.ok) {
            setAccess(data.access)
            setRefresh(data.refresh)
            setUser(jwtDecode(data.access))

            localStorage.setItem("access", data.access)
            localStorage.setItem("refresh", data.refresh)

            return ({ "success": response.ok, "detail": "Connexion réussie" })

        }
        else {
            return ({ "success": response.ok, "detail": data.detail })
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


            try{
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
            catch{
                logoutUser()
            }
           
        }


        if (loading) {
            setLoading(false)
        }

    }

    let contextData = {
        user: user,
        loginUser: loginUser,
        logoutUser: logoutUser,
        isRegisterInProgress: isRegisterInProgress,
        setIsRegisterInProgress: setIsRegisterInProgress,
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
