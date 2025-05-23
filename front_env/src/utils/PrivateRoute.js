import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function PrivateRoute({ element: Component, ...rest }) {
    let {user} = useContext(AuthContext)

    return user ? (
        <Component {...rest} />
    ) : (
        <Navigate to="/login" />
    );
}

export default PrivateRoute;