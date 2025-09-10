$(document).ready(function(){    
    var cnvs = document.getElementById('cnvs3');
    var ctx = cnvs.getContext('2d');
    if (cnvs.getContext) {
        var isDraw = false;
        ctx.lineCap='round';
        ctx.lineJoin='round';
        var backgroundCanvas = document.getElementById('backgroundCanvas'); // 배경 이미지 캔버스
        var ctxBackground = backgroundCanvas.getContext('2d');
        var drawingCanvas = document.getElementById('cnvs3'); // 그림 캔버스
        var ctxDrawing = drawingCanvas.getContext('2d');

        /*// 배경 이미지 그리기
        var backgroundImage = new Image();
        backgroundImage.src = '/static/img/44.jpeg'; // 배경 이미지 파일 경로
        backgroundImage.onload = function() {
            ctxBackground.drawImage(backgroundImage, 0, 0);*/
    
        if (localStorage['imgData']) {
            var aData = new Array();
            aData = localStorage['imgData'].split('|');
            var imgData = ctxDrawing.createImageData(drawingCanvas.width, drawingCanvas.height);

            var j = 0;
            for (var i=0; i<imgData.data.length; i+=4) {
                imgData.data[i]    = aData[j+0]; 
                imgData.data[i+1] = aData[j+1]; 
                imgData.data[i+2] = aData[j+2];
                imgData.data[i+3] = 0xFF; 
                j += 3;
            }
            ctxDrawing.putImageData(imgData, 0, 0);
        // 이미지 초기화
        } 
        else {
            ctxDrawing.fillStyle = "white";
            ctxDrawing.fillRect(0, 0, drawingCanvas.width, drawingCanvas.height);
        }

        // 그림 그리기
        var dot = 1;
        var color = 'rgb(255, 255, 255)';

        function getCanvasCoordinates(event) {
            var cnvsRect = cnvs.getBoundingClientRect(); // 그림판 요소의 위치와 크기 정보
            var offsetX = event.clientX - cnvsRect.left; // 그림판 내에서의 X 좌표
            var offsetY = event.clientY - cnvsRect.top; // 그림판 내에서의 Y 좌표
            return { x: offsetX, y: offsetY };
        }

        function draw(e) {
            var currentColor = color; // 변경된 부분: color 변수 사용
            var currentPos = getCanvasCoordinates(e); // 그림판 내에서의 마우스 좌표
        
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(currentPos.x, currentPos.y);
            ctx.lineWidth = dot;
            ctx.strokeStyle = currentColor; // 변경된 부분: 현재 색상 적용
            ctx.stroke();
            ctx.closePath();
        
            startX = currentPos.x;
            startY = currentPos.y;
        
            if (currentPos.x < 0 || currentPos.y < 0 || currentPos.x > cnvs.width || currentPos.y > cnvs.height) {
                return 0;
            }
        }

        // 그리기 옵션

        // 그리기 옵션 - 도트크기
        $('#dot3').bind('change', function(){  dot = $('#dot3').val(); });
        // 그리기 옵션 - 색깔
        $('#color3').bind('change', function(){ color = $('#color3').val(); });

        // 이벤트 핸들러 연결
        $('#cnvs3').mousemove(function(e){
            // 그릴 수 있으면 그린다.
            if (isDraw) {
                draw(e);
            }      
        });

        $('#cnvs3').mouseleave(function(e){
            isDraw = false;
        });
        
        $('#cnvs3').mousedown(function(e){

            isDraw = true;
            var startPos = getCanvasCoordinates(e); // 그림 그리기 시작점 저장
            startX = startPos.x;
            startY = startPos.y;
        
        });
        
        $('#cnvs3').mouseup(function(e){
            // 버튼 up 이면 그릴 수 없다고 선언
            isDraw = false;   

        });

        

        function downloadCanvasImage(canvas, filename) {
            // 캔버스의 이미지를 데이터 URL로 변환
            var dataURL = canvas.toDataURL();
        
            // 캔버스의 이미지 데이터를 Blob 형태로 변환
            var blob = dataURLToBlob(dataURL);
        
            // a 태그를 생성하여 다운로드 링크로 사용
            var downloadLink = document.createElement('a');
            downloadLink.href = URL.createObjectURL(blob);
            downloadLink.download = 'canvas_image.png';
        
            // 링크를 클릭하여 이미지를 다운로드
            downloadLink.click();
        }

        /*//이미지 보내는 코드 
        function sendImageToServer() {
            var imageBlob = drawingCanvas.toBlob();
            var imagePromptText = document.getElementById('inpaint_prompt').value;
            var imagenPromptText=document.getElementById('inpaint_nprompt').value;
            var filter=document.getElementById("sfilter3")
        
            // FormData 객체를 생성하고 데이터를 추가합니다.
            var formData = new FormData();
            formData.append('image_data', imageBlob);
            formData.append('image_prompt', imagePromptText);
            formData.append('image_nprompt', imagenPromptText);
            formData.append('filter', filter);
        
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/inpainting_image', true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    // 서버로부터 받은 데이터를 처리하는 로직을 추가하세요
                } else if (xhr.readyState === XMLHttpRequest.DONE) {
                    // 에러 처리 로직을 추가하세요
                }
            };
            xhr.send(formData);
        }*/
        

        // 지우기
        function clearCanvas()
        {
            ctxDrawing.clearRect(0, 0, drawingCanvas.width, drawingCanvas.height);
            ctxDrawing.beginPath();

            localStorage.removeItem('imgData');
        }

        function setCanvasBackground(color) {
            ctxDrawing.fillStyle = color;
            ctxDrawing.fillRect(0, 0, drawingCanvas.width, drawingCanvas.height);
        }
        
        function saveCanvas() {
            var combinedCanvas = document.getElementById('cnvs3');

            // 이미지 파일로 변환
            var imageFile = combinedCanvas.toDataURL('image/jpeg');

            // 이미지 파일을 다운로드하거나 화면에 표시하는 등의 작업 수행
            var img = new Image();
            img.src = imageFile;
            document.body.appendChild(img);

            // Canvas를 이미지 파일로 변환하여 서버로 전송합니다.
            combinedCanvas.toBlob(function(blob) {
                // blob 데이터를 서버로 전송하거나 다른 용도로 사용할 수 있습니다.
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/get_mask_image', true);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                        //console.log(xhr.responseText);
                    }
                };
                xhr.send(blob);
            }, 'image/jpeg', 0.3);
        }


        // 전체지우기
        $('button[id="btnAllDel3"]').click(function(){
            clearCanvas();
        });
        
        var popup3= document.getElementById("popup3")
        var display=popup2.style.display;
        $('button[id="style_button3"]').click(function(){
            if(display==""){
            clearCanvas();};});

        // 저장하기
        $('button[id="btnSave3"]').click(function(){
            saveCanvas();
        });

        $('button[id="sendBtn3"]').click(function(){
            saveCanvas();
        });
    }

    // canvas 사용불가
    else { return;}
});
