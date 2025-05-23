import { useContext, useEffect, useState } from 'react'
import "../styles/numericinput.scss"

function NumericInput(props) {

    const [value ,setValue] = useState(0)

    function handlePlus(){
            setValue(value+1)
    }

    function handleMinus(){
        if (value > 0){
            setValue(value-1)
        }
    }

    return (<div className="NumericInput">
        <span id="Minus" className="Sign" onClick={handleMinus}>-</span>
        <span className="Nb">{value}</span>
        <span id="Plus" className="Sign" onClick={handlePlus}>+</span>
    </div>)

}

export default NumericInput