import * as Var from "./Var.js"

export async function fetchGet(page, auth = true) {

    let headers = {}

    if (auth) {
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem("access")
        }
    }
    else {
        headers = {
            'Content-Type': 'application/json',
        }
    }

    const response = await fetch(Var.backendUrl + page, {
        method: "GET",
        headers: headers
    })

    try {
        const data = await response.json()

        if (data.detail) {
            data = data.detail
        }
        const msg = { "success": response.ok, "detail": data }
        return msg

    }

    catch {
        const msg = { "success": false, "detail": "error" }
        return msg


    }

}

export async function fetchPost(page, data, auth = true) {
    let headers;
    if (auth) {
        headers = {
            'Authorization': 'Bearer ' + localStorage.getItem("access"),
            'Content-Type': "application/json"
        };
    }
    else {
        headers = {
            'Content-Type': "application/json"
        };
    }



    data = JSON.stringify(data)

    try{
        const response = await fetch(Var.backendUrl + page, {
            method: "POST",
            headers: headers,
            body: data
        })
    
        data = await response.json()
        if (data.detail) {
            data = data.detail
        }
        const msg = { "success": response.ok, "detail": data }
    
        return msg
    }

    catch {
        const msg = { "success": false, "detail": "error" }
        return msg
    }

   
}

export async function fetchPatch(page, data) {
    let headers = {
        'Authorization': 'Bearer ' + localStorage.getItem("access"),
        'Content-Type': "application/json"
    };

    data = JSON.stringify(data)

    const response = await fetch(Var.backendUrl + page, {
        method: "PATCH",
        headers: headers,
        body: data
    })
    
    data = await response.json()
    if (data.detail) {
        data = data.detail
    }
    const msg = { "success": response.ok, "detail": data }

    return msg
}

export async function fetchDelete(page) {

    const response = await fetch(Var.backendUrl + page, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem("access")
        }
    })

    const msg = { "success": response.ok }
    return msg
}