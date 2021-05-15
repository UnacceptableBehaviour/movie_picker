// simple POC - fingerprint2.js test

var version='v0.0';
console.log(`fingerprint2.js test: ${version}`);

// register button click events
document.addEventListener("DOMContentLoaded", function(event) {
  document.getElementById('but_get_fp').addEventListener('click', getDeviceFP);
  document.getElementById('but_get_fpv18').addEventListener('click', getDeviceFPv18);
  document.getElementById('but_get_fpx64').addEventListener('click', getDeviceFPx64);
  document.getElementById('but_get_fpVs').addEventListener('click', getDeviceFPVs);
});


function getDeviceFP() {
  var fingerPrint = 'fp Object';
  var bShow = document.getElementById("but_show_fp");
  var textOp = document.getElementById("time_report");

  console.log(`device fingerprint type was: ${fingerPrint}`);

  var d1 = new Date();
  Fingerprint2.get(function(result) {
    var d2 = new Date();
    var timeString = (d2 - d1) + "ms";
    if(typeof window.console !== "undefined") {
      console.log(timeString);
      console.log(result);
    }
    console.log("typeof result");
    console.log(typeof result);
    console.log(`result[0] - ${result[0]}`);
    console.log(typeof result[0]);
    console.log(`result[0]["userAgent"] - ${result[0]["userAgent"]}`);
    console.log(`result[0]["fonts"] - ${result[0]["userAgent"]}`);

    var index = 0;
    result.forEach(function (arrayItem) {
      console.log(`${index} - ${arrayItem} - - - - - - - - - - - - - - - - - - - -`);
      for (const [key, val] of Object.entries(arrayItem)) {
          console.log(`key:${key}: size:${val.length}...\n${val}`);
      }
      index += 1;
    });

    for (const [key, val] of Object.entries(result)) {
        console.log(`${key}: ${val}`);
    }

    //for (const item in result) {
    //  console.log(typeof item);
    //  for (const property in item) {
    //    console.log(typeof property);
    //    console.log(`${property}: ${item[property]}`);
    //  }
    //}
    bShow.innerText = result;
    textOp.innerText = `Fingerprint calc took: ${timeString}`;
  });
}

function getDeviceFPv18() {
  var fingerPrint = 'V18';
  var bShow = document.getElementById("but_show_fpv18");
  var textOp = document.getElementById("time_report");

  console.log(`device fingerprint type was: ${fingerPrint}`);

  var d1 = new Date();
  Fingerprint2.getV18(function(result) {
    var d2 = new Date();
    var timeString = (d2 - d1) + "ms";
    if(typeof window.console !== "undefined") {
      console.log(timeString);
      console.log(result);
    }
    bShow.innerText = result;
    textOp.innerText = `Fingerprint calc took: ${timeString}`;
  });
}

function getDeviceFPx64() {
  var fingerPrint = 'x64hash128';
  var bShow = document.getElementById("but_show_fpx64");
  var textOp = document.getElementById("time_report");

  console.log(`device fingerprint type was: ${fingerPrint}`);

  bShow.innerText = Fingerprint2.x64hash128;
}

function getDeviceFPVs() {
  var fingerPrint = 'version';
  var bShow = document.getElementById("but_show_fpVs");
  var textOp = document.getElementById("time_report");

  console.log(`device fingerprint type was: ${fingerPrint}`);

  bShow.innerText = Fingerprint2.VERSION;
}

// uses Promises
// https://www.javascripttutorial.net/es6/javascript-promises/
//
// basic format of a promise
let completed = true;

let learnJS = new Promise(function (resolve, reject) {
    if (completed) {
        resolve("I have completed learning JS.");
    } else {
        reject("I haven't completed learning JS yet.");
    }
});

// from HTML http://valve.github.io/fingerprintjs2/
//<code id="time">
//
//  <button type="button" id="btn">Get my fingerprint</button>
//
//  <a href="https://github.com/Valve/fingerprintjs2"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://camo.githubusercontent.com/365986a132ccd6a44c23a9169022c0b5c890c387/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f7265645f6161303030302e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png"></a>
//
//  <script src="fingerprint2.js"></script>
//  <script>
//    $("#btn").on("click", function () {
//      var d1 = new Date();
//      var fp = new Fingerprint2();
//      fp.get(function(result) {
//        var d2 = new Date();
//        var timeString = "Time took to calculate the fingerprint: " + (d2 - d1) + "ms";
//        if(typeof window.console !== "undefined") {
//          console.log(timeString);
//          console.log(result);
//        }
//        $("#fp").text(result);
//        $("#time").text(timeString);
//      });
//    });
//  </script>
//
//</code>
