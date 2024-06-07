// Limit name length to avoid overflowing the form
export const setDisplayedName = (product, lengthMax) => {
    let displayedName = product.name;
      if (product?.name.length > lengthMax) { 
        displayedName = product.name.slice(0, lengthMax) + '...'; 
      }
    return displayedName;
  }

// Returns the current data as a string formated (dd-mm-yyyy)
export const getTodaysDate = () => {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0'); 
    const year = today.getFullYear();
  
    return `${day}.${month}.${year}`;
}

// Splits a date string into components
// Then converts it to Date obj formated as (yyyy-mm-dd)
export const parseDate = (dateString) => {
  const [day, month, year] = dateString.split(".");
  return new Date(`${year}-${month}-${day}`);
};

// Sort an array of objeccts (table-inputs) based on date fields
export const sortByDate = (list, sortBy, modifier) => {
  return list.sort((a, b) => {
    const dateA = parseDate(a[sortBy]);
    const dateB = parseDate(b[sortBy]);
    return (dateA - dateB) * modifier;
  });
};

// Sort an array of objeccts (table-inputs) based on non-date fields
export const sortByField = (list, sortBy, modifier) => {
  return list.sort((a, b) => {
    if (a[sortBy] < b[sortBy]) return -1 * modifier;
    if (a[sortBy] > b[sortBy]) return 1 * modifier;
    return 0;
  });
};


