import { useContext, useEffect, useState } from 'react'
import "../styles/tos.scss"
import * as Api from "../utils/Api.js"

function TosPage() {

    return (<div className="TosPage">
        <div className="Content">
            <h1>Conditions générales d'utilisation</h1>

            <h2>1. Introduction</h2>
            <p>Bienvenue sur AutoShare. Ces Conditions Générales d'Utilisation (CGU) régissent l'utilisation de notre service permettant aux vendeurs de voitures d'occasion professionnels de synchroniser leur stock Autoscout24 avec leur page Facebook. En utilisant notre application, vous acceptez pleinement ces conditions.</p>

            <h2>2. Accès et Utilisation du Service</h2>
            <p>Vous devez être un professionnel de la vente de voitures d'occasion et disposer d'un compte Autoscout24 et d'une page Facebook professionnelle.</p>
            <p>Vous nous autorisez à accéder aux informations de votre stock Autoscout24 et à publier des contenus sur votre page Facebook.</p>
            <p>Toute utilisation frauduleuse ou abusive du service est interdite.</p>

            <h2>3. Données Personnelles</h2>
            <p>Notre application collecte certaines informations personnelles conformément à notre <a href="privacy">Politique de Confidentialité</a>. Vous acceptez que nous utilisions vos données uniquement aux fins de fourniture du service.</p>
            <h2>4. Responsabilités</h2>
            <p>Nous nous efforçons de garantir un service fiable, mais nous ne pouvons garantir une disponibilité ininterrompue ou exempte d'erreurs.</p>
            <p>Vous êtes responsable du contenu publié sur votre page Facebook et de l'exactitude des données de votre stock.</p>
            <p>Nous ne sommes pas responsables des conséquences liées à l'utilisation de notre service, notamment en cas de dysfonctionnement des plateformes tierces (Facebook, Autoscout24).</p>

            <h2>5. Modifications du Service et des CGU</h2>
            <p>Nous nous réservons le droit de modifier ou d'interrompre le service à tout moment. Les présentes CGU peuvent également être mises à jour, et les utilisateurs en seront informés.</p>

            <h2>6. Résiliation</h2>
            <p>Vous pouvez cesser d'utiliser notre service à tout moment.</p>
            <p>Nous nous réservons le droit de suspendre ou de supprimer un compte en cas de violation de ces CGU.</p>

            <h2>7. Droit Applicable</h2>
            <p>Ces CGU sont soumises au droit belge. En cas de litige, les tribunaux compétents seront ceux de Namur.</p>
            <h2>8. Contact</h2>
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

export default TosPage