import { useContext, useEffect, useState } from 'react'
import "../styles/privacy.scss"
import * as Api from "../utils/Api.js"

function PrivacyPage() {



    return (<div className="PrivacyPage">
        <div className="Content">
            <h1>Politique de confidentialité</h1>
            <h2>1. Introduction</h2>
            <p>LEROY Loick respecte votre vie privée et s'engage à protéger les données personnelles que vous partagez avec nous. Cette politique explique quelles données nous collectons, comment nous les utilisons et vos droits en matière de confidentialité.</p>

            <h2>2. Données collectées</h2>
            <p>Nous collectons les données suivantes via Facebook Login, uniquement lorsque vous nous y autorisez :
                <ul>
                    <li>Nom et prénom</li>
                    <li>Adresse e-mail</li>
                    <li>Photo de profil Facebook</li>
                    <li>Liste des pages professionnelles que vous administrez</li>
                    <li>Contenu des publications que vous souhaitez automatiser</li>
                    <li>Nous ne collectons aucune donnée personnelle sans votre consentement explicite.</li>
                </ul>
            </p>
            <h2>3. Utilisation des données</h2>
            <p>Les données que nous collectons sont utilisées dans les objectifs suivants :
                <ul>
                    <li>Vous permettre de vous connecter à votre compte via Facebook Login.</li>
                    <li>Automatiser la publication de contenu sur les pages professionnelles que vous administrez.</li>
                    <li>Vous fournir des analyses et des rapports sur les performances des publications.</li>
                </ul>
                Nous ne vendons ni ne partageons vos données personnelles à des tiers sans votre accord.
            </p>
            <h2>4. Partage des données</h2>
            <p>Vos données personnelles peuvent être partagées uniquement avec les services suivants :
                <ul>
                    <li>Meta Platforms Inc. pour la connexion et l’accès aux pages Facebook.</li>
                </ul>
            </p>
            <h2>5. Sécurité des données</h2>
            <p>Nous prenons des mesures de sécurité appropriées pour protéger vos données contre l'accès non autorisé, la modification, la divulgation ou la destruction. Cependant, aucune méthode de transmission sur Internet ou de stockage électronique n’est 100 % sécurisée.</p>
            <h2>6. Vos droits</h2>
            <p>Vous avez le droit de :
                <ul>
                    <li>Accéder aux données que nous avons collectées à votre sujet.</li>
                    <li>Demander la modification ou la suppression de vos données.</li>
                    <li>Retirer votre consentement à tout moment.</li>
                </ul>
            </p>
            <h2>7. Cookies et technologies similaires</h2>
            <p>Nous pouvons utiliser des cookies pour améliorer votre expérience utilisateur et analyser l’utilisation de notre application. Vous pouvez configurer votre navigateur pour refuser les cookies.</p>
            <h2>8. Modifications de la politique</h2>
            <p>Nous nous réservons le droit de modifier cette politique de confidentialité à tout moment. Les modifications seront publiées sur cette page, et la date de mise à jour sera modifiée en conséquence.</p>
            <h2>9. Contact</h2>
            <p>Pour toute question concernant cette politique, veuillez nous contacter à :
                <ul>
                    <li>LEROY Loick</li>
                    <li>loick.leroy01@gmail.com</li>
                    <li>0477 26 19 90</li>
                </ul>
            </p>
        </div>
    </div>)

}

export default PrivacyPage