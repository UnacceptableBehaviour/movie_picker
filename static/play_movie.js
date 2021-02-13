var movie_display_name='movie odyssey v0.0';
console.log(`RUNNING: ${movie_display_name}`);

// assign movie info to local parameter
console.log(`JS movie local ${movie['title']} - ${movie['genres']} - inline`); 

// register each remote button to a function thot console parameters to send to server

var btNav2Start, btBack30Sec, btPlay, btFwd30Sec, btNav2End, btRewind2x;
var btVolume, btForward2x, btSpare1, btSpare2;   

const ST_PAUSED = 10;
const ST_PLAYING = 20;
const ST_FF2X = 30;
const ST_RR2X = 40;

var Remote = {};
Remote.state = ST_PAUSED;

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
    console.log('func: button PLAY');    
  } else if (Remote.state === ST_PLAYING) {
    Remote.state = ST_PAUSED ;
    console.log('func: button PAUSED');        
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

document.addEventListener("DOMContentLoaded", function(event) {
  btNav2Start = document.querySelector('.rc-item.rc-start');  
  btBack30Sec = document.querySelector('.rc-item.rc-back30s');
  btPlay      = document.querySelector('.rc-item.rc-play');
  btFwd30Sec  = document.querySelector('.rc-item.rc-forward30s');
  btNav2End   = document.querySelector('.rc-item.rc-end');
  
  btRewind2x  = document.querySelector('.rc-item.rc-back2x');
  btVolume    = document.querySelector('.rc-item.rc-volume');
  btForward2x = document.querySelector('.rc-item.rc-forward2x');
  
  btSpare1    = document.querySelector('.rc-item.rc-s1');
  btSpare2    = document.querySelector('.rc-item.rc-s2');

  btNav2Start.addEventListener('click', consoleButton);
  btBack30Sec.addEventListener('click', consoleButton);
  btPlay.addEventListener('click', consoleButton);
  btFwd30Sec.addEventListener('click', consoleButton);
  btNav2End.addEventListener('click', consoleButton);
  
  btRewind2x.addEventListener('click', consoleButton);
  btVolume.addEventListener('click', consoleButton);
  btForward2x.addEventListener('click', consoleButton);
  
  btSpare1.addEventListener('click', consoleButton);
  btSpare2.addEventListener('click', consoleButton);  
});




//switch (button_id){
//  case 'rcbt-start':
//    break;
//  case 'rcbt-bak30s':
//    break;
//  case 'rcbt-play':
//    break;
//  case 'rcbt-fwd30s':
//    break;
//  case 'rcbt-end':
//    break;
//  case 'rcbt-bak2x':
//    break;
//  case 'rcbt-vol':
//    break;
//  case 'rcslid-vol':
//    break;
//  case 'rcbt-fwd2x':
//    break;
//  case 'rcbt-s1':
//    break;
//  case 'rcbt-s2':
//    break;
//  default: 
//    consoleButton.log("ERROR!");
//}
