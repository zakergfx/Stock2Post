import { useContext, useEffect, useState } from 'react'
import "../styles/header.scss"
import * as Api from "../utils/Api.js"
import { AuthContext } from '../context/AuthContext.js'

function Header() {

    const { user, logoutUser } = useContext(AuthContext)



    return (<div className="Header">
        <a href="/">Accueil</a>
        <a href="/main">Administration</a>
        <a href="/contact">Contact</a>
        {user ? <a href="" onClick={logoutUser}>Se déconnecter</a> : <a href="/login">Se connecter</a>}



    </div>)

}

export default Header