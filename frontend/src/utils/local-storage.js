function saveToLocalStorage(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (e) {
      console.error('Failed to save to localStorage', e);
      return false;
    }
  }
  
  function getFromLocalStorage(key) {
    try {
      const value = localStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (e) {
      console.error('Failed to retrieve from localStorage', e);
      return null;
    }
  }
  
  function removeFromLocalStorage(key) {
    try {
      localStorage.removeItem(key);
      return true;
    } catch (e) {
      console.error('Failed to remove item from localStorage', e);
      return false;
    }
  }

  export {saveToLocalStorage, getFromLocalStorage, removeFromLocalStorage }