img1 = document.getElementById('canvas-container-3')
img2 = document.getElementById('canvas-container-4')
result = document.getElementById('canvas-container-5')
var form1 = document.getElementById('form1-phasemag')
var form2 = document.getElementById('form2-phasemag')
var select = document.getElementById('select')
var cut= document.getElementById('cut')
var phase1mag2 = document.getElementById('phase1mag2')
var phase2mag1 = document.getElementById('phase2mag1')
var Delete= document.getElementById('Delete')


let isNowDrawing = false;
let rectArray = [[0,0],[0,0]];
let trArray = [[0,0],[0,0]];
let stageArray = [0,0,0,0];
let layerArray = [0,0,0,0];
let rect_flag_1 = 0;
let rect_flag_2 = 0;
let drawThreshold = 0;
let y = 0;
let stage1Active = 0;
let stage2Active = 0;
let stage_active = [];
let dim_to_send = [];

konvaInit('canvas-container-3',0);
konvaInit('canvas-container-4',1);
konvaInit('canvas-container',2);
konvaInit('canvas-container-2',3);

uploadImage(layerArray[2] , "#file_input" , 1);
uploadImage(layerArray[3] , "#file_input_2", 2);

// listen for the file input change event and load the image.
function uploadImage( layer , file_input , image)
{
    $(file_input).change(function(e)
    {
        var URL = window.webkitURL || window.URL;
        var url = URL.createObjectURL(e.target.files[0]);
        var img = new Image();

        img.src = url;

        img.onload = function() {
            var img_width = img.width;
            var img_height = img.height;

            // calculate dimensions to get max 369px
            var max = 369;
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
        var xhr = new XMLHttpRequest;
        if (image === 1) {
            fd.append("image1", e.target.files[0], "./image1");
            xhr.onreadystatechange = function ()
            {
                if (xhr.status == 200)
                {
                    send_img1();
                    send_result();
                    send_img2();
                }
            };
            xhr.open("POST", "/", true);
            xhr.send(fd);
            document.getElementById('options').classList.remove('hide');
        }
        if (image === 2)
        {
            fd.append("image2",e.target.files[0],"./image2");
            xhr.onreadystatechange = function()
            {
                if (xhr.status == 200)
                {
                    send_img2();
                    send_result();
                    send_img1();
                }
            };
            xhr.open( "POST", "/",true);
            xhr.send(fd);
            document.getElementById('options').classList.remove('hide');
        }
    });
}

function rectdown( x,flag ) {
  rectArray[x][flag] = new Konva.Rect({
    x: stageArray[x].getPointerPosition().x,
    y: stageArray[x].getPointerPosition().y,
    width: 0,
    height: 0,
    fill: "transparent",
    stroke: "red",
    strokeWidth: 2,
  });
  if (x === 0 )
  {
      dim_to_send[0] = stageArray[x].getPointerPosition().x;
      dim_to_send[1] = stageArray[x].getPointerPosition().y;
  }
  else
  {
      dim_to_send[4] = stageArray[x].getPointerPosition().x;
      dim_to_send[5] = stageArray[x].getPointerPosition().y;
  }
  layerArray[x].add(rectArray[x][flag]);
  layerArray[x].draw();
}

function rectMove(x,flag) {
  const newWidth = stageArray[x].getPointerPosition().x - rectArray[x][flag].x();
  const newHeight = stageArray[x].getPointerPosition().y - rectArray[x][flag].y();
  rectArray[x][flag].width(newWidth);
  rectArray[x][flag].height(newHeight);
}


//stageArray[0].on("mousedown", mousedownHandler(0));
stageArray[0].on("mousedown", function() { mousedownHandler(0); });
stageArray[0].on("mousemove", function() { mousemoveHandler(0); });
stageArray[0].on("mouseup", function() { mouseupHandler(0); });

//stageArray[0].on("mousedown", mousedownHandler(0));
stageArray[1].on("mousedown", function() { mousedownHandler(1); });
stageArray[1].on("mousemove", function() { mousemoveHandler(1); });
stageArray[1].on("mouseup", function() { mouseupHandler(1); });

function mousedownHandler(x)
{
    if (x===0)
    {
        if (rect_flag_1 < 1)
        {
            isNowDrawing = true;
            rectdown(x,rect_flag_1);
        }
    }
    else
    {
        if (rect_flag_2 < 1)
        {
            isNowDrawing = true;
            rectdown(x,rect_flag_2);
        }
    }
}

function mousemoveHandler(x)
{
    if (x===0) {
        if (rect_flag_1 < 1)
        {
            if (!isNowDrawing) return false;
            rectMove(x,rect_flag_1);
        }
    }
    else
    {
        if (rect_flag_2 < 1)
        {
            if (!isNowDrawing) return false;
            rectMove(x,rect_flag_2);
        }
    }
}

function mouseupHandler(x)
{
    if (x===0) {
        if (rect_flag_1 < 1)
        {
            isNowDrawing = false;
            transformer(x, rect_flag_1);
            rect_flag_1 = rect_flag_1 + 1;
            stage_active.push(1);
            dim_to_send[2] = rectArray[x][0].height();
            dim_to_send[3] = rectArray[x][0].width();
            console.log(dim_to_send);
            send_dim();
        }
            //send_dim();
        else
        {
            dim_to_send[0]=trArray[0][0].x();
            dim_to_send[1]=trArray[0][0].y();
            dim_to_send[2]=trArray[0][0].height();
            dim_to_send[3]=trArray[0][0].width();
            console.log(dim_to_send);
            send_dim();
        }
        // send_dim();
        // send_result();
    }
    else
    {
        if (rect_flag_2 < 1)
        {
            isNowDrawing = false;
            transformer(x,rect_flag_2);
            rect_flag_2 = rect_flag_2 + 1;
            stage_active.push(2);
            dim_to_send[6] = rectArray[x][0].height();
            dim_to_send[7] = rectArray[x][0].width();
            console.log(dim_to_send);
            send_dim();
            // send_result();
        }
        else
        {
            dim_to_send[4]=trArray[1][0].x();
            dim_to_send[5]=trArray[1][0].y();
            dim_to_send[6]=trArray[1][0].height();
            dim_to_send[7]=trArray[1][0].width();
            console.log(dim_to_send);
            send_dim();
        }
        // console.log(rectArray[1][0]);
        // console.log(trArray[1][0]);
        // stage2Active = 1;
        // send_dim();
        // send_result();
    }
    //send_dim();
    send_result();
    // await send_dim();
    // send_result();
}
function transformer(x,flag)
{
    let group = new Konva.Group({
        draggable: true,
    });
    layerArray[x].add(group);
    group.add(rectArray[x][flag]);
    trArray[x][flag] = new Konva.Transformer({
        node: group,
    });
    layerArray[x].add(trArray[x][flag]);
}

function konvaInit(container , x)
{
    stageArray[x] = new Konva.Stage({
        container: container,
        width: 369,
        height: 369
    });
    layerArray[x] = new Konva.Layer();
    stageArray[x].add(layerArray[x]);
    stageArray[x].draw();
}

function send_img1(){
    var img = new Image();
    // console.log('Image exists.')
    var timestamp = new Date().getTime();
    img = document.createElement("img");
    img.src = '/static/1.jpg?t='+ timestamp;
    // img.src = '/static/1.jpg';
    img.onload = function() {
      var img_width = img.width;
      var img_height = img.height;
      // calculate dimensions to get max 369 px
      var max = 369;
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
      layerArray[0].add(theImg);
      layerArray[0].draw();
      rect_flag_1 = 0;
    }
}
 function send_img2(){
    var img = new Image();
    var timestamp = new Date().getTime();
    img = document.createElement("img");
    img.src = '/static/2.jpg?t='+ timestamp;
    // img.src = '/static/2.jpg';
    img.onload = function() {
      var img_width = img.width;
      var img_height = img.height;

      // calculate dimensions to get max 369 px
      var max = 369;
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
      layerArray[1].add(theImg);
      layerArray[1].draw();
      rect_flag_2 = 0;
    }
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
  var fd2 = new FormData();
  var xhr = new XMLHttpRequest;
  fd2.append("phasemag",blob,"1");
  xhr.onreadystatechange = function() {
    if (xhr.status == 200) {
      send_img1();
      send_img2();
      send_result();
    }
  };
  xhr.open( "POST", "/",true);
  xhr.send(fd2);
  console.log('success');
});
form2.addEventListener("click",function(e){
  e.preventDefault();
  phase1mag2.value = "0";
  phase2mag1.value = "1";
  var send = [phase1mag2.value,phase2mag1.value];
  var blob = new Blob(send);
  var fd2 = new FormData();
  var xhr = new XMLHttpRequest;
  fd2.append("phasemag",blob,"2");
  xhr.onreadystatechange = function() {
    if (xhr.status == 200) {
      send_img1();
      send_img2();
      send_result();
    }
  };
  xhr.open( "POST", "/",true);
  xhr.send(fd2);
  console.log('success2');
});
select.addEventListener("click",function(e){
  e.preventDefault();
  select.value = "1";
  cut.value = "0";
  var send = [select.value,cut.value];
  var blob = new Blob(send);
  console.log(blob)
  var fd2 = new FormData();
  fd2.append("selectORcut",blob,"1");
  var xhr = new XMLHttpRequest;
  xhr.open( "POST", "/",false);
  xhr.send(fd2);
  send_dim();
  send_result();
});

