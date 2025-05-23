import { useContext, useEffect, useState } from 'react'
import "../styles/featurecard.scss"

function FeatureCard(props) {

    return (<div className="FeatureCard">
        <h3>{props.title}</h3>
        {props.children}
    </div>)

}

export default FeatureCard