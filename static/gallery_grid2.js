console.log(`gallery_grid.js - START`);

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
// prefsInfo passed in using jinja filter in HTML

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


function postUpdateSettingsToServer(){
  // TODO - store setting locally

  console.log( JSON.stringify( { 'prefs_info':prefsInfo }) );

  fetch( '/', {
    method: 'POST',                                             // method (default is GET)
    headers: {'Content-Type': 'application/json' },             // JSON
    //body: JSON.stringify( { 'uuid':prefsInfo.uuid, 'prefs_info':prefsInfo } )      // Payload
    body: JSON.stringify( { 'prefs_info':prefsInfo } )      // Payload

  }).then( function(response) {
    return response.json();

  }).then( function(jsonResp) {
    //window.location.replace('/tracker');
    //window.location.replace('/weigh_in');
    console.log(`setting UPDATED? - ${jsonResp}`);
  });

}


document.addEventListener('click', clickHandler);

function clickHandler(e) {
  console.log("\n-\n-\n");
  console.log(e);
  console.log(e.target);
  console.log(e.target.parentNode.id);
  console.log(e.target.parentNode.classList);
  console.log("\n-\n-\n");
  postUpdateSettingsToServer();

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
  //  postUpdateSettingsToServer();
  //
  //  // TODO - chain promises?
  //  console.log(`IGD EXC = RELOAD /settings`);
  //  window.location.replace('/settings');
  //
  //}

}




















console.log(`gallery_grid.js - END`);
