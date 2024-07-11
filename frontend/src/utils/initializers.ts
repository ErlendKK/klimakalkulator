import { Product, Project, UserFormInput } from "../interfaces/interfaces"

const initializeProduct = (): Product => {
  return {
    EPD_URL: "",
    bygningsdel: "",
    classific: "",
    displayedName: "",
    name: "",
    owner: "",
    produktgruppe: "",
    project_id: 0,
    quantity: 0,
    regNo: "",
    type: "",
    unit: "",
    utskiftingsintervall: 0,
    uuid: "",
    validUntil: "",
    vedlikeholdsutslipp: 0,
  }
}

const initializeProject = (): Project => {
  return {
    active: 1,
    address: "",
    analyseperiode: 50,
    bta: 0,
    created_date: "",
    name: "",
    products: [],
    prosjektstart: 2024,
    type: "",
    updated_date: "",
  }
}

const initializeUser = (): UserFormInput => {
  return {
    email: "",
    message: "",
    name: "",
    photo_filename: "",
    photo_url: "",
    projects: [],
    stayLoggedIn: true,
  }
}

export { initializeProduct, initializeProject, initializeUser }
