import { useContext, useEffect, useState } from 'react'
import "../styles/header.scss"
import { AuthContext } from '../context/AuthContext.js'
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";

function Header() {

    const { user, logoutUser } = useContext(AuthContext)

    const location = useLocation();

    useEffect(() => {
      if (location.hash) {
        const element = document.getElementById(location.hash.substring(1));
        if (element) {
          element.scrollIntoView({ behavior: "smooth" });
        }
      }
    }, [location]);

    return (
    <div className="Header">
        <a href="/#home">Accueil</a>
        <a href="/#features">Fonctionnalités</a>
        <a href="/main">Administration</a>
        <a href="/#contact">Contact</a>
        {user ? <a className="Log"  href="" onClick={logoutUser}>Se déconnecter</a> : <a className="Log" href="/login">Se connecter</a>}
    </div>)

}

export default Header