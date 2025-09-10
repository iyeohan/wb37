/*text-to-img*/
function popupShow(){
    $(".popup").show();
    /*버튼 효과*/
    const btn = document.getElementById('style_button1')
        
    const onClick = d => {
        const { x, y, width, height} = btn.getBoundingClientRect()
        const radius = Math.sqrt(width * width + height * height)
        btn.style.setProperty('--diameter', radius * 2 + 'px')
        const { clientX, clientY } = d
        const left = (clientX - x - radius) / width * 100 + '%'
        const top = (clientY - y - radius) / height * 100 + '%'
    
        btn.style.setProperty('--left', left)
        btn.style.setProperty('--top', top)
        btn.style.setProperty('--a', '')
        setTimeout(() => {
            btn.style.setProperty('--a', 'ripple-effect 500ms linear')
        }, 5)
    }    
    btn.addEventListener('click', onClick)
    
    const sendBtn = document.getElementById('sendBtn');
    var checkbox1=document.getElementById('open')
    var checkbox2=document.getElementById('close')
    checkbox1.addEventListener("change", function() {
        if (checkbox1.checked) {
            checkbox2.checked = false; // 체크박스 2의 체크를 해제
        }
    });

    checkbox2.addEventListener("change", function() {
        if (checkbox2.checked) {
            checkbox1.checked = false; // 체크박스 1의 체크를 해제
        }
    });

    var filterbtns = document.querySelectorAll('.p1filterbtn'); // 모든 filterbtn 요소 선택
    
    filterbtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            // 모든 filterbtn 요소의 클래스 초기화
            filterbtns.forEach(function(btn) {
                btn.classList.remove('p1clicked');
            });

            // 현재 클릭한 요소에만 클래스 추가
            this.classList.add('p1clicked');
        });
    });
    popupShutdown2();
    popupShutdown3();
    popupShutdown4();
}
function popupShutdown(){
  $(".popup").hide();
}

