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


console.log(`get_fp.js - - - - - - - S`);

// TODO - use this to make sure fp loaded
// IIFE - check what scripts loaded
(function(){
  //var desiredSource = 'https://sitename.com/js/script.js';          // < - - TODO
  var scripts       = document.getElementsByTagName('script');
  var alreadyLoaded = false;

  if(scripts.length){
    for(var scriptIndex in scripts) {
      console.log(`id:${scripts[scriptIndex].id}\t- script: ${scripts[scriptIndex].src}`);
      //if(!alreadyLoaded && desiredSource === scripts[scriptIndex].src) {            // < - - TODO
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





console.log(`get_fp.js - - - - - - - E`);
