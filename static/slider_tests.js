// add Netflix Style Movie browsing w/ custom categories called moods
// simple POC



class Slider {
  constructor(name) {
    this.name = name;
    this.id = `glider-${name}`;
    this.items = [];
  }

  info(){
    console.log(`Slider - name: {this.name}`);
    console.log(`Slider - size: {this.items.length}`);
    console.log(`Slider - div ID: {this.id}`);
  }

  addItem(diplayItem){
    this.items.push(diplayItem);
  }

  //buildHTML(container, settings){
  buildHTML(visXStart, visXEnd, lazyY=true){
    //console.log(settings);
    let allGlidersContainer = document.getElementById("glider-supercontainer");

    let gliderContain = document.createElement('div');
    gliderContain.classList.add('glider-contain');

    let gliderHeading = document.createElement('div');
    gliderHeading.classList.add('slider-title');
    gliderHeading.id = `${this.id}-heading`;
    gliderHeading.textContent = this.name;
    gliderContain.appendChild(gliderHeading);

    let gliderDiv = document.createElement('div');
    gliderDiv.id = this.id;
    gliderDiv.classList.add('glider');
    gliderContain.appendChild(gliderDiv);

    allGlidersContainer.appendChild(gliderContain);

    //console.log(this.id);
    gliderDiv = document.getElementById(this.id);
    //console.log(gliderDiv);

    for (var i in this.items) {
      // lazy=false if in 'visible' window - visXStart >= here <= visXEnd
      gliderDiv.appendChild(this.createSliderElement(this.items[i], false));
    }
    //this.items.forEach(
    //  function (item, index) {
    //    let lazyX=true;
    //    if ((index >= visXStart) && (index <=visXEnd)) { lazyX=false; }
    //    gliderDiv.appendChild(this.createSliderElement(lazyX || lazyY)));
    //  }, this
    //);
  }

  //<div class='poster'>
  //  <image class='img-poster'
  //    src="{{ url_for('static', filename='covers/') }}{{movies[0]['hires_image']}}">
  //  </image>
  //</div>
  createSliderElement(i, lazy=true){
    // create basic container w/ image for (now
    let sDiv = document.createElement('div');
    sDiv.classList.add('glid-div-box','fit-box','opt-1');
    sDiv.id = i.id;

    if (!lazy) {
      if (i.hires_image.includes('movie_image_404.png')) {  // no image put text in

        let title = document.createElement('div');
        //title.textContent = `${i.id}<br>${i.title}<br>${i.root}`;
        //let volume = (i.root.replace('/Volumes/nfs/','').split('/'))[0];
        //title.innerHTML = `${i.id}<br>${i.title}<br>${volume}`;
        title.textContent = i.title;
        title.classList.add('mv-info');
        title.value = i.hires_image;
        sDiv.appendChild(title);

      } else { // image is good enough for (athousand words!

        //let image = document.createElement('picture');
        let image = document.createElement('img');
        let src = `/static/covers/${i.hires_image}`;
        image.src = src; // check for /static/covers/movie_image_404.png
        image.value = i.id;
        sDiv.appendChild(image);

      }
    }


    // button looks naff - don't bother
    //let sl_button = document.createElement('button');
    //sl_button.value = i.id;
    //sl_button.textContent = '+L';
    //sl_button.classList.add('bt-sl','btn','btn-secondary');
    //sDiv.appendChild(sl_button);

    //console.log(`createSliderElement ${i}`);

    //i.hires_image
    //let img = document.createElement('image');
    return sDiv;
  }

  addGlider(id){
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    // top ten slider
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    let qry = `#${id}`;
    window._ = new Glider(document.querySelector(qry), {
        slidesToShow: 4.3, //'auto',
        slidesToScroll: 4.3,
        itemWidth: 50,
        draggable: true,
        dragVelocity: 3.3,     // default 3.3
        scrollLock: false,   // set to false to turn off snap to movie
        dots: '#dots',
        rewind: true,
        //arrows: {
        //    prev: '.glider-prev',
        //    next: '.glider-next'
        //},
        responsive: [
            {
                breakpoint: 800,
                settings: {
                    slidesToScroll: 6.4,
                    slidesToShow: 6.4,
                    //slidesToScroll: 'auto',
                    //itemWidth: 162,
                    //slidesToShow: 'auto',
                    //exactWidth: true
                }
            },
            {
                breakpoint: 700,
                settings: {
                    slidesToScroll: 6.4,
                    slidesToShow: 6.4,
                    dots: false,
                    arrows: false,
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToScroll: 5.3,
                    slidesToShow: 5.3
                }
            },
            {
                breakpoint: 500,
                settings: {
                    slidesToScroll: 4.3,
                    slidesToShow: 4.3,
                    dots: false,
                    arrows: false,
                    scrollLock: true
                }
            }
        ]
    });
  }
}



