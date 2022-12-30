img1 = document.getElementById('canvas-container-3')
img2 = document.getElementById('canvas-container-4')
result = document.getElementById('canvas-container-5')
var form1 = document.getElementById('form1')
var form2 = document.getElementById('form2')
var phase1mag2 = document.getElementById('phase1mag2')
var phase2mag1 = document.getElementById('phase2mag1')
let isNowDrawing = false;
let rectArray = [];
let rect_flag = 0;

// Create the stage and a layer to draw on.
var stage = new Konva.Stage({
  container: 'canvas-container',
  width: 500,
  height: 500
});

var layer = new Konva.Layer();
stage.add(layer);
stage.draw();

// listen for the file input change event and load the image.
$("#file_input").change(function(e){

    var URL = window.webkitURL || window.URL;
    var url = URL.createObjectURL(e.target.files[0]);
    var img = new Image();
    img.src = url;

    img.onload = function() {

      var img_width = img.width;
      var img_height = img.height;

      // calculate dimensions to get max 300px
      var max = 500;
      var ratio = (img_width > img_height ? (img_width / max) : (img_height / max))

      // now load the Konva image
      var theImg = new Konva.Image({
        image: img,
        x: 0,
        y: 0,
        width: img_width/ratio,
        height: img_height/ratio,
        draggable: false,
        rotation: 0
      });
      layer.add(theImg);
      layer.draw();
    }
    var fd = new FormData();
    fd.append("image1",e.target.files[0],"./image1");  
    var xhr = new XMLHttpRequest;
    xhr.onreadystatechange = function() {
      if (xhr.status == 200) {
        send_img1();
        send_result();    
      }
    };  
    xhr.open( "POST", "/",true);
    xhr.send(fd);
  });

function rectdown() {
  rect = new Konva.Rect({
    x: stage.getPointerPosition().x,
    y: stage.getPointerPosition().y,
    width: 0,
    height: 0,
    fill: "transparent",
    stroke: "red",
    strokeWidth: 2,
  });
  layer.add(rect);
  layer.draw();
  console.log(stage.getPointerPosition().x);
  console.log(stage.getPointerPosition().y);
}

function rectMove() {
  const newWidth = stage.getPointerPosition().x - rect.x();
  const newHeight = stage.getPointerPosition().y - rect.y();
  rect.width(newWidth);
  rect.height(newHeight);
}

stage.on("mousedown", mousedownHandler);
stage.on("mousemove", mousemoveHandler);
stage.on("mouseup", mouseupHandler);
function mousedownHandler() {
if (rect_flag < 2) {
  isNowDrawing = true;
  rectdown();
}
}

function mousemoveHandler() {
 if (rect_flag < 2) {
  if (!isNowDrawing) return false;
  rectMove();
 }
}

function mouseupHandler() {
if (rect_flag < 2) {
  isNowDrawing = false;
  rect_flag = rect_flag + 1;
  rectArray.push(rect);
  // console.log(rectArray);
  // console.log(rect.height());
  // console.log(rect.width());
}
  // let group = new Konva.Group({
  //   draggable: true,
  // });
  // layer.add(group);
  // for (i = 0; i < rectArray.length; i++) {
  //   const tr1 = new Konva.Transformer({
  //     node: rectArray[i],
  //   });
  //   group.add(tr1);
  //   layer.add(group);
  //   layer.add(tr1);
  // }
  // layer.draw();
}
stage.add(layer);

function move(){
  // let group = new Konva.Group({
  //   draggable: true,
  // });
  // layer.add(group);
  for (i = 0; i < rectArray.length ; i++) {
    let group = new Konva.Group({
    draggable: true,
    });
    // console.log(group.x());
    // console.log(group.y());
    layer.add(group);
    group.add(rectArray[i]);
    const tr1 = new Konva.Transformer({
      node: group,
    });
    //layer.add(group);
    layer.add(tr1);
  }
  layer.draw();
}

///////////////////////////////////////////

