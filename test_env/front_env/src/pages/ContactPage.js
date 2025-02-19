import { useContext, useEffect, useState } from 'react'
import "../styles/contact.scss"
import * as Api from "../utils/Api.js"

function ContactPage() {



    return (<div className="ContactPage">
        <div className="Content">
            <h1>Informations de contact</h1>
            <h2>Pour signaler un problème, poser une question, proposer une suggestion ou autre, voici comment nous contacter.</h2>
            <span><b>Personne de contact: </b>LEROY Loick</span>
            <span><b>Mail: </b>REMOVED_EMAIL</span>
            <span><b>Téléphone: </b>0477 26 19 90</span>
        </div>

    </div>)

}

export default ContactPage