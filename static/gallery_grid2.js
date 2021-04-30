// style note
// variable used on server python IE passed as JSON   server_var
// variable coming from client JS                     clientVar
// ref to html class                                  html-class


console.log(`gallery_grid.js - START`);
// prefsInfo passed in using jinja filter in HTML

// IIFE - check what scripts loaded
(function(){
  //var desiredSource = 'https://sitename.com/js/script.js';
  var scripts       = document.getElementsByTagName('script');
  var alreadyLoaded = false;

  if(scripts.length){
    for(var scriptIndex in scripts) {
      console.log(`id:${scripts[scriptIndex].id}\t- script: ${scripts[scriptIndex].src}`);
      //if(!alreadyLoaded && desiredSource === scripts[scriptIndex].src) {
      //    alreadyLoaded = true;
      //}
    }
  }
  if(!alreadyLoaded){
    // Run your code in this block?
  }
})();


var d1 = new Date();

// IIFE - get FP asap!
(function (time=d1) {
  console.log(`Calling FP2 ${time}`)

  Fingerprint2.getV18(function(result) {
    console.log(`FP2 callback ${result}`);
    var d2 = new Date();
    var timeString = (d2 - d1) + "ms";
    if(typeof window.console !== "undefined") {
      console.log(`FP ${result}`);
      console.log(timeString);
    }
    if (!prefsInfo.fingerprints.includes(result)){
      prefsInfo.fingerprints.push(result);
    }
    //textOp.innerText = `Fingerprint calc took: ${timeString}`;
  });
})();


function postUpdatePrefsToServer(){
  // TODO - store setting locally

  console.log( JSON.stringify( { 'prefs_info':prefsInfo }) );

  fetch( '/', {
    method: 'POST',                                             // method (default is GET)
    headers: {'Content-Type': 'application/json' },             // JSON
    body: JSON.stringify( { 'prefs_info':prefsInfo } )          // Payload

  }).then( function(response) {
    return response.json();

  }).then( function(jsonResp) {
    console.log(`setting UPDATED? - ${jsonResp}`);
  });

}

function updateMoviePrefs(movId, buttonPref, movieRating=-1) {
  console.log( JSON.stringify( { 'mov_id_prefs':movId, 'button':buttonPref, 'rating': movieRating }) );

  fetch( '/', {
    method: 'POST',                                             // method (default is GET)
    headers: {'Content-Type': 'application/json' },             // JSON
    body: JSON.stringify( { 'mov_id_prefs':movId, 'button':buttonPref, 'rating': movieRating } ) // Payload

  }).then( function(response) {
    return response.json();

  }).then( function(jsonResp) {
    console.log(`mov prefs UPDATED: ${movId} - ${jsonResp}`);
    window.location.replace('/');
  }).catch( function(err){
    console.log(err);
  });
}

function changeUser(new_id) {
  console.log( JSON.stringify( { 'new_id':new_id }) );

  fetch( '/', {
    method: 'POST',                                             // method (default is GET)
    headers: {'Content-Type': 'application/json' },             // JSON
    body: JSON.stringify( { 'new_id':new_id } )          // Payload

  }).then( function(response) {
    return response.json();

  }).then( function(jsonResp) {
    console.log(`user CHANGED to: ${prefsInfo.name} - ${jsonResp}`);
    window.location.replace('/');
  });
}



