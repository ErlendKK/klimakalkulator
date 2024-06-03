// Slett prosjekt
const response = await fetch('http://localhost:5000/projects/delete/1', {
    method: "DELETE",
    credentials: 'include',
});

const data = await response.json();
console.log(data.message)

