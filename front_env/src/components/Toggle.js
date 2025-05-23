import { useContext, useEffect, useState } from 'react'
import "../styles/toggle.scss"

function Toggle(props) {

    const [className, setClassName] = useState(props.isActive ? "Active" : "Inactive")

    function handleOnClick() {

        if (className === "Active") {
            setClassName("Inactive")
            props.setFct(false)
        }
        else if (className === "Inactive") {
            setClassName("Active")
            props.setFct(true)
        }

    }

    return (<div className="Toggle" >
        <div className={"Container " + className} onClick={handleOnClick}>
            <div className={"Button " + className} onClick={handleOnClick}></div>
        </div>



    </div>)
}

export default Toggle