import { useContext, useEffect, useState } from 'react'
import "../styles/login.scss"
import * as Api from "../utils/Api.js"
import { AuthContext } from '../context/AuthContext.js'

function LoginPage() {
    const token = "EAAIzZAhit7IcBOZCEGcM8nLl9LBWVUFyREEIAM10IbVG49stkWqzI04UpYsA5ZAP5v1CnOzUehfk3xlAZCW1Gxy6ErNPY9ZCSpnZCAPa6RLrZAALdE8HAwZAaURWSjw4kPGgFUU5kYlTxg0TJPLXpahiHVylamOb6jbZBHJ12QYxJ2s0FJH12GMpN64gFNGKTS7I5"

    const { loginUser } = useContext(AuthContext)

    async function fbLogin() {
        alert("auth start")
        const response = await loginUser(token)
        if (response.success) {
            console.log("auth success")
        }

    }

    return (<div className="LoginPage">
        <div className="Content">
            <button onClick={fbLogin}>FB LOGIN</button>
        </div>
    </div>)

}

export default LoginPage