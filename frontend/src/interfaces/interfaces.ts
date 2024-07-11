interface ServerResponse {
    message: string,
    status: string,
    data?: object
  }

  interface EmissionFactor {
    A1: number;
    A1A2A3: number;
    A2: number;
    A3: number;
    A4: number;
    C1: number;
    C2: number;
    C3: number;
    C4: number;
    D: number;
  }

  interface Product {
    EPD_URL: string;
    bygningsdel: string;
    classific: string;
    displayedName: string;
    emission_factors?: EmissionFactor;
    emission_id?: number;
    product_id?: number;
    name: string;
    owner: string;
    produktgruppe: string;
    project_id: number;
    quantity: number;
    regNo: string;
    type: string;
    unit: string;
    utskiftingsintervall: number;
    uuid: string;
    validUntil: string;
    vedlikeholdsutslipp: number;
    product?: object  // Handles temporary nested product properties
  }

  interface Project {
    active: number;
    address: string;
    analyseperiode: number;
    bta: number;
    created_date: string;
    name: string;
    products: Product[];
    prosjektstart: number;
    type: string;
    updated_date: string;
    user_id?: number;
    project_id?: number;
  }

  interface User {
    email: string;
    message: string;
    name: string;
    photo_filename: string;
    photo_url: string;
    projects: Project[];
    user_id?: number;
  }

  interface UserFormInput extends User {
    photo?: File;
    stayLoggedIn?: boolean;
    password?: string;
    confirmPassword?: string;
  }

  interface TableEntry {
    heading: string, 
    body: string, 
    sortable: boolean
  }

  interface Result {
    'bygningsdel': string, 
    'A1-A3': number, 
    'A4': number, 
    'B2': number, 
    'B4': number, 
    'C': number, 
    'total': number, 
    'andel': string
  };

  interface GlobalState {
    isLoggedIn: boolean;
    user: User | null;
    projects: Project[];
    currentProject: Project | null;
  }

  interface SortPreference {
    currentSort: any,
    sortAscending: boolean
  }

  interface EmissionDataResponse {
    emission_factors: EmissionFactor;
    unit: string;
  }
  

  export {ServerResponse, EmissionFactor, Product, Project, User, UserFormInput, TableEntry, Result, GlobalState, SortPreference, EmissionDataResponse };