var slider_info='Slider Info v0.0';
console.log(`RUNNING: ${slider_info}`);

// assign movie info to local parameter
console.log(`JS slider_tests.js movies[0]`);
console.log(movies[0]);

var slider_names = [];
var sliders = {};

// iterate movies, add new categories to slider names
// add movie id / index to sliders slider list
console.log(typeof(movies));
console.log(movies);

for (var m of movies) {
  //console.log(`* * * * * * ${slider_names.join(' - ')}`);
  //console.log(`${m.id} - ${m.genres}`);

  for (var g in m.genres) {
    const genre = m.genres[g];
    if ((genre === 'Adult') || (genre === 'News')){
      continue;   // TODO - genre comes from misclassified - 2010 (scifi) evaluate to Adult convention 2010
                  // empty and no image - messy in glider view
    }
    if (slider_names.includes(genre)) {
      //console.log(`${genre} in slider_names`);
      // add id to slider
      sliders[genre].addItem(m);       // add movie to relevant slider
    } else {
      slider_names.push(genre);       // create a new genre slider then add movie
      sliders[genre] = new Slider(genre);
      sliders[genre].addItem(m);
    }

  }
}

console.log(sliders);
console.log(prefsInfo);
console.log(prefsInfo.prefs_genre);
console.log(prefsInfo.prefs_genre.neg);
console.log(prefsInfo.prefs_genre.pos);

// put prefered genres at the top, rest in middle, negs at bottom . .
var pref_sliders = [];
slider_names.forEach(
  (genre) => {
    if (!((prefsInfo.prefs_genre.neg.includes(genre) || prefsInfo.prefs_genre.pos.includes(genre)))) {
      pref_sliders.push(genre);
    }
  }
);
pref_sliders.unshift(prefsInfo.prefs_genre.pos);
pref_sliders.push(prefsInfo.prefs_genre.neg);
slider_names = pref_sliders.flat();
console.log(pref_sliders);
console.log(slider_names);


//ts = new Slider('test-gen');
//ts.addItem(movies[0]);
//ts.addItem(movies[1]);
//ts.addItem(movies[3]);
//console.log(ts);
//
//var superCont = document.getElementById("glider-supercontainer");
//console.log(superCont);
//console.log(sliders[0]);
//sliders['Drama'].buildHTML();
//ts.buildHTML();

//
var visXStart = 0;
var visXEnd = 6;
var visYStart = 0;
var visYEnd = 3;

//for (s in sliders) {
//    console.log(`slider: ${s}`);
//    sliders[s].buildHTML(visXStart, visXEnd);
//}
slider_names.forEach(
  function (slider, index) {
    let lazyY=true;
    if ((index >= visYStart) && (index <=visYEnd)) { lazyY=false; }
    sliders[slider].buildHTML(visXStart, visXEnd, lazyY);
  }, this
);

// '#glider-Drama'

window.addEventListener('load',function(){
  document.querySelector('.glider').addEventListener('glider-slide-visible', function(event){
      var glider = Glider(this);
      //console.log('Slide Visible %s', event.detail.slide)
  });
  document.querySelector('.glider').addEventListener('glider-slide-hidden', function(event){
      //console.log('Slide Hidden %s', event.detail.slide)
  });
  document.querySelector('.glider').addEventListener('glider-refresh', function(event){
      //console.log('Refresh')
  });
  document.querySelector('.glider').addEventListener('glider-loaded', function(event){
      console.log('Loaded: glider-loaded')
  });


  for (s in sliders) {
      let div_id = sliders[s].id;
      //console.log(`addGlider: ${div_id} ${s}`);
      sliders[s].addGlider(div_id);
  }

});



//function sliderClickHandler(e) {
//  console.log("\n-\n-\n");
//  console.log(e);
//  console.log(e.target);
//  console.log(e.target.classList);
//  //console.log(e.target.parentNode.id);
//  //console.log(e.target.parentNode.classList);
//  console.log("\n-\n-\n");
//
//  if (Array.from(e.target.classList).includes('glid-div-box')) {
//    console.log(`slider click: ${e.target.id}`);
//  }
//}
//
//document.addEventListener('click', sliderClickHandler);
