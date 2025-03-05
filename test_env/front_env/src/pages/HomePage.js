import { useContext, useEffect, useState } from 'react'
import "../styles/home.scss"
import * as Api from "../utils/Api.js"
import * as Var from "../utils/Var.js"
import FeatureCard from '../components/FeatureCard.js'
import { MainContext } from '../context/MainContext.js'

function HomePage() {

    const {isMobile} = useContext(MainContext)

    return (<div className="HomePage" id="home">
        <div className="Content">
            <h1>Gagnez en visibilité sur les réseaux sociaux sans effort</h1>
            <p className="Subtitle">Synchronisez automatiquement votre stock <span className="AS">AutoScout24</span> avec votre page <span className="FB">Facebook</span> et <span className="IG">Instagram (bientôt disponible)</span></p>
            {!isMobile ? <div className="Visuals">
                <img id="iphone" src={Var.backendUrl + "/api/media/iphone.png"} />
                <div className="MacAndCta">
                    <img id="mac" src={Var.backendUrl + "/api/media/mac.png"} />
                    <div className="TextAndCta">
                        <span>Intéressé par ce service ?</span>
                        <a href="/#contact" className="Button Primary">Je demande une démo !</a>
                    </div>
                </div>
            </div> :
                <div className="Visuals">
                    <div className="MacAndCta">
                        <div className="Img"><img id="iphone" src={Var.backendUrl + "/api/media/iphone.png"} /></div>
                        <div className="TextAndCta">
                            <span>Intéressé par ce service ?</span>
                            <a href="/#contact" className="Button Primary">Je demande une démo !</a>
                        </div>
                    </div>
                </div>}

            <div className="Features" id="features">
                <div className="Titles">
                    <h2>Fonctionnalités</h2>
                    <p>Les fonctionnalités suivantes sont déjà disponible et vous permettent de gérer <b>automatiquement</b> vos réseaux</p>
                </div>
                <div className="Cards">
                    <div className="Card">
                        <h3>Création de post</h3>
                        <div className="CardContent" id="card1">
                            <h4><span className="Red">!!!</span> Nouvel arrivage <span className="Red">!!!</span></h4>
                            <p>Très beau modèle de <b>Ford Focus</b> au prix de <b>9 800 €</b></p>
                            <p><b>Première immatriculation : </b>04/2021
                                <br /><b>Kilométrage : </b>95 000 km
                                <br /><b>Carburant : </b>Essence
                                <br /><b>Transmission : </b>Manuelle
                                <br /> <b>Puissance : </b>96 kw (131 ch)
                            </p>
                            <p>
                                <b>Téléphone : </b>0477 26 19 90
                                <br /><b>Mail : </b>abc@example.com
                            </p>
                            <p><b>Consulter en détail sur : <br /></b><a href="https://autoscout24.be/fordfocus/14568">https://autoscout24.be/fordfocus/14568</a></p>
                            <div className="ImgContainer">
                                <img src={Var.backendUrl + "/api/media/redcar.png"}></img>
                            </div>
                        </div>
                    </div>
                    <div className="Card">
                        <h3>Création de story</h3>
                        <div className="CardContent" id="card2">
                            <img src={Var.backendUrl + "/api/media/redcar.png"}></img>
                            <h4><span className="Red">!!!</span> Nouvel arrivage <span className="Red">!!!</span></h4>
                            <div className="ModelAndDesc">
                                <b>Ford Focus</b>
                                <span className="Description">Avec caméra de recul, kit main libre, etc ...</span>
                            </div>
                            <div className="Table">
                                <span>Essence</span>
                                <span className="Right">Manuel</span>
                                <span >04/2021</span>
                                <span className="Right">95 000 km</span>
                                <span>96 kw (131 ch)</span>
                                <span className="Right">Garantie 12 mois</span>
                                <b id="price">9800 €</b>
                            </div>
                            <b className="Contacts">0477 26 19 90 - abc@example.com</b>
                        </div>
                    </div>
                    <div className="Card">
                        <h3>Autres cas d'usage</h3>
                        <div className="CardContent" id="card3">
                            <div className="SubCard">
                                <b>Création automatique de posts dans les cas suivants :</b>
                                <ul>
                                    <li>Un véhicule est <b>en réduction</b></li>
                                    <li>Un véhicule a été <b>vendu</b></li>
                                    <li>La fiche technique d'un véhicule a été <b>modifiée</b></li>
                                    <li>Un véhicule disponible depuis <b>X semaines</b> n'a <b>pas</b> encore <b>été vendu</b></li>
                                </ul>
                                <span><b>Remise en avant</b> de l'ensemble du catalogue de manière régulière</span>
                            </div>
                            <a href="/examples" className="Button Secondary">Voir des exemples concrets</a>
                            <a href="/#contact" className="Button Primary">Je demande une démo !</a>
                        </div>
                    </div>
                </div>
            </div>
            <div className="Contact" id="contact">
                <h2>Nous contacter</h2>
                <p>Que cela soit pour nous <b>poser une question</b> ou bien <b>demander une démo</b>, voici comment vous pouvez nous contacter</p>
                <span><b>Téléphone : </b>0477 26 19 90</span>
                <span><b>Mail : </b>loick.leroy01@gmail.com</span>
                <br /><span>Ou bien via ce formulaire</span><br />
                <form>
                    <label for="name">Nom</label>
                    <label for="surname">Prénom</label>
                    <input type="text" id="name"></input>
                    <input type="text" id="surname"></input>
                    <label for="phone">N° de téléphone</label>
                    <label for="mail">Adresse mail</label>
                    <input type="number" id="phone"></input>
                    <input type="text" id="mail"></input>
                    <label className="Wide" for="company">Nom de votre entreprise</label>
                    <input className="Wide" type="text" id="company"></input>
                    <label className="Wide" for="message">Message</label>
                    <textarea rows="10" className="Wide" id="message"></textarea>
                    <a className="Button Primary">Envoyer</a>
                </form>
            </div>
            <div className="NextFeatures" id="nextfeatures">
                <h2>Fonctionnalités à venir</h2>
                <p>L'application est amenée à évoluer au cours du temps. Voici les fonctionnalités qui vont arriver prochainement</p>
                <div className="FeatureCards">
                    <FeatureCard title="Planification horaire">
                        <p>Possibilité de choisir quel jour et à quelle heure sont faites les publication.</p>
                        <p>L’objectif est de maximiser la visibilité des posts en vous permettant de publier aux heures de pics d’utilisation des réseaux sociaux.</p>
                    </FeatureCard>
                    <FeatureCard title="Page de statistiques">
                        <p>Page qui reprend le nombre de posts qu’AutoShare a fait pour vous.</p>
                        <p>
                            L’objectif est que vous puissiez facilement vous rendre compte si oui ou non l’application vous fait gagner en temps et visibilité.</p>
                    </FeatureCard>
                    <FeatureCard title="Intégration d’Instagram">
                        <p>L’outil sera capable de publier des posts et Story (Reels) sur instagram. Pour ce faire il vous suffira de lier votre compte Instagram via l’onglet de Connexion.</p>
                    </FeatureCard>
                    <FeatureCard title="Mise en avant des avis">
                        <p>Les avis positifs des utilisateurs laissés sur AutoScout pourront être automatiquement publiés sur votre page Facebook.</p>
                    </FeatureCard>
                </div>
            </div>
        </div>
    </div >)

}

export default HomePage