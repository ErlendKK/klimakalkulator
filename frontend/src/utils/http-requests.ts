import { ServerResponse } from "../interfaces/interfaces"

const BASE_URL = "http://localhost:5000"

async function getData(path: string): Promise<ServerResponse> {
  try {
    const response = await fetch(BASE_URL + path, {
      method: "GET",
      credentials: "include",
    })

    if (!response.ok) {
      throw new Error("response not ok")
    }

    const responseParsed: ServerResponse = await response.json()
    console.log(responseParsed)
    return responseParsed
  } catch (err) {
    console.log("error: " + err)
    return { status: "failed", message: "" }
  }
}

async function postData(payload: object, path: string): Promise<ServerResponse> {
  try {
    const response = await fetch(BASE_URL + path, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      throw new Error("response not ok")
    }

    const responseParsed: ServerResponse = await response.json()
    console.log(responseParsed)
    return responseParsed
  } catch (err) {
    console.log("error: " + err)
    return { status: "failed", message: "" }
  }
}

async function postForm(payload: object, path: string): Promise<ServerResponse> {
  let responseParsed: ServerResponse
  try {
    const response = await fetch(BASE_URL + path, {
      method: "POST",
      credentials: "include",
      body: payload,
    })

    responseParsed = await response.json()

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}: ${responseParsed.message || "unknown error"}`)
    }

    console.log(responseParsed)
    return responseParsed
  } catch (err) {
    console.log("error: " + err.message)
    return responseParsed ?? { status: "failed", message: "" }
  }
}

async function updateData(payload: object, path: string): Promise<ServerResponse> {
  try {
    const response = await fetch(BASE_URL + path, {
      method: "PUT",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      throw new Error("response not ok")
    }

    const responseParsed = await response.json()
    console.log(responseParsed)
    return responseParsed
  } catch (err) {
    console.log("error: " + err)
    return { status: "failed", message: "" }
  }
}

async function deleteData(path: string): Promise<ServerResponse> {
  try {
    const response = await fetch(BASE_URL + path, {
      method: "DELETE",
      credentials: "include",
    })

    if (!response.ok) {
      throw new Error("response not ok")
    }

    const responseParsed: ServerResponse = await response.json()
    console.log(responseParsed)
    return responseParsed
  } catch (err) {
    console.log("error: " + err)
    return { status: "failed", message: "" }
  }
}

export { getData, postData, postForm, updateData, deleteData }