// Create the stage and a layer to draw on.
var stage_2 = new Konva.Stage({
  container: 'canvas-container-2',
  width: 500,
  height: 500
});

var layer_2 = new Konva.Layer();
stage_2.add(layer_2);
stage_2.draw();

// listen for the file input change event and load the image.
$("#file_input_2").change(function(e){
    var URL = window.webkitURL || window.URL;
    var url = URL.createObjectURL(e.target.files[0]);
    var img = new Image();

    img.src = url;

    img.onload = function() {
      var img_width = img.width;
      var img_height = img.height;

      // calculate dimensions to get max 300px
      var max = 500;
      var ratio = (img_width > img_height ? (img_width / max) : (img_height / max))

      // now load the Konva image
      var theImg = new Konva.Image({
        image: img,
        x: 0,
        y: 0,
        width: img_width/ratio,
        height: img_height/ratio,
        draggable: false,
        rotation: 0
      });

      layer_2.add(theImg);
      layer_2.draw();
    }
    var fd = new FormData();
    var xhr = new XMLHttpRequest;
    fd.append("image2",e.target.files[0],"./image2");
    xhr.onreadystatechange = function() {
      if (xhr.status == 200) {
        send_img2();
        send_result();    
      }
    };  
    xhr.open( "POST", "/",true);
    xhr.send(fd);
});

function delete_(){
  console.log(rect.position());
  //console.log(rectArray);
  rectArray.pop(rect);
  rect.destroy();
  //console.log(rectArray);
  layer.draw();
}

function send_img1(){
  checkIfImageExists('/static/1.jpg', (exists) => {
  if (exists) {
      console.log('Image exists.')
      var timestamp = new Date().getTime();
      img1_received = document.createElement("img");
      img1_received.src = '/static/1.jpg?t='+ timestamp;
      img1.innerHTML = " ";
      img1.appendChild(img1_received);
      console.log("sucessfully send"); 
  } else {
      console.log('Image does not exists.')
  }
});
}
function send_img2(){
  checkIfImageExists('/static/2.jpg', (exists) => {
  if (exists) {
      console.log('Image exists.')
      var timestamp = new Date().getTime();
      img2_received = document.createElement("img");
      img2_received.src = '/static/2.jpg?t='+ timestamp;
      img2.innerHTML = " ";
      img2.appendChild(img2_received);
      console.log("sucessfully send"); 
  } else {
      console.log('Image does not exists.')
  }
});
}
function send_result(){
  checkIfImageExists('/static/3.jpg', (exists) => {
  if (exists) {
      console.log('Image exists.')
      var timestamp = new Date().getTime();
      result_received = document.createElement("img");
      result_received.src = '/static/3.jpg?t='+ timestamp;
      result.innerHTML = " ";
      result.appendChild(result_received);
      console.log("sucessfully send"); 
  } else {
      console.log('Image does not exists.')
  }
});
}

form1.addEventListener("click",function(e){
  e.preventDefault();
  phase1mag2.value = "1";
  phase2mag1.value = "0";
  var send = [phase1mag2.value,phase2mag1.value];
  var blob = new Blob(send);
  console.log(blob)
  var fd = new FormData();
  fd.append("phasemag",blob,"1");  
  var xhr = new XMLHttpRequest;
  xhr.open( "POST", "/",true);
  xhr.send(fd);
});
form2.addEventListener("click",function(e){
  e.preventDefault();
  phase1mag2.value = "0";
  phase2mag1.value = "1";
  var send = [phase1mag2.value,phase2mag1.value];
  var blob = new Blob(send);
  var fd = new FormData();
  fd.append("phasemag",blob,"2");  
  var xhr = new XMLHttpRequest;
  xhr.open( "POST", "/",true);
  xhr.send(fd);
});
function checkIfImageExists(url, callback) {
  const img = new Image();
  img.src = url;
  if (img.complete) {
      callback(true);
  } else {
      img.onload = () => {
      callback(true);
  };
      img.onerror = () => {
      callback(false);
      };
  }
}


