// add the fetch interface to VLC
// simple POC

// assign movie info to local parameter
console.log(`play_movie.js - - - - - - - - - - S: ${movie['title']} - ${movie['genres']}`);

const ST_PAUSED = 10;
const ST_PLAYING = 20;
const ST_FF2X = 30;
const ST_RR2X = 40;

var Remote = {};
Remote.state = ST_PLAYING;

// map button id to functions
var idToFunc = {
  'rcbt-start':   buttonStart,
  'rcbt-bak30s':  buttonBak30s,
  'rcbt-play':    buttonPlay,
  'rcbt-fwd30s':  buttonFwd30s,
  'rcbt-end':     buttonEnd,

  'rcbt-bak2x':   buttonBak2x,
  'rcbt-vol':     buttonVol,
  'rcslid-vol':   sliderVol,
  'rcbt-fwd2x':   buttonFwd2x,

  'rcbt-s1':      buttonS1,
  'rcbt-s2':      buttonS2
}
// ROW 1 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function buttonStart(){
  console.log('func: button Back to START');
  sendCommand('start');
}
function buttonBak30s(){
  console.log('func: button REWIND 30 secs');
  sendCommand('bak30s');
}

function buttonPlay(){
  if ((Remote.state === ST_PAUSED) ||
      (Remote.state === ST_FF2X)   ||
      (Remote.state === ST_RR2X))  {
    Remote.state = ST_PLAYING ;
    console.log(`func: button PLAY - state:${Remote.state}`);
    document.getElementById("rcbt-play").innerText = 'PAUSE';
    sendCommand('play');

  } else if (Remote.state === ST_PLAYING) {
    Remote.state = ST_PAUSED ;
    console.log(`func: button PAUSED - state:${Remote.state}`);
    document.getElementById("rcbt-play").innerText = 'PLAY';
    sendCommand('pause');
  }
  console.log('buttonPlay: movie');
  console.log(movie);
  // PLAY / PAUSE based on state
  // update state & button ICON

}
function buttonFwd30s(){
  console.log('func: button FORWARD 30 secs');
  sendCommand('fwd30s');
}
function buttonEnd(){
  console.log('func: button Goto END');
  sendCommand('end');
}

// ROW 2 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function buttonBak2x(){
  Remote.state = ST_RR2X;
  console.log('func: button REWIND -120sec');
  sendCommand('bak2x');
}
function buttonVol(){
  Remote.vol = document.getElementById("rcslid-vol").value;
  console.log(`func: button VOL -  ${Remote.vol}`);
  sendCommand('vol'); // TODO add slider move event listener
}
function sliderVol(){
  Remote.vol = document.getElementById("rcslid-vol").value;
  console.log(`func: button VOL slider ${Remote.vol}`);
  sendCommand('vol'); // TODO add slider move event listener
}
function buttonFwd2x(){
  Remote.state = ST_FF2X;
  console.log('func: button FORWARD 2x');
  sendCommand('fwd2x');
}

// ROW 3 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function buttonS1(){
  console.log('func: button S1');
  sendCommand('s1');
}
function buttonS2(){
  console.log('func: button S2');
  sendCommand('s2');
}

function consoleButton(e){
  console.log('> - - - - - - - - - - - - - - - - - - - - - - - - - - - S');
  console.log(`remote: ${e.srcElement.innerText} - ID ${e.srcElement.id}`);
  console.log(e);
  console.log(e.srcElement);
  console.log(e.srcElement.classList);
  console.log('> - - - - - - - - - - - - - - - - - - - - - - - - - - - E');

  idToFunc[e.srcElement.id]();
}

// register button click events
document.addEventListener("DOMContentLoaded", function(event) {
  console.log('DOMContentLoaded:/play_movie.js - - - - - S');
  Array.from(document.getElementsByClassName('bt-usr2')).forEach(
    function (element, index, array) {
        console.log(element);
        element.style.display = 'None';
    }
  );
  console.log('DOMContentLoaded:/play_movie.js - - - - - M');
  document.querySelector('.rc-item.rc-start').addEventListener('click', consoleButton);
  document.querySelector('.rc-item.rc-back30s').addEventListener('click', consoleButton);
  document.querySelector('.rc-item.rc-play').addEventListener('click', consoleButton);
  document.querySelector('.rc-item.rc-forward30s').addEventListener('click', consoleButton);;
  document.querySelector('.rc-item.rc-end').addEventListener('click', consoleButton);

  document.querySelector('.rc-item.rc-back2x').addEventListener('click', consoleButton);
  document.querySelector('.rc-item.rc-volume').addEventListener('click', consoleButton);
  document.querySelector('.rc-item.rc-forward2x').addEventListener('click', consoleButton);
  Remote.vol = document.getElementById("rcslid-vol").value;

  document.querySelector('.rc-item.rc-s1').addEventListener('click', consoleButton);
  document.querySelector('.rc-item.rc-s2').addEventListener('click', consoleButton);
  console.log('DOMContentLoaded/play_movie.js - - - - - E');
});

// S1
function sendCommand (cmd) {
  json_cmd = {
    id: movie.id,
    path: movie.file_path,
    vol: Remote.vol,
    cmd: cmd
  };
  console.log(`sendCommand: ${cmd}`);

  fetch(`${window.origin}/play_movie/${movie.id}`, {
  //fetch(`/play_movie/${movie.id}`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(json_cmd),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    .then(function(response) {
      if (response.status !== 200) {
        console.log(`Looks like there was a problem. Status code: ${response.status}`);
        return;
      }
      response.json().then(function(data) {
        console.log(`sendCommand RX:`);
        console.log(data);
      });
    })
    .catch(function(error) {
      console.log("Fetch error: " + error);
  });

}

// S2
function getStatus ( route=`/play_movie/${movie.id}` ) {

}

console.log('play_movie.js - - - - - - - - - - E');
