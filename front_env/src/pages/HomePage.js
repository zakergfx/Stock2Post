import { useContext, useEffect, useState } from 'react'
import "../styles/home.scss"
import * as Api from "../utils/Api.js"

function HomePage() {

    return (<div className="HomePage">
        <div className="Content">
            <div className="Title">
                <img src="https://i.ibb.co/TDqkqNpy/favic.png"></img>
                <h1>Gagnez du temps via la de gestion automatisée de vos réseaux sociaux.</h1>
            </div>
            <h2>AutoShare synchronise votre page Facebook avec votre stock Autoscout, sans que vous n'ayez rien à faire.</h2>
            <h2>Pourquoi choisir AutoShare ?</h2>
            <p><h3>Les avantages sont nombreux :</h3>
                <ul>
                    <li>Si vous avez pour habitude de gérer vos publications manuellement, celà peut consommer beaucoup de temps et d'énergie que vous pourriez investir dans votre activité. <ul>
                        <li>Recréer un post avec la fiche technique complète</li>
                        <li>Publier les dizaines de photos</li>
                        <li>Revenir sur la publication quand un véhicule a été vendu</li>
                        <li>Créer un poste lorsqu'un véhicule est en promo</li>
                    </ul>
                        Toutes ces actions à réaliser au quotidien sont très chronophages et répétitives.</li>
                    <br />
                    <li>Si vous ne profitez pas encore de la visibilité offerte par les réseaux sociaux car vous pensez que celà demande du temps à gérer, c'est l'occasion de sy mettre puisque tout sera géré automatiquement.</li>
                </ul>
            </p>
            <h2>Quels type de post AutoShare peut-il publier ?</h2>
            <p>Notre outils permet de créer des publications dans les cas suivants :
                <ul>
                    <li>Nouvelle annonce publiée sur Autoscout</li>
                    <li>Un véhicule a été vendu</li>
                    <li>Réduction du prix d'un véhicule</li>
                    <li>Véhicule présent depuis longtemps dans le catalogue mais toujours disponible</li>
                    <li>Un post récapitulatif du stock est aussi réalisé de manière régulière.</li>




                </ul>
            </p>
            <div className="Examples">
                <div className="Example">
                    <h3>Publication des nouvelles annonces</h3>
                    <img src="https://i.ibb.co/r2HJB3p3/Capture-d-cran-2025-02-17-194557.png"></img>
                </div>
                <div className="Example">
                    <h3>Publication lorsqu'une vente est effectuée</h3>
                    <img src="https://i.ibb.co/21Pd8cvv/Capture-d-cran-2025-02-17-202602.png"></img>
                </div>
                <div className="Example">
                    <h3>Publication lorsqu'un véhicule est en promo</h3>
                    <img src="https://i.ibb.co/DHWjbq2x/Capture-d-cran-2025-02-17-195144.png"></img>
                </div>
                <div className="Example">
                    <h3>Publication de rappel lorsqu'un véhicule est présent depuis longtemps dans le catalogue</h3>
                    <img src="https://i.ibb.co/bjqzq1qS/Capture-d-cran-2025-02-17-195803.png"></img>
                </div>
                <div className="Example">
                    <h3>Publication rappelant l'ensemble du stock disponible à interval régulier.</h3>
                    <img src="https://i.ibb.co/7tJ7ZnKG/Capture-d-cran-2025-02-17-195942.png"></img>
                </div>
            </div>
        </div>
    </div>)

}

export default HomePage