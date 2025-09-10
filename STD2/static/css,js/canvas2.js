
$(document).ready(function(){    
    var cnvs = document.getElementById('cnvs');
    var ctx = cnvs.getContext('2d');
    if (cnvs.getContext) {
        var isDraw = false;
        ctx.lineCap='round';
        ctx.lineJoin='round';
    
        if (localStorage['imgData']) {
            var aData = new Array();
            aData = localStorage['imgData'].split('|');
            var imgData = ctx.createImageData(cnvs.width, cnvs.height);

            var j = 0;
            for (var i=0; i<imgData.data.length; i+=4) {
                imgData.data[i]    = aData[j+0]; 
                imgData.data[i+1] = aData[j+1]; 
                imgData.data[i+2] = aData[j+2];
                imgData.data[i+3] = 0xFF; 
                j += 3;
            }
            ctx.putImageData(imgData, 0, 0);
        // 이미지 초기화
        } 
        else {
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, cnvs.width, cnvs.height);
        }

        // 그리기 옵션
        var dot = 1;
        var color = 'rgb(0, 0, 0)';

        // 그리기 옵션 - 도트크기
        $('#dot').bind('change', function(){  dot = $('#dot').val(); });
        // 그리기 옵션 - 색깔
        $('#color').bind('change', function(){ color = $('#color').val(); });

        // 이벤트 핸들러 연결
        $('#cnvs').mousemove(function(e){
            // 그릴 수 있으면 그린다.
            if (isDraw) {
                draw(e);
            }        
        });

        $('#cnvs').mouseleave(function(e){
            isDraw = false;
        });
        
        $('#cnvs').mousedown(function(e){
            // 왼쪽 버튼 down 이면 그릴 수 있다고 선언
            isDraw = true;
            var startPos = getCanvasCoordinates(e); // 그림 그리기 시작점 저장
            startX = startPos.x;
            startY = startPos.y;
        });
        
        $('#cnvs').mouseup(function(e){
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

        // //이미지 보내는 코드 
        // function sendImageToServer() {
        //     var imageBlob = cnvs.toBlob();
        //     var imagePromptText = document.getElementById('image_prompt_text').value;
        //     var cfg = document.querySelector('select[name="icfg"]').value;
        //     var steps=document.getElementById("isteps").value;
        //     var noise=document.getElementById("noise_strength").value;
        
        //     // FormData 객체를 생성하고 데이터를 추가합니다.
        //     var formData = new FormData();
        //     formData.append('image_data', imageBlob);
        //     formData.append('image_prompt', imagePromptText);
        //     formData.append('cfg', cfg);
        //     formData.append('steps', steps);
        //     formData.append('noise', noise);
        
        //     var xhr = new XMLHttpRequest();
        //     xhr.open('POST', '/change_image', true);
        //     xhr.onreadystatechange = function () {
        //         if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
        //             var response = JSON.parse(xhr.responseText);
        //             // 서버로부터 받은 데이터를 처리하는 로직을 추가하세요
        //         } else if (xhr.readyState === XMLHttpRequest.DONE) {
        //             // 에러 처리 로직을 추가하세요
        //         }
        //     };
        //     xhr.send(formData);
        // }

        // 그리기
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

        // 지우기
        function clearCanvas()
        {
            ctx.clearRect(0, 0, cnvs.width, cnvs.height);
            ctx.beginPath();

            localStorage.removeItem('imgData');
        }

        function setCanvasBackground(color) {
            ctx.fillStyle = color;
            ctx.fillRect(0, 0, cnvs.width, cnvs.height);
        }
        
        function saveCanvas() {
            // 그렸던 그림을 이미지 데이터로 저장
            var imgData = ctx.getImageData(0, 0, cnvs.width, cnvs.height);
            var aData = new Array();

            for (var i = 0; i < imgData.data.length; i += 4) {
                aData.push(imgData.data[i]);
                aData.push(imgData.data[i + 1]);
                aData.push(imgData.data[i + 2]);
                // 알파 채널도 저장합니다.
                aData.push(imgData.data[i + 3]);
            }

            localStorage['imgData'] = aData.join('|');

            // 흰 배경으로 설정
            setCanvasBackground('#FFFFFF');

            // 저장된 그림을 다시 그립니다.
            var savedImgData = localStorage['imgData'];
            if (savedImgData) {
                savedImgData = savedImgData.split('|');
                var pixelIndex = 0;
                for (var y = 0; y < cnvs.height; y++) {
                    for (var x = 0; x < cnvs.width; x++) {
                        var r = parseInt(savedImgData[pixelIndex++]);
                        var g = parseInt(savedImgData[pixelIndex++]);
                        var b = parseInt(savedImgData[pixelIndex++]);
                        var a = parseInt(savedImgData[pixelIndex++]);
                        var rgbaColor = `rgba(${r},${g},${b},${a})`;

                        // 이미지 데이터를 다시 그림
                        ctx.fillStyle = rgbaColor;
                        ctx.fillRect(x, y, 1, 1);
                    }
                }
            }

            // Canvas를 이미지 파일로 변환하여 서버로 전송합니다.
            cnvs.toBlob(function (blob) {
                // blob 데이터를 서버로 전송하거나 다른 용도로 사용할 수 있습니다.

                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/get_image', true);
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                        //console.log(xhr.responseText);
                    }
                };
                xhr.send(blob);
            }, 'image/jpeg',0.3);
        }


        // 전체지우기
        $('button[id="btnAllDel"]').click(function(){
            clearCanvas();
        });
        
        var popup2= document.getElementById("popup2")
        var display=popup2.style.display;
        $('button[id="style_button2"]').click(function(){
            if(display==""){
            clearCanvas();};});

        // 저장하기
        $('button[id="btnSave"]').click(function(){
            saveCanvas();
        });

        $('button[id="sendBtn"]').click(function(){
            saveCanvas();
        });
    }

    // canvas 사용불가
    else { return;}
});