function send_dim()
{
    const xhr = new XMLHttpRequest()
        var json =
            {
                data : dim_to_send
            }
    //}
  
    // open request
    xhr.open('POST', '/',async=false)
  
    // set `Content-Type` header
    xhr.setRequestHeader('Content-Type', 'application/json')
    console.log(JSON.stringify(json))
    // send rquest with JSON payload
    xhr.send(JSON.stringify(json))
};

cut.addEventListener("click",function(e){
  e.preventDefault();
  select.value = "0";
  cut.value = "1";
  var send = [select.value,cut.value];
  var blob = new Blob(send);
  var fd2 = new FormData();
  fd2.append("selectORcut",blob,"2");
  var xhr = new XMLHttpRequest;
  xhr.open( "POST", "/",false);
  xhr.send(fd2);
  send_dim();
  send_result();
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

function Deletee()
{
    if( stage_active[1] === 2 )
    {
        if (rect_flag_2 !== 0) {
            rectArray[1][rect_flag_2 - 1].destroy();
            trArray[1][rect_flag_2 - 1].destroy();
            rect_flag_2 = rect_flag_2 - 1;
            stage_active.pop();
        }
    }

    else if(stage_active[1] === 1 )
    {
        if (rect_flag_1 !== 0) {
            rectArray[0][rect_flag_1 - 1].destroy();
            trArray[0][rect_flag_1 - 1].destroy();
            rect_flag_1 = rect_flag_1 - 1;
            stage_active.pop();
        }
    }

    else if(stage_active[0] === 1 )
    {
        if (rect_flag_1 !== 0) {
            rectArray[0][rect_flag_1 - 1].destroy();
            trArray[0][rect_flag_1 - 1].destroy();
            rect_flag_1 = rect_flag_1 - 1;
            stage_active.pop();
        }
    }

    else if( stage_active[0] === 2 )
    {
        if (rect_flag_2 !== 0) {
            rectArray[1][rect_flag_2 - 1].destroy();
            trArray[1][rect_flag_2 - 1].destroy();
            rect_flag_2 = rect_flag_2 - 1;
            stage_active.pop();
        }
    }
    send_result();
}
Delete.addEventListener("click",function(e){
  e.preventDefault();
  Deletee();
});