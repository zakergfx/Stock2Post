import { useContext, useEffect, useState } from 'react'
import "../styles/footer.scss"
import { MainContext } from '../context/MainContext.js'

function Footer() {
    const { isMobile } = useContext(MainContext)

    if (!isMobile)
        return (<div className="Footer">
            <div className="BlankAndFooter">
                <div className="Blank"></div>
                <div className="OnlyFooter">
                    <div className="Column">
                        <b>@2025 LEROY Loick - Tous droits réservés</b>
                        <span>Numéro d'entreprise: BE1018983911 </span>
                        <span>Numéro TVA: BE1018983911</span>
                    </div>
                    <div className="Column">
                        <b>Contact</b>
                        <span>Adresse: Rue d'Estinia 9, 5590 Sovet</span>
                        <span>GSM: 0477 26 19 90</span>
                        <span>Mail: loick.leroy01@gmail.com</span>
                    </div>
                    <div className="Column">
                        <b>Navigation</b>
                        <a href="/">Accueil</a>
                        <a href="/main">Administration</a>
                        <a href="/contact">Contact</a>
                        <a href="/login">Se connecter</a>

                        <a href="/privacy">Politique de confidentialité</a>
                        <a href="/tos">Conditions générales d'utilisation</a>
                    </div>
                </div>
            </div>

        </div>)
    else return (
        <div className="Footer">
            <div className="BlankAndFooter">
                <div className="Blank"></div>
                <div className="OnlyFooter">
                    <div className="Column">
                        <b>@2025 LEROY Loick - Tous droits réservés</b>
                        <span>Numéro d'entreprise: BE1018983911 </span>
                        <span>Numéro TVA: BE1018983911</span>
                        <br/><b>Contact</b>
                        <span>Adresse: Rue d'Estinia 9, 5590 Sovet</span>
                        <span>GSM: 0477 26 19 90</span>
                        <span>Mail: loick.leroy01@gmail.com</span>
                    </div>

                    <div className="Column">
                        <b>Navigation</b>
                        <a href="/">Accueil</a>
                        <a href="/main">Administration</a>
                        <a href="/contact">Contact</a>
                        <a href="/login">Se connecter</a>

                        <a href="/privacy">Politique de confidentialité</a>
                        <a href="/tos">Conditions générales d'utilisation</a>
                    </div>
                </div>
            </div>

        </div>
    )

}

export default Footer