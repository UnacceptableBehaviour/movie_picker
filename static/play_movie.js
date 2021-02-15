// add the fetch interface to VLC
// simple POC


var movie_display_name='movie odyssey v0.0';
console.log(`RUNNING: ${movie_display_name}`);

// assign movie info to local parameter
console.log(`JS movie local ${movie['title']} - ${movie['genres']} - inline`); 
  
const ST_PAUSED = 10;
const ST_PLAYING = 20;
const ST_FF2X = 30;
const ST_RR2X = 40;

var Remote = {};
Remote.state = ST_PAUSED;

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
}
function buttonBak30s(){
  console.log('func: button REWIND 30 secs');
}

function buttonPlay(){
  if ((Remote.state === ST_PAUSED) ||
      (Remote.state === ST_FF2X)   ||
      (Remote.state === ST_RR2X))  {
    Remote.state = ST_PLAYING ;
    console.log(`func: button PLAY - state:${Remote.state}`);
    document.getElementById("rcbt-play").innerText = 'PAUSE';
    
  } else if (Remote.state === ST_PLAYING) {
    Remote.state = ST_PAUSED ;
    console.log(`func: button PAUSED - state:${Remote.state}`);
    document.getElementById("rcbt-play").innerText = 'PLAY';
  }

  // PLAY / PAUSE based on state
  // update state & button ICON
}
function buttonFwd30s(){  
  console.log('func: button FORWARD 30 secs');
}
function buttonEnd(){
  console.log('func: button Goto END');
}

// ROW 2 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function buttonBak2x(){
  Remote.state = ST_RR2X;
  console.log('func: button REWIND 2x');
}
function buttonVol(){
  var volume = document.getElementById("rcslid-vol").value;
  console.log(`func: button VOL -  ${volume}`);
}
function sliderVol(){
  var volume = document.getElementById("rcslid-vol").value;
  console.log(`func: button VOL slider ${volume}`);
}
function buttonFwd2x(){
  Remote.state = ST_FF2X;
  console.log('func: button FORWARD 2x');
}

// ROW 3 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function buttonS1(){
  console.log('func: button S1');
}
function buttonS2(){
  console.log('func: button S2');
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
  document.querySelector('.rc-item.rc-start').addEventListener('click', consoleButton);
  document.querySelector('.rc-item.rc-back30s').addEventListener('click', consoleButton);
  btPlay      = document.querySelector('.rc-item.rc-play').addEventListener('click', consoleButton);
  btFwd30Sec  = document.querySelector('.rc-item.rc-forward30s').addEventListener('click', consoleButton);;
  btNav2End   = document.querySelector('.rc-item.rc-end').addEventListener('click', consoleButton);
  
  btRewind2x  = document.querySelector('.rc-item.rc-back2x').addEventListener('click', consoleButton);
  btVolume    = document.querySelector('.rc-item.rc-volume').addEventListener('click', consoleButton);
  btForward2x = document.querySelector('.rc-item.rc-forward2x').addEventListener('click', consoleButton);
  
  btSpare1    = document.querySelector('.rc-item.rc-s1').addEventListener('click', consoleButton);
  btSpare2    = document.querySelector('.rc-item.rc-s2').addEventListener('click', consoleButton);
});


