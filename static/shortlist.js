// style note
// variable used on server python IE passed as JSON   server_var
// variable coming from client JS                     clientVar
// ref to html class                                  html-class


console.log(`shortlist.js - START`);
// prefsInfo passed in using jinja filter in HTML


function updateMoviePrefs(movId, buttonPref, movieRating=-1) {
  console.log( JSON.stringify( { 'mov_id_prefs':movId, 'button':buttonPref, 'rating': movieRating }) );

  fetch( '/short_list', {
    method: 'POST',                                             // method (default is GET)
    headers: {'Content-Type': 'application/json' },             // JSON
    body: JSON.stringify( { 'mov_id_prefs':movId, 'button':buttonPref, 'rating': movieRating } ) // Payload

  }).then( function(response) {
    return response.json();

  }).then( function(jsonResp) {
    console.log(`mov prefs UPDATED: ${movId} - ${jsonResp}`);
    window.location.replace('/short_list');
  }).catch( function(err){
    console.log(err);
  });
}


function clickHandler(e) {
  console.log("\n-\n-\n");
  console.log(e);
  console.log(e.target);
  console.log(e.target.classList);
  console.log("\n-\n-\n");


  // button classes
  // MOVIE PREFS  control-bt
  if (Array.from(e.target.classList).includes('control-bt')) {
    console.log(`control-bt: ${e.target.name}`);
    console.log(`${e.target.value}`);
    updateMoviePrefs(e.target.value, e.target.name);
  }

}




document.addEventListener('click', clickHandler);

document.addEventListener('DOMContentLoaded', (event) => {
  console.log('DOMContentLoaded:shortlist.js - S');

  Array.from(document.getElementsByClassName('bt-usr2')).forEach(
    function (element, index, array) {
        console.log(element);
        element.style.display = 'None';
    }
  );

  console.log('DOMContentLoaded:shortlist.js - E');
});








console.log(`shortlist.js - END`);
