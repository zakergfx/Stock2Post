import { useContext, useEffect, useState } from 'react'
import "../styles/example.scss"
import * as Api from "../utils/Api.js"
import * as Var from "../utils/Var.js"
import { MainContext } from '../context/MainContext.js'


function ExamplePage() {

    const { isMobile } = useContext(MainContext)


    if (!isMobile)
        return (<div className="ExamplePage">
            <div className="Content">
                <div className="Title">
                    <h1>Exemples pour chacun des posts</h1>
                    <p>Cette section montre un post example pour chacune des fonctionnalité de l’application.</p>
                </div>
                <div className="Examples">
                    <img src={Var.backendUrl + "/api/media/newcar.png"}></img>
                    <h1>Nouvelle voiture dans le catalogue</h1>
                    <h1>Nouvelle voiture dans le catalogue (Story)</h1>
                    <img src={Var.backendUrl + "/api/media/story.gif"}></img>
                    <img src={Var.backendUrl + "/api/media/soldcar.png"}></img>
                    <h1>Un véhicule a été vendu</h1>
                    <h1>Un véhicule a été mis en promotion</h1>
                    <img src={Var.backendUrl + "/api/media/promo.png"}></img>
                    <img src={Var.backendUrl + "/api/media/stillhere.png"}></img>

                    <h1>Post rappelant qu'un véhicule est toujours disponible</h1>
                    <h1>La fiche technique d'un véhicule à été mise à jour</h1>
                    <img src={Var.backendUrl + "/api/media/edited.png"}></img>
                    <img src={Var.backendUrl + "/api/media/summary.png"}></img>
                    <h1>Résumé de l'ensemble du stock disponible</h1>
                </div>
            </div>

        </div>)
    else
        return (<div className="ExamplePage">
            <div className="Content">
                <div className="Title">
                    <h1>Exemples pour chacun des posts</h1>
                    <p>Cette section montre un post example pour chacune des fonctionnalité de l’application.</p>
                </div>
                <div className="Examples">
                    <h1>Nouvelle voiture dans le catalogue</h1>
                    <img src={Var.backendUrl + "/api/media/newcar.png"}></img>
                    <h1>Nouvelle voiture dans le catalogue (Story)</h1>
                    <img src={Var.backendUrl + "/api/media/story.gif"}></img>
                    <h1>Un véhicule a été vendu</h1>
                    <img src={Var.backendUrl + "/api/media/soldcar.png"}></img>
                    <h1>Un véhicule a été mis en promotion</h1>
                    <img src={Var.backendUrl + "/api/media/promo.png"}></img>
                    <h1>Post rappelant qu'un véhicule est toujours disponible</h1>
                    <img src={Var.backendUrl + "/api/media/stillhere.png"}></img>
                    <h1>La fiche technique d'un véhicule à été mise à jour</h1>
                    <img src={Var.backendUrl + "/api/media/edited.png"}></img>
                    <h1>Résumé de l'ensemble du stock disponible</h1>
                    <img src={Var.backendUrl + "/api/media/summary.png"}></img>
                </div>
            </div>

        </div>
        )

}

export default ExamplePage