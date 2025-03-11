import { useContext, useEffect, useState } from 'react'
import "../styles/header.scss"
import { AuthContext } from '../context/AuthContext.js'
import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";
import { MainContext } from '../context/MainContext.js'
import * as Var from "../utils/Var.js"

function Header() {
  const { isMobile, isHeaderDisplayed, setIsHeaderDisplayed } = useContext(MainContext)

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

  if (!isMobile)
    return (
      <div className="Header">
        <a href="/#home"><b>Stock<span className="Colored">2Post</span></b></a>
        <a href="/#features">Fonctionnalités</a>
        <a href="/main">Administration</a>
        <a href="/profil">Profil</a>
        <a href="/#contact">Contact</a>
        {user ? <a className="Log" href="" onClick={logoutUser}>Se déconnecter</a> : <a className="Log" href="/login">Se connecter</a>}
      </div>)

  else return (
    <div className="Header">
      <div className="ButtonDiv">
        <img src={Var.backendUrl+"/api/media/hamburger.png"} onClick={() => setIsHeaderDisplayed(!isHeaderDisplayed)}></img>
      </div>
      <div className={"Content " + (isHeaderDisplayed ? "Shown" : "Hidden")}>
        <a href="/#home" onClick={() => setIsHeaderDisplayed(false)}><b>Stock<span className="Colored">2Post</span></b></a>
        <a href="/#features" onClick={() => setIsHeaderDisplayed(false)}>Fonctionnalités</a>
        <a href="/main" onClick={() => setIsHeaderDisplayed(false)}>Administration</a>
        <a href="/profil" onClick={() => setIsHeaderDisplayed(false)}>Profil</a>
        <a href="/#contact" onClick={() => setIsHeaderDisplayed(false)}>Contact</a>
        {user ? <a className="Log" href="" onClick={logoutUser}>Se déconnecter</a> : <a className="Log" href="/login">Se connecter</a>}
      </div>
    </div>)


}

export default Header