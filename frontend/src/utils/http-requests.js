const BASE_URL = 'http://localhost:5000';


async function getData(path) {
    try {
        const response = await fetch(BASE_URL + path, {
            method: 'GET',
            credentials: 'include'
          })

        if (!response.ok) {
            throw new Error('response not ok');
        }

        const responseBody = await response.json();
        console.log(responseBody);
        return responseBody;

    } catch(err) {
        console.log('error: ' + err);
        return {status: 'failed'}
    }
}


async function postData(payload, path) {
    try {
        const response = await fetch(BASE_URL + path, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }, 
            credentials: 'include',
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('response not ok')
        }

        const responseBody = await response.json();
        console.log(responseBody);
        return responseBody;

    } catch(err) {
        console.log('error: ' + err);
        return {status: "failed"};
    }
}

async function postForm(payload, path) {
    let responseBody;
    try {
        const response = await fetch(BASE_URL + path, {
            method: 'POST',
            credentials: 'include',
            body: payload,
        });

        responseBody = await response.json();

        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}: ${responseBody.message || 'unknown error'}`);
        }
        
        console.log(responseBody);
        return responseBody;

    } catch(err) {
        console.log('error: ' + err.message);
        return responseBody ?? {status: "failed"};
    }
}


async function updateData(payload, path)  {
    try {
        const response = await fetch(BASE_URL + path, {
            method: "PUT",
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('response not ok');
        }

        const responseBody = await response.json();
        console.log(responseBody);
        return responseBody

    } catch(err) {
        console.log('error: ' + err);
        return {'status': 'failed'};
    }
}


async function deleteData(path) {
    try {
        const response = await fetch(BASE_URL + path, {
            method: "DELETE",
            credentials: 'include',
        });

        if (!response.ok) {
            throw new Error('response not ok');
        }

        const responseBody = await response.json();
        console.log(responseBody);
        return responseBody;

    } catch(err) {
        console.log('error: ' + err);
        return {'status': 'failed'};
    }
}

export { getData, postData, postForm, updateData, deleteData };