/*img-to-img*/
function popupShow2(){
  $(".popup2").show();    
  /*버튼 효과*/
  var imagePromptInput = document.getElementById('prompt');
  var imageNPromptInput= document.getElementById('nprompt');
  var ifilter=document.getElementById("sfilter2");
  var icfg=document.querySelector('select[id="icfg"]');
  var isteps=document.getElementById("isteps");
  var inoise=document.getElementById("noise");
  const btn2 = document.getElementById('style_button2');

  
  const onClick2 = d => {
      const { x, y, width, height} = btn2.getBoundingClientRect();
      const radius = Math.sqrt(width * width + height * height);
      btn2.style.setProperty('--diameter', radius * 2 + 'px');
      const { clientX, clientY } = d;
      const left = (clientX - x - radius) / width * 100 + '%';
      const top = (clientY - y - radius) / height * 100 + '%';
  
      btn2.style.setProperty('--left', left);
      btn2.style.setProperty('--top', top);
      btn2.style.setProperty('--a', '');
      setTimeout(() => {
          btn2.style.setProperty('--a', 'ripple-effect 500ms linear');
      }, 5);
  }
  btn2.addEventListener('click', onClick2);

  var userid=document.getElementById('user');
  var canvas = document.getElementById('cnvs');

  var checkbox3=document.getElementById("open2")
  var checkbox4=document.getElementById('close2')
  checkbox3.addEventListener("change", function() {
      if (checkbox3.checked) {
          checkbox4.checked = false; // 체크박스 2의 체크를 해제
      }
  });
  
  checkbox4.addEventListener("change", function() {
      if (checkbox4.checked) {
          checkbox3.checked = false; // 체크박스 1의 체크를 해제
      }
  });
  
  var filterbtns = document.querySelectorAll('.filterbtn'); // 모든 filterbtn 요소 선택
  
  filterbtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
          // 모든 filterbtn 요소의 클래스 초기화
          filterbtns.forEach(function(btn) {
              btn.classList.remove('clicked');
          });

          // 현재 클릭한 요소에만 클래스 추가
          this.classList.add('clicked');
      });
  });
  /*canvas 그림 보내기*/
  const sendBtn = document.getElementById('sendBtn');
  var oshare=document.getElementById('open2')
  var cshare=document.getElementById('close2')
  var ishare
  // 체크된 상태인지 확인하고 값 가져오기
  if (oshare.checked) {
    ishare = "1";
    }
  if (cshare.checked) {
    ishare = "0";
    }

  else{ishare="1"}
  sendBtn.addEventListener('click', function () {
      const id=userid.value;
      const stdname="Img To Img"
      const share=ishare;
      const imagePromptText = imagePromptInput.value;
      const imageNPromptText=imageNPromptInput.value;
      const cfg=icfg.value;
      const steps=isteps.value;
      const noise=inoise.value;
      const filter=ifilter.value;

      canvas.toBlob(function (blob) {
          const formData = new FormData();
          formData.append('user', id);
          formData.append('stdname', stdname);
          formData.append('share', share)
          formData.append('image_prompt_text', imagePromptText);
          formData.append('image_nprompt_text', imageNPromptText);
          formData.append('filter', filter);
          formData.append('cfg', cfg);
          formData.append('steps',steps);
          formData.append('noise', noise);

          const xhr = new XMLHttpRequest();
          xhr.open('POST', '/change_image', true);
          xhr.onreadystatechange = function () {
              if (xhr.readyState === XMLHttpRequest.DONE) {
                if(xhr.status === 200){
                  //console.log(xhr.responseText)
                  imagePromptInput.value=""
                  imageNPromptInput.value=""
                  document.getElementById("icfg").selectedIndex=0
                  document.getElementById('filename').value="";
                  isteps.value=50
                  inoise.value=0.4
                  checkbox3.checked=false;                
                  checkbox4.checked=false;
                  clearCanvas('cnvs');
                  var filterbtns = document.querySelectorAll('.filterbtn'); // 모든 filterbtn 요소 선택
                  filterbtns.forEach(function(btn) {
                    // 모든 filterbtn 요소의 클래스 초기화
                    filterbtns.forEach(function(btn) {
                        btn.classList.remove('clicked');
                    });
                  });
                  var response = JSON.parse(xhr.responseText); // Parse the response
                  var image_url=response.image_file;
                  closeResult();
                  openResult(image_url);
                }
                else {
                  // 오류 응답 처리
                  console.log("Ahh...")
                  var page = JSON.parse(xhr.responseText).page;
                  window.location.href = page;
                }
              }
          };
          xhr.send(formData);
      }, 'image/png');
  });

  popupShutdown();            
  popupShutdown3();
  popupShutdown4();
}
function popupShutdown2(){
  $(".popup2").hide();
}

