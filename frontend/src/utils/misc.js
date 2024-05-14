function logObject(obj) {
    Object.entries(obj).forEach(([key, value]) => {
        console.log(`${key}: ${value}`)
    })
}

// Limit name length to avoid overflowing the form
function setDisplayedName(product, lengthMax) {
    let displayedName = product.name;
      if (product.name && product.name.length > lengthMax) { 
        displayedName = product.name.slice(0, lengthMax) + '...'; 
      }
    return displayedName;
  }

function getTodaysDate() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0'); 
    const year = today.getFullYear();
  
    return `${day}.${month}.${year}`;
}



export { logObject, getTodaysDate, setDisplayedName }


