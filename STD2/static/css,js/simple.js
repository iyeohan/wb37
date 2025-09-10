const downloadLink = document.createElement('a');
var startX, startY;
function stdname(){
    var user=document.getElementById('user').value;
    var stdname1=document.getElementById("stdname1").value;
    var stdname2=document.getElementById('stdname2').value;
    // 보낼 데이터를 객체로 생성
    var dataToSend = {
        userid:user,
        stdname1:stdname1,
        stdname2:stdname2
    };

    $.ajax({
        url: "/", // 데이터를 받아올 서버 엔드포인트 URL
        type: "get",
        data: dataToSend, // 데이터를 JSON 문자열로 변환하여 전송
        success: function(response) {
            $("#allbody").html(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function fileselect(){
    var file = document.getElementById("filename").files[0];
    var formData = new FormData();
    formData.append("file", file);

    $.ajax({
        url:"/upload_done",
        type:"POST",
        data: formData,
        contentType: false, // 필수: 기본값이 'application/x-www-form-urlencoded; charset=UTF-8'이므로 false로 설정
        processData: false, // 필수: 데이터를 변환하지 않도록 false로 설정
        success: function(response){
        var image_data=response.image_path;
        var canvas=document.getElementById('cnvs');
        canvas.innerHTML="";
        var context=canvas.getContext('2d');
        var img=new Image();
        // 이미지 로드가 완료되면 실행
        img.onload = function() {
            context.drawImage(img, 0, 0); // 이미지를 canvas에 그립니다.
        };

        img.src = image_data; // 이미지 로드 시작
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function twofile_select()
{
    var file1 = document.getElementById("filename1").files[0];
    document.getElementById("filename2").click();
    var file2 = document.getElementById("filename2").files[0];
    formData.append("file1",file1);
    formData.append("file2",file2);

    $.ajax({
        url:"/twofile_upload_done",
        type:"POST",
        data:formData,
        contentType:false,
        processData:false,
        success: function(response){
            var image_data1 = response.image_path
        }


    })

}

function fileselect3(){
    var file = document.getElementById("filename3").files[0];
    var formData = new FormData();
    formData.append("file", file);

    $.ajax({
        url:"/forinpaint_upload_done",
        type:"POST",
        data: formData,
        contentType: false, // 필수: 기본값이 'application/x-www-form-urlencoded; charset=UTF-8'이므로 false로 설정
        processData: false, // 필수: 데이터를 변환하지 않도록 false로 설정
        success: function(response){
        var image_data=response.image_path;
        var canvas=document.getElementById('backgroundCanvas');
        var context=canvas.getContext('2d');
        var img=new Image();
        img.src = image_data; // 이미지 로드 시작

        // 이미지 로드가 완료되면 실행
        img.onload = function() {
            context.drawImage(img, 0, 0); // 이미지를 canvas에 그립니다.
        };
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function fileselect4(){
    var file = document.getElementById("filename4").files[0];
    var formData = new FormData();
    formData.append("file", file);

    $.ajax({
        url:"/pose_upload_done",
        type:"POST",
        data: formData,
        contentType: false, // 필수: 기본값이 'application/x-www-form-urlencoded; charset=UTF-8'이므로 false로 설정
        processData: false, // 필수: 데이터를 변환하지 않도록 false로 설정
        success: function(response){
        var image_data=response.image_path;
        var pose=document.getElementById('poseimg');
        pose.src = image_data; // 이미지 로드
        },
        error: function(error) {
            console.log(error);
        }
    });
}
    
function selectfilter(popup,number){
    var filter
    if (popup=="1")
    {
        filter=document.getElementById("sfilter");
        if(number=="1") {text="CompVis";}
        else if(number=="2") {text="MajicMix";}
        else if(number=="3") {text="Ghibli1";}
        else if(number=="4") {text="MintReal";}
        else if(number=="5") {text="PastelMix";}
        else if(number=="6") {text="CetusMix";}
    }
    else if (popup=="2")
    {
        filter=document.getElementById("sfilter2");
        if(number=="1") {text="MajicMix";}
        else if(number=="2") {text="Ghibli1";}
        else if(number=="3") {text="MintReal";}
        else if(number=="4") {text="CetusMix";}
    }
    else if(popup=="3")
    {
        filter=document.getElementById("sfilter3"); 
        if(number=="1") {text="MajicMix";}
        else if(number=="2") {text="Ghibli1";}
        else if(number=="3") {text="PastelMix";}
        else if(number=="4") {text="MintReal";}
    }
    else if(popup=="4")
    {
        filter=document.getElementById("sfilter4");
        if(number=="1") {text="MajicMix";}
        else if(number=="2") {text="Ghibli1";}
        else if(number=="3") {text="MintReal";}
        else if(number=="4") {text="CetusMix";}
    }
    
    filter.setAttribute("value", text)
}

function generateImage() {
    event.preventDefault();
    var prompt=document.getElementById("p_text");
    $.ajax({
        url: "/search",
        type: "get",
        data: { ptext: prompt },
        success: function(response) {
            var image_data = response.image_data; // 서버에서 받아온 이미지 데이터
            // 이미지 소스를 설정하여 이미지를 표시
            var imgElement = document.createElement('generatedImage');
            imgElement.src = image_data;
            imgElement.width = 400;
            imgElement.height = 500;

            var imageBox = document.getElementById('Load_Image');
            imageBox.innerHTML = '';
            imageBox.appendChild(imgElement);
            //event.preventDefault();

        },
        error: function(error) {
            console.log(error);
        }
    });
}

/*결과 창, text-to-image*/
var resultwindow
var url
const beforeurl=[]

function openResult(image_url){
  url = '/open_result?image_url=' + image_url;
  resultwindow= window.open(url, '_blank', 'width=612, height=735');  
  $('#loading').hide();
  $('#circle1').hide();
  $('#popup1_filter').show();
  $('#cnvs').show();
  $('#popup2_filter').show();
  $('#popup2_buttons').show();
  $('#popup2_div').hide();
  $('#loading1').hide();
  $('#circle2').hide();
  $('#backgroundCanvas').show();
  $('#cnvs3').show();
  $('#popup3_filter').show();
  $('#popup3_buttons').show();
  $('#popup3_div').hide();
  $('#loading2').hide();
  $('#circle3').hide();
  $('#poseimg').show();
  $('#popup4_filter').show();
  $('#popup4_buttons').show();
  $('#popup4_div').hide();
  $('#loading3').hide();
  $('#circle4').hide();
  if (resultwindow) {
    beforeurl.unshift(resultwindow);
  }  
}

function closeResult(){
  if (beforeurl.length > 0) {
    var lastWindow = beforeurl.shift();
    lastWindow.close();
  }
}

function sendData(){
  var userid=document.getElementById('user').value
  var pp=document.getElementById("p_text").value
  var np=document.getElementById("n_text").value
  var f=document.getElementById("sfilter").value
  var tcfg = document.querySelector('select[id="tcfg"]').value;
  var tsteps=document.getElementById("tsteps").value;
  var toshare=document.getElementById('open')
  var tcshare=document.getElementById('close')
  var tshare
  // 체크된 상태인지 확인하고 값 가져오기
  if (toshare.checked) {
    tshare = "1";
    }
  if (tcshare.checked) {
    tshare = "0";
    }
  else{tshare="1"}
  // 보낼 데이터를 객체로 생성
  var dataToSend = {
      user:userid,
      share:tshare,
      stdname:"Text To Image",
      ptext: pp,
      ntext: np,
      filter_num: f,
      cfg:tcfg,
      steps:tsteps
  };

  $.ajax({
      url: "/search", // 데이터를 받아올 서버 엔드포인트 URL
      type: "get",
      data: dataToSend, // 데이터를 JSON 문자열로 변환하여 전송
      success: function(response) {
          // 서버 응답을 받은 후 실행할 함수를 여기에 작성합니다.
          // 예를 들어, 이미지를 렌더링하거나 다른 처리를 수행할 수 있습니다.
          document.getElementById("p_text").value=""
          document.getElementById("n_text").value=""
          document.getElementById("tcfg").selectedIndex=0
          document.getElementById("tsteps").value=30
          toshare.checked=false;                
          tcshare.checked=false;
          var filterbtns = document.querySelectorAll('.p1filterbtn'); // 모든 filterbtn 요소 선택
          filterbtns.forEach(function(btn) {
            // 모든 filterbtn 요소의 클래스 초기화
            filterbtns.forEach(function(btn) {
                btn.classList.remove('p1clicked');
            });
          });
          var image_url=response.image_file;
          closeResult();
          openResult(image_url);
      },
      error: function(error) {
        console.log("Ahh...")
        var page=error.responseJSON.page;
        window.location.href=page;
      }
  });
}

function createWithPose(){
    var userid=document.getElementById('user').value
    var pp=document.getElementById("pose_prompt").value
    var np=document.getElementById("pose_nprompt").value
    var f=document.getElementById("sfilter4").value
    var oshare=document.getElementById('open4')
    var cshare=document.getElementById('close4')
    var pshare
    // 체크된 상태인지 확인하고 값 가져오기
    if (oshare.checked) {
        pshare = "1";
      }
    if (cshare.checked) {
        pshare = "0";
      }
    else{cshare="1"}
    // 보낼 데이터를 객체로 생성
    var dataToSend = {
        user:userid,
        share:pshare,
        stdname:"Pose",
        ptext: pp,
        ntext: np,
        filter_num: f
    };

    $.ajax({
        url: "/openpose_image", // 데이터를 받아올 서버 엔드포인트 URL
        type: "get",
        data: dataToSend, // 데이터를 JSON 문자열로 변환하여 전송
        success: function(response) {
            // 서버 응답을 받은 후 실행할 함수를 여기에 작성합니다.
            // 예를 들어, 이미지를 렌더링하거나 다른 처리를 수행할 수 있습니다.
            document.getElementById("pose_prompt").value=""
            document.getElementById("pose_nprompt").value=""            
            oshare.checked=false;                
            cshare.checked=false;
            document.getElementById('poseimg').setAttribute("src","");
            document.getElementById('filename4').value="";
            var image_url=response.image_file;
            var filterbtns = document.querySelectorAll('.filterbtn'); // 모든 filterbtn 요소 선택
            filterbtns.forEach(function(btn) {
              // 모든 filterbtn 요소의 클래스 초기화
              filterbtns.forEach(function(btn) {
                  btn.classList.remove('clicked');
              });
            });
            closeResult();
            openResult(image_url);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