/*InPainting*/
function popupShow3(){
  $(".popup3").show();
  /*버튼 효과*/
  const btn3 = document.getElementById('style_button3');

  const onClick3 = d => {
      const { x, y, width, height} = btn3.getBoundingClientRect();
      const radius = Math.sqrt(width * width + height * height);
      btn3.style.setProperty('--diameter', radius * 2 + 'px');
      const { clientX, clientY } = d;
      const left = (clientX - x - radius) / width * 100 + '%';
      const top = (clientY - y - radius) / height * 100 + '%';

      btn3.style.setProperty('--left', left);
      btn3.style.setProperty('--top', top);
      btn3.style.setProperty('--a', '');
      setTimeout(() => {
          btn3.style.setProperty('--a', 'ripple-effect 500ms linear');
      }, 5);
  }

  btn3.addEventListener('click', onClick3);

  var checkbox5=document.getElementById("open3")
  var checkbox6=document.getElementById('close3')
  checkbox5.addEventListener("change", function() {
      if (checkbox5.checked) {
          checkbox6.checked = false; // 체크박스 2의 체크를 해제
      }
  });
  
  checkbox6.addEventListener("change", function() {
      if (checkbox6.checked) {
          checkbox5.checked = false; // 체크박스 1의 체크를 해제
      }
  });

  var filterbtns = document.querySelectorAll('.filterbtn'); // 모든 filterbtn 요소 선택
  
  filterbtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
          // 모든 filterbtn 요소의 클래스 초기화
          filterbtns.forEach(function(btn) {
              btn.classList.remove('clicked');
          });

          // 현재 클릭한 요소에만 클래스 추가
          this.classList.add('clicked');
      });
  });
  /*canvas 그림 보내기*/  
  var userid=document.getElementById('user');
  var canvas = document.getElementById('cnvs3');
  var imagePromptInput = document.getElementById('inpaint_prompt');
  var imageNPromptInput=document.getElementById('inpaint_nprompt');
  var filter=document.getElementById("sfilter3");
  const sendBtn3 = document.getElementById('sendBtn3');
  var oshare=document.getElementById('open3')
  var cshare=document.getElementById('close3')
  var inshare
  // 체크된 상태인지 확인하고 값 가져오기
  if (oshare.checked) {
    inshare = "1";
    }
  if (cshare.checked) {
    inshare = "0";
    }
  else{inshare="1"}
  
  sendBtn3.addEventListener('click', function () {
      const id=userid.value;
      const stdname="InPaint"
      const share=inshare;

      canvas.toBlob(function (blob) {
          const formData = new FormData();
          formData.append('user', id);
          formData.append('stdname', stdname);
          formData.append('share', share)
          formData.append('image_prompt_text', imagePromptInput.value);
          formData.append('image_nprompt_text', imageNPromptInput.value);
          formData.append('filter', filter.value);
  
          const xhr = new XMLHttpRequest();
          xhr.open('POST', '/inpainting_image', true);
          xhr.onreadystatechange = function () {
              if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                //console.log(xhr.responseText)
                imagePromptInput.value=""
                imageNPromptInput.value=""
                checkbox5.checked=false;                
                checkbox6.checked=false;
                document.getElementById('filename3').value="";
                var response = JSON.parse(xhr.responseText); // Parse the response
                var image_url=response.image_file;
                clearCanvas('backgroundCanvas');
                clearCanvas('cnvs3');
                var filterbtns = document.querySelectorAll('.filterbtn'); // 모든 filterbtn 요소 선택
                filterbtns.forEach(function(btn) {
                  // 모든 filterbtn 요소의 클래스 초기화
                  filterbtns.forEach(function(btn) {
                      btn.classList.remove('clicked');
                  });
                });
                closeResult();
                openResult(image_url);
              }
          };
          xhr.send(formData);
      }, 'image/png');
  });
  
  popupShutdown();
  popupShutdown2();
  popupShutdown4();
}
function popupShutdown3(){
  $(".popup3").hide();
}
  
/*Open Pose*/
function popupShow4(){
  $(".popup4").show();
  /*버튼 효과*/
  const btn4 = document.getElementById('style_button4');

  const onClick4 = d => {
    const { x, y, width, height} = btn4.getBoundingClientRect();
    const radius = Math.sqrt(width * width + height * height);
    btn4.style.setProperty('--diameter', radius * 2 + 'px');
    const { clientX, clientY } = d;
    const left = (clientX - x - radius) / width * 100 + '%';
    const top = (clientY - y - radius) / height * 100 + '%';

    btn4.style.setProperty('--left', left);
    btn4.style.setProperty('--top', top);
    btn4.style.setProperty('--a', '');
    setTimeout(() => {
      btn4.style.setProperty('--a', 'ripple-effect 500ms linear');
    }, 5);
  }

  btn4.addEventListener('click', onClick4);

  var checkbox7=document.getElementById("open4")
  var checkbox8=document.getElementById('close4')
  checkbox7.addEventListener("change", function() {
      if (checkbox7.checked) {
          checkbox8.checked = false; // 체크박스 2의 체크를 해제
      }
  });
  
  checkbox8.addEventListener("change", function() {
      if (checkbox8.checked) {
          checkbox7.checked = false; // 체크박스 1의 체크를 해제
      }
  });

  var filterbtns = document.querySelectorAll('.filterbtn'); // 모든 filterbtn 요소 선택

  filterbtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
          // 모든 filterbtn 요소의 클래스 초기화
          filterbtns.forEach(function(btn) {
              btn.classList.remove('clicked');
          });

          // 현재 클릭한 요소에만 클래스 추가
          this.classList.add('clicked');
      });
  });
  popupShutdown();
  popupShutdown3();
  popupShutdown2();
}
function popupShutdown4(){
  $(".popup4").hide();
}


function clearCanvas(canvas)
{
    var cnvs = document.getElementById(canvas);
    var ctx = cnvs.getContext('2d');
    ctx.clearRect(0, 0, cnvs.width, cnvs.height);
    ctx.beginPath();

    localStorage.removeItem('imgData');
}