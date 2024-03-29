// prefsInfo passed in using jinja filter in HTML
//
// current_user: true
// fingerprints: ["6012bf36aba6d881aede81f36a75b819"]
// name: "usr3"
// ni_list: (10) ["8579674", "4218572", "2267968", "3040964", "7846844", "9340860", ...]
// prefs_actors: {neg: Array(0), pos: Array(0)}
// prefs_genre:
//   neg: (5) ["Documentary", "Music", "Comedy", "Sci-Fi", "Action"]
//   pos: (2) ["Adventure", "Thriller"]
// ratings: {}
// seen_list: (9) ["0078718", "6294822", "0816692", "7556122", "6386748", "7497366", ...]
// short_list: (3) ["9620292", "5867314", "7784604"]
// uuid: "1d016209-52d9-4539-ac45-f82acfb841be"
//
//
// - - - style note
// variable used on server python IE passed as JSON   server_var
// variable coming from client JS                     clientVar
// ref to html class                                  html-class


console.log(`gallery_grid.js - - - - - - - - S ${prefsInfo.name}`);



// update prefs W/O RELOADING
function postUpdatedPrefsToServerNOReload( successCallback=null, failureCallBack=null ){
  // TODO - store setting locally - PERSISTENT CACHE - one for each user on device

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

function removeValFromArray(val, arr){
  return arr.filter(function(element){
    return element != val;
  });
}

function updateGenrePrefs(genre){
  // change pref of button pressed
  // send update
  // update button colous on success
  if (prefsInfo.prefs_genre.neg.includes(genre)) {          // red > green
    prefsInfo.prefs_genre.neg = removeValFromArray(genre, prefsInfo.prefs_genre.neg);
    prefsInfo.prefs_genre.pos.push(genre);
  } else if (prefsInfo.prefs_genre.pos.includes(genre)) {   // green > grey
    prefsInfo.prefs_genre.pos = removeValFromArray(genre, prefsInfo.prefs_genre.pos);
  } else {
    prefsInfo.prefs_genre.neg.push(genre);                  // grey > red
  }
  postUpdatedPrefsToServerNOReload();
  setButtonColours();                       // TODO - call this on successful prefs update!
                                            // add callback to postUpdatedPrefsToServerNOReload(setButtonColours) ?
}

function updateSortByPrefs(sortType){
  prefsInfo.chosen_sort = sortType;
  postUpdatedPrefsToServerNOReload();
  setButtonColours();
}

function updateMoviePrefs(movId, buttonPref, route, reLoad=null, movieRating=-1) {
  console.log( JSON.stringify( { 'mov_id_prefs':movId, 'button':buttonPref, 'rating': movieRating }) );

  fetch( route, {
    method: 'POST',                                             // method (default is GET)
    headers: {'Content-Type': 'application/json' },             // JSON
    body: JSON.stringify( { 'mov_id_prefs':movId, 'button':buttonPref, 'rating': movieRating } ) // Payload

  }).then( function(response) {
    return response.json();

  }).then( function(jsonResp) {
    console.log(`mov prefs UPDATED: ${movId} - ${jsonResp}`);
    if (reLoad) {
      window.location.replace(reLoad);
    }
  }).catch( function(jsonResp){
    console.log(`setting UPDATED? - ${jsonResp}`);
  });
}


function changeUser(new_id) {
  console.log( JSON.stringify( { 'new_id':new_id }) );
  source = document.querySelector('body').id;
  if ( source === 'movie_gallery_home') {
    return_route = '/';
  } else {
    return_route = `/${source}`;
  };

  fetch( '/', {
    method: 'POST',                                             // method (default is GET)
    headers: {'Content-Type': 'application/json' },             // JSON
    body: JSON.stringify( { 'new_id':new_id } )                 // Payload

  }).then( function(response) {
    return response.json();

  }).then( function(jsonResp) {
    console.log(`user CHANGED to: ${prefsInfo.name} - ${jsonResp}`);
    window.location.replace(return_route);
  });
}


//<div class="rt-stars" id="rt-stars-7179594">
//  <img class="solo-star star-gold" srcset="static/SVG/star.svg" src="static/PNG/star.png" alt="rating star">
//  <img class="solo-star star-gold" srcset="static/SVG/star.svg" src="static/PNG/star.png" alt="rating star">
//</div>
function goldStars(e) {
  // color stars in set up to mouseover star gold and the rest grey
  let stars = e.target.parentElement.getElementsByClassName('solo-star');
  let movId = e.target.parentElement.id.replace('rt-stars-', '');
  let movRating = 0;

  Array.from(stars).forEach( a => {
    if (a.value <= e.target.value) {
      a.classList.remove('star-grey');
      a.classList.add('star-gold');
      movRating = a.value;
    } else {
      a.classList.remove('star-gold');
      a.classList.add('star-grey');
    }
  });

  prefsInfo.ratings[movId] = movRating;
}


// display single movie
function showMovieWithID(movId) {
  console.log( JSON.stringify( { 'show_mov_id':movId }) );

  fetch( '/', {
    method: 'POST',                                              // method (default is GET)
    headers: {'Content-Type': 'application/json' },             // JSON
    body: JSON.stringify( { 'show_mov_id':movId })  // Payload

  }).then( function(response) {
    return response.json();

  }).then( function(jsonResp) {
    console.log(`mov prefs UPDATED: ${movId} - ${jsonResp}`);
    window.location.replace('/');
  }).catch( function(err){
    console.log(err);
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
  //postUpdatedPrefsToServerNOReload();

  // button classes
  // ACTIVE USER  bt-usr2     btn-warning bt-usr-inactiv bt-usr-activ
  // GENRES       btn-genre   btn-success btn-danger
  // MOVIE PREFS  control-bt

  if (Array.from(e.target.classList).includes('glid-div-box')) {
    console.log(`slider click: ${e.target.id}`);
    showMovieWithID(e.target.id);
    return;
  }

  if (Array.from(e.target.classList).includes('bt-usr2')) {
    console.log(`${e.target.id}`);
    changeUser(e.target.id);
    return;
  }

  if (Array.from(e.target.classList).includes('btn-genre')) {
    console.log(`btn-genre: ${e.target.value}`);
    updateGenrePrefs(e.target.value);
    return;
  }

  if (Array.from(e.target.classList).includes('bt-sort')) {
    console.log(`bt-sort: ${e.target.value}`);
    updateSortByPrefs(e.target.value);
    return;
  }

  if (Array.from(e.target.classList).includes('control-bt')) {
    let targetButton = e.target.name;
    let routeId = document.getElementsByTagName("BODY")[0].id;
    let movieCard = e.target.closest('.grid-movie-card-v2');
    let movId = movieCard.id.replace('gmc','');   // go up node tree until find first class='bla'
    console.log(`BUT: ${targetButton}`);
    console.log(`movId: ${e.target.value}`);
    console.log(`route: ${routeId}`);
    switch (targetButton) {
      case 'mov_prefs_rate':
        console.log(`RATE CLICKED: ${targetButton}`);

        console.log(`movId: ${movId}`);
        let rtStars = document.getElementById(`rt-stars-${movId}`);

        if (rtStars.children.length > 0) { // send rating
          console.log(`RATE > SEND RATING as PREFS JSON : ${prefsInfo.ratings[movId]}`);
          postUpdatedPrefsToServerNOReload();
        } else { // add stars to rate movie
          console.log(`rtStars.children.length == 0: ${rtStars.children.length}`);
          for (let s = 1; s < 11; s += 1) {
            let starColour = 'star-grey';
            if (s <= prefsInfo.ratings[movId]) { starColour = 'star-gold'; }
            greyStar = document.createElement('img');
            greyStar.value = s;
            greyStar.name = 'mov_prefs_star';
            greyStar.className = "control-bt solo-star " + starColour;
            greyStar.srcset = "/static/SVG/star.svg";
            greyStar.src="/static/PNG/star.png";
            greyStar.alt="rating star";
            //greyStar.addEventListener('mouseenter', goldStars(e) ); // calls function and uses result as callback!
            greyStar.addEventListener('mouseenter', function(e){ goldStars(e); });  // do this instead!
            //greyStar.addEventListener('mouseenter', goldStars);   // w/o argument
            rtStars.appendChild(greyStar);
          }
        }
        break;

      case 'mov_prefs_star':
        console.log(`STAR > SEND RATING as PREFS JSON: ${prefsInfo.ratings[movId]}`);
        postUpdatedPrefsToServerNOReload();
        break;
      case 'mov_prefs_sl': // REMOVE BUTTON in SL & combined_SL
        switch (routeId) {
          case 'movie_gallery_home':
            console.log('+List BUTTON - ROUTE: movie_gallery_home');
            updateMoviePrefs(movId, 'mov_prefs_sl', '/');
            movieCard.remove();
            break;
          case 'movie_gallery_single':
            console.log('+List BUTTON - ROUTE: movie_gallery_single');
            updateMoviePrefs(movId, 'mov_prefs_sl', '/', '/slider_tests');
            break;
          case 'short_list':
            console.log('REMOVE BUTTON - ROUTE: short_list');
            updateMoviePrefs(movId, 'mov_prefs_sl', '/short_list');
            movieCard.remove();
            break;
          case 'combined_short_list':
            updateMoviePrefs(movId, 'mov_prefs_sl', '/combined_short_list');
            movieCard.remove();
            break;
        }
        break;
      case 'mov_prefs_seen': // SEEN BUTTON in SL & gallery
        switch (routeId) {
          case 'movie_gallery_home':
            console.log('SEEN BUTTON - ROUTE: movie_gallery_home');
            updateMoviePrefs(movId, 'mov_prefs_seen', '/');
            movieCard.remove();
            break;
          case 'movie_gallery_single':
            console.log('SEEN BUTTON - ROUTE: movie_gallery_single');
            updateMoviePrefs(movId, 'mov_prefs_seen', '/', '/slider_tests');
            break;
          case 'short_list':
            console.log('SEEN BUTTON - ROUTE: short_list');
            updateMoviePrefs(movId, 'mov_prefs_seen', '/short_list');
            movieCard.remove();
            break;
          case 'combined_short_list':                                // WTF?
            console.log('SEEN BUTTON - ROUTE: combined_short_list'); // DOESN'T EXIST - TODO WHY NOT MOST LIKELY NEEDED
            updateMoviePrefs(movId, 'mov_prefs_seen', '/combined_short_list');
            movieCard.remove();
            break;
        }
        break;
      case 'mov_prefs_ni': // NOT INTERESTED
        switch (routeId) {
          case 'movie_gallery_home':
            console.log('NI BUTTON - ROUTE: movie_gallery_home');
            updateMoviePrefs(movId, 'mov_prefs_ni', '/');
            movieCard.remove();
            break;
          case 'movie_gallery_single':
            console.log('SEEN BUTTON - ROUTE: movie_gallery_single');
            updateMoviePrefs(movId, 'mov_prefs_ni', '/', '/slider_tests');
            break;
        }
        break;
      default:
        console.log(`default: * * * * WARNING * * * *  button shouldn't exit: ${e.target.name} - id: ${e.target.value}`);

    }
  }
}




//HTMLCollection.prototype.forEach = Array.prototype.forEach;
//genre_buttons = document.getElementsByClassName('btn-genre'); // returns HTMLCollection - not array
//genre_buttons.forEach(  // requires HTMLCollection.prototype.forEach = Array.prototype.forEach;
//  function(element, index, array) {
//    console.log(index, element);
//  }
//);

function setButtonColours() {

  //console.log('User buttons - - - S');
  // genre buttons
  Array.from(document.getElementsByClassName("btn-genre")).forEach(   // getElementsByClassName returns HTMLCollection - not array
    function(element, index, array) {
      console.log(element.value);
      if (prefsInfo.prefs_genre.neg.includes(element.value)) {
        element.classList.remove('btn-success');
        element.classList.add('btn-danger');
      } else if (prefsInfo.prefs_genre.pos.includes(element.value)) {
        element.classList.remove('btn-danger');
        element.classList.add('btn-success');
      } else {
        element.classList.remove('btn-danger');
        element.classList.remove('btn-success');
        element.classList.add('btn-secondary');
      }
    }
  );

  // current user button
  Array.from(document.getElementsByClassName("bt-usr2")).forEach(   // getElementsByClassName returns HTMLCollection - not array
    function(element, index, array) {
      if (prefsInfo.name === element.innerText) {
        element.classList.remove('btn-secondary');  //highlight SELECTED user
        element.classList.add('btn-warning');
      } else {
        element.classList.remove('btn-warning');
        element.classList.add('btn-secondary');
      }
    }
  );

  // set SORT BY button selection
  Array.from(document.getElementsByName('sort_type')).forEach(
    function (element) {
      console.log(`sort_type ${element.value} - pref.chosen ${prefsInfo.chosen_sort}`);
      if (prefsInfo.chosen_sort === element.value) {
        console.log(`sort_type ${element.value} SELECTED`);
        element.classList.add('btn-success');
        element.classList.remove('btn-secondary');
      } else {
        element.classList.remove('btn-success');
        element.classList.add('btn-secondary');
      }
    }
  );
}

function customiseButtons() {
  let routeId = document.getElementsByTagName("BODY")[0].id;
  console.log(`customiseButtons - routeId = ${routeId}`);
  // TODO page customisation
  switch (routeId) {
    case 'movie_gallery_home':
      break;
    case 'play_movie':
      break;
    case 'short_list':
      Array.from(document.getElementsByName('mov_prefs_sl')).forEach(   // TODO - can we use fall through for DRY code
        function (element, index, array) {
            console.log(element);
            element.textContent = 'Remove';
        }
      );
      Array.from(document.getElementsByClassName('bt-usr2')).forEach(   // TODO - can we use fall through for DRY code
        function (element, index, array) {
            console.log(element);
            element.style.display = 'None';
        }
      );
      break;
    case 'combined_short_list':
      Array.from(document.getElementsByName('mov_prefs_sl')).forEach(   // TODO - can we use fall through for DRY code
        function (element, index, array) {
            console.log(element);
            element.textContent = 'Remove';
        }
      );
      Array.from(document.getElementsByClassName('bt-usr2')).forEach(   // TODO - can we use fall through for DRY code
        function (element, index, array) {
            console.log(element);
            element.style.display = 'None';
        }
      );
      Array.from(document.getElementsByName('mov_prefs_rate')).forEach(
        function (element, index, array) {
            console.log(element);
            element.style.display = 'None';
        }
      );
      Array.from(document.getElementsByName('mov_prefs_seen')).forEach(
        function (element, index, array) {
            console.log(element);
            element.style.display = 'None';
        }
      );
      break;
    case 'slider_tests':
      break;
    case 'settings':
      break;
    default:
  }
}

document.addEventListener('click', clickHandler);

document.addEventListener('DOMContentLoaded', (event) => {
  console.log('DOMContentLoaded:gallery_grid.js - S');

  setButtonColours();

  customiseButtons();

  console.log('DOMContentLoaded:gallery_grid.js - E');
});








console.log(`gallery_grid.js - - - - - - - - E`);