function clickHandler(e) {
  console.log("\n-\n-\n");
  console.log(e);
  console.log(e.target);
  console.log(e.target.classList);
  //console.log(e.target.parentNode.id);
  //console.log(e.target.parentNode.classList);
  console.log("\n-\n-\n");
  //postUpdatePrefsToServer();

  // button classes
  // ACTIVE USER  bt-usr      bt-usr-inactiv bt-usr-activ
  // GENRES       btn_genre   genre-pos genre-neg
  // MOVIE PREFS  control-bt


  if (Array.from(e.target.classList).includes('bt-usr')) {
    console.log(`${e.target.id}`);
    changeUser(e.target.id);
    return;
  }

  if (Array.from(e.target.classList).includes('control-bt')) {
    console.log(`${e.target.name}`);
    console.log(`${e.target.value}`);
    updateMoviePrefs(e.target.value, e.target.name);
  }
  //if (e.target.id.includes('tag_btn_id_')) { // its a tag - toggle it
  //  toggleTagInCategory(e.target);
  //
  //} else if (e.target.id.includes('_igd_btn_id')) {  // and an ingredients to exclude button
  //  input = document.getElementById('add_igd_form');
  //
  //  console.log(`IGD EXC = ${input.value}`); console.log(input);
  //
  //  if ( input.value === '' ) return; // dont add blanks
  //
  //  if (e.target.id === 'add_igd_btn_id') {
  //    ts = userInfo['tag_sets']['ingredient_exc'];           // add ingredient to tag sets to creat button
  //    ts.indexOf(input.value) === -1 ? ts.push(input.value) : console.log(`ADD - ALREADY PRESENT: ${input.value} <`);
  //
  //    df = userInfo['default_filters']['ingredient_exc'];   // seeing as we're creating the button user probably want it set!
  //    df.indexOf(input.value) === -1 ? df.push(input.value) : console.log(`ADD - ALREADY PRESENT: ${input.value} <`);
  //
  //  } else if (e.target.id === 'remove_igd_btn_id') {
  //    ts = userInfo['tag_sets']['ingredient_exc'];            // remove ingredient fomr tag_sets
  //    var index = ts.indexOf(input.value);
  //    index === -1 ? console.log(`REMOVE - ALREADY PRESENT: ${input.value} <`) : ts.splice(index, 1);
  //
  //    df = userInfo['default_filters']['ingredient_exc'];     // seeing as we're removing the button remove from user defaults
  //    index = df.indexOf(input.value);
  //    index === -1 ? console.log(`REMOVE - ALREADY PRESENT: ${input.value} <`) : df.splice(index, 1);
  //  }
  //
  //  postUpdatePrefsToServer();
  //
  //  // TODO - chain promises?
  //  console.log(`IGD EXC = RELOAD /settings`);
  //  window.location.replace('/settings');
  //
  //}

}



//HTMLCollection.prototype.forEach = Array.prototype.forEach;
//genre_buttons = document.getElementsByClassName('btn_genre'); // returns HTMLCollection - not array
//genre_buttons.forEach(  // requires HTMLCollection.prototype.forEach = Array.prototype.forEach;
//  function(element, index, array) {
//    console.log(index, element);
//  }
//);

function setButtonColours() {

  //console.log('User buttons -S');
  // genre buttons
  Array.from(document.getElementsByClassName("btn_genre")).forEach(   // getElementsByClassName returns HTMLCollection - not array
    function(element, index, array) {
      //console.log(element.value);
      if (prefsInfo.prefs_genre.neg.includes(element.value)) {
        element.classList.remove('genre-pos');
        element.classList.add('genre-neg');
      } else if (prefsInfo.prefs_genre.pos.includes(element.value)) {
        element.classList.remove('genre-neg');
        element.classList.add('genre-pos');
      }
    }
  );

  // current user button
  Array.from(document.getElementsByClassName("bt-usr")).forEach(   // getElementsByClassName returns HTMLCollection - not array
    function(element, index, array) {
      if (prefsInfo.name === element.innerText) {
        element.classList.remove('bt-usr-inactiv');
        element.classList.add('bt-usr-activ');
      } else {
        element.classList.remove('bt-usr-activ');
        element.classList.add('bt-usr-inactiv');
      }
    }
  );


}



document.addEventListener('click', clickHandler);

document.addEventListener('DOMContentLoaded', (event) => {
  console.log('document. - S');

  setButtonColours();

  console.log('document. - E');
});








console.log(`gallery_grid.js - END`);
