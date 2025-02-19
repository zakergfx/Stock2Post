import { useContext, useEffect, useState } from 'react'
import "../styles/login.scss"
import * as Api from "../utils/Api.js"
import { AuthContext } from '../context/AuthContext.js'
import FacebookLoginButton from '../components/FacebookLoginButton.js'

function LoginPage() {
    const token = "EAAIzZAhit7IcBOxnZCACOSngzA6pZCjRk2emlCrmTWlwP9ZBbVLX13ZA2GcCdTqAU1mjBAmaCkOhgdiZARz9E7OnXf4y9Tfxv7QRZCC53J5ZAqoskDjAG54hOv8otIli5WZCxZCIudFWYZBbJzY7JQCfOwa4BssLsS0fnIKy0tXOTBS7nV54qGAHW1HV1Gp8CnElgom"



    return (<div className="LoginPage">
        <div className="Content">
            <FacebookLoginButton/>

        </div>
    </div>)

}

export default LoginPage