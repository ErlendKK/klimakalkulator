import { Project, Product, ProductInput } from '../interfaces/interfaces'

// Limit name length to avoid overflowing the form
const setDisplayedName = (product: Product | ProductInput, lengthMax: number): string => {
  let displayedName = product.name;
  if (product.name.length > lengthMax) { 
    displayedName = product.name.slice(0, lengthMax) + '...'; 
  }
  return displayedName;
}

// Returns the current data as a string formated (dd-mm-yyyy)
const getTodaysDate = (): string => {
  const today = new Date();
  const day = String(today.getDate()).padStart(2, '0');
  const month = String(today.getMonth() + 1).padStart(2, '0'); 
  const year = today.getFullYear();

  return `${day}.${month}.${year}`;
}

// Splits a date string into components
// Then converts it to Date obj formated as (yyyy-mm-dd)
const parseDate = (dateString: string): Date => {
  const [day, month, year] = dateString.split(".");
  return new Date(`${year}-${month}-${day}`);
};

type SortFunction<T> = (list: T[], sortBy: string, modifier: number) => T[];

// Sort an array of objeccts (table-inputs) based on date fields
const sortByDate: SortFunction<Project> = (list, sortBy, modifier) => {
  return list.sort((a, b) => {
    const dateA = parseDate(a[sortBy] as string);
    const dateB = parseDate(b[sortBy] as string);
    return (dateA.getTime() - dateB.getTime()) * modifier;
  });
};

// Sort an array of objeccts (table-inputs) based on non-date fields
const sortByField: SortFunction<Project | Product> = (list, sortBy, modifier) => {
  return list.sort((a, b) => {
    if (a[sortBy] < b[sortBy]) return -1 * modifier;
    if (a[sortBy] > b[sortBy]) return 1 * modifier;
    return 0;
  });
};

// Generate a new project ID or a new product id
function* generateIdForGuest() {
  let projectNumber = 1;
  let productNumber = 1;

  while (true) {
    const selector: string = yield;  // Pause and receive the next selector
    if (selector === 'project') {
      yield projectNumber++;
    } else if (selector === 'product') {
      yield productNumber++;
    } else {
      console.error(`Invalid argument passed to generateIdForGuest: ${selector}`);
      yield -1;
    }
  }
}

// Create a generator instance and start the generator
const idGenerator = generateIdForGuest();
idGenerator.next();  

const getNextId = (selector: string): number => {
  const result = idGenerator.next(selector);
  return result.value as number;
}

export { getTodaysDate, setDisplayedName, sortByDate, sortByField, getNextId, parseDate };