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
  buildHTML(){
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

    console.log(this.id);
    gliderDiv = document.getElementById(this.id);
    console.log(gliderDiv);

    for (var i in this.items) {
      gliderDiv.appendChild(this.createSliderElement(this.items[i]));
    }


  }

  //<div class='poster'>
  //  <image class='img-poster'
  //    src="{{ url_for('static', filename='covers/') }}{{movies[0]['hires_image']}}">
  //  </image>
  //</div>
  createSliderElement(i){
    // create basic container w/ image for (now
    let sDiv = document.createElement('div');
    sDiv.classList.add('glid-div-box');
    sDiv.classList.add('fit-box');
    sDiv.classList.add('opt-1');

    //sDiv.textContent = `${i.id} - ${i.hires_image}`;
    console.log(`createSliderElement ${i}`);

    //let image = document.createElement('picture');
    let image = document.createElement('img');
    let src = `/static/covers/${i.hires_image}`;
    image.src = src;

    sDiv.appendChild(image);

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
  console.log(`* * * * * * ${slider_names.join(' - ')}`);
  console.log(`${m.id} - ${m.genres}`);

  for (var g in m.genres) {
    const genre = m.genres[g];

    if (slider_names.includes(genre)) {
      console.log(`${genre} in slider_names`);
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

for (s in sliders) {
    console.log(`slider: ${s}`);
    sliders[s].buildHTML();
}


// '#glider-Drama'

window.addEventListener('load',function(){
  document.querySelector('.glider').addEventListener('glider-slide-visible', function(event){
      var glider = Glider(this);
      console.log('Slide Visible %s', event.detail.slide)
  });
  document.querySelector('.glider').addEventListener('glider-slide-hidden', function(event){
      console.log('Slide Hidden %s', event.detail.slide)
  });
  document.querySelector('.glider').addEventListener('glider-refresh', function(event){
      console.log('Refresh')
  });
  document.querySelector('.glider').addEventListener('glider-loaded', function(event){
      console.log('Loaded')
  });


  for (s in sliders) {
      let div_id = sliders[s].id;
      console.log(`addGlider: ${div_id} ${s}`);
      sliders[s].addGlider(div_id);
  }

});
