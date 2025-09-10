from flask import Flask, render_template, request, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
from auth_token import client_id, client_secret
from torch import autocast
import os
from io import BytesIO
import base64
import urllib.parse
import urllib.request
import datalist
import twoimagelist
from functionCode import std_CompVis
from functionCode import std_tutorial
from functionCode import std_img_img
from functionCode import inpainting
from functionCode import open_pose
import json
from functionCode import testimage as tt
from natsort import natsorted

application = Flask(__name__)
application.config["RED"] = 0

std_list = []  # 전역 변수로 미리 정의해줍니다.
stdlength = 0
twofile_list = []
twolength = 0


def translate(text):
    encText = urllib.parse.quote(str(text))
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    req = urllib.request.Request(url, data=data.encode('utf-8'))
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(req)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        result = json.loads(response_body.decode('utf-8'))
        translated_text = result['message']['result']['translatedText']
        return translated_text
    else:
        print("Error Code:" + rescode)

# 메인 사이트 출력
@application.route("/", methods=['get'])
def home():
    std_list = datalist.load_list("all")
    std_list2 = twoimagelist.load_list("all")
    stdlength = len(std_list)
    stdlength2 = len(std_list2)
    twofile_list = ""
    two_list = ""
    twolength = len(twofile_list)
    twolength2 = len(two_list)
    data = request.args
    user = data.get('userid')
    stdname1 = data.get('stdname1')
    stdname2 = data.get('stdname2')
    if(stdname1 == "전체보기"):
        std_list = datalist.load_list("all")
        std_list2 = twoimagelist.load_list("all")
        stdlength = len(std_list)
        stdlength2 = len(std_list2)

    elif(stdname1 == "Text To Image"):
        std_list = datalist.load_list(stdname1)  # 이미지 리스트 불러오기
        stdlength = len(std_list)
        std_list2 = ""
        stdlength = len(std_list2)

    elif(stdname1 == "Img To Img"):
        std_list = datalist.load_list(stdname1)  # 이미지 리스트 불러오기
        stdlength = len(std_list)
        std_list2 = ""
        stdlength2 = len(std_list2)

    elif(stdname1 == "InPaint"):
        std_list2 = twoimagelist.load_list(stdname1)  # 이미지 리스트 불러오기
        stdlength2 = len(std_list)
        std_list = ""
        stdlength = len(std_list2)

    elif(stdname1 == "Pose"):
        std_list2 = twoimagelist.load_list(stdname1)  # 이미지 리스트 불러오기
        stdlength2 = len(std_list)
        std_list = ""
        stdlength = len(std_list2)
    if(user != ""):
        if(stdname2 == "전체보기"):
            twofile_list = datalist.user_load_list("all", user)
            two_list = twoimagelist.user_load_list("all", user)
            twolength = len(twofile_list)
            twolength2 = len(two_list)

        elif(stdname2 == "Text To Image"):
            twofile_list = datalist.user_load_list(
                stdname2, user)  # 이미지 리스트 불러오기
            twolength = len(twofile_list)
            two_list = ""
            twolength2 = len(two_list)

        elif(stdname2 == "Img To Img"):
            twofile_list = datalist.user_load_list(
                stdname2, user)  # 이미지 리스트 불러오기
            twolength = len(twofile_list)
            two_list = ""
            twolength2 = len(two_list)

        elif(stdname2 == "InPaint"):
            two_list = twoimagelist.user_load_list(
                stdname2, user)  # 이미지 리스트 불러오기
            twolength2 = len(twofile_list)
            twofile_list = ""
            twolength = len(two_list)

        elif(stdname2 == "Pose"):
            two_list = twoimagelist.user_load_list(
                stdname2, user)  # 이미지 리스트 불러오기
            twolength2 = len(twofile_list)
            twofile_list = ""
            twolength = len(two_list)
        response_data={"std_list":std_list, "std_list2":std_list2, "stdlength2":stdlength2, 
                  "stdlength":stdlength, "twofile_list":twofile_list, "two_list":two_list, "twolength2":twolength2, "twolength":twolength}
    return render_template("simple.html", std_list=std_list, std_list2=std_list2, stdlength2=stdlength2, stdlength=stdlength, twofile_list=twofile_list, two_list=two_list, twolength2=twolength2, twolength=twolength)
# 파일 업로드
@application.route("/upload_done", methods=["POST"])
def upload_done():
    uploaded_file = request.files.get("file")
    print(uploaded_file)
    if uploaded_file:
        file_path = f'static/uploaded/_{datalist.Now_idx()}.jpeg'
        uploaded_file.save(file_path)
        print(file_path)
        return jsonify({'success': True, 'image_path': file_path})
    else:
        return jsonify({'success': False, 'message': 'No image file provided'})

@application.route("/forinpaint_upload_done", methods=["POST"])
def forinpaint_upload_done():
    uploaded_file = request.files.get("file")
    print(uploaded_file)
    if uploaded_file:
        file_path = f'static/uploaded/inpaint_{twoimagelist.Now_idx()}.jpeg'
        uploaded_file.save(file_path)
        print("업로드 된 파일: ", file_path)
        return jsonify({'success': True, 'image_path': file_path})
    else:
        return jsonify({'success': False, 'message': 'No image file provided'})

@application.route("/pose_upload_done", methods=["POST"])
def pose_upload_done():
    uploaded_file = request.files.get("file")
    print(uploaded_file)
    if uploaded_file:
        file_path = f'static/uploaded/pose_{twoimagelist.Now_idx()}.jpeg'
        uploaded_file.save(file_path)
        print(file_path)
        return jsonify({'success': True, 'image_path': file_path})
    else:
        return jsonify({'success': False, 'message': 'No image file provided'})

# 정보 가져오기, 이미지 생성, 출력
@application.route("/open_result")
def result():
    image_url = request.args.get("image_url")
    return render_template('result.html', photo=image_url)

@application.route("/detail_info/<int:index>/")
def detail(index):
    d_info = datalist.load_std(index)[0]
    userid = d_info[1]
    stdname = d_info[2]
    pprompt = d_info[3]
    nprompt = d_info[4]
    filter = d_info[5]
    file = d_info[6]
    cfg = d_info[8]
    steps = d_info[9]
    noise = d_info[7]
    share = d_info[11]

    photo = f"img/{index}.jpeg"
    return render_template("detail_info.html", userid=userid, stdname=stdname, pprompt=pprompt, nprompt=nprompt, filter=filter, file=file, cfg=cfg, steps=steps, noise=noise, photo=photo, share=share)

@application.route("/detail_info2/<int:index>/")
def detail2(index):
    d_info = twoimagelist.load_std(index)[0]
    userid = d_info[1]
    stdname = d_info[2]
    pprompt = d_info[3]
    nprompt = d_info[4]
    filter = d_info[5]
    file1 = d_info[6]
    file2 = d_info[7]
    share=d_info[9]

    photo = "/"+d_info[8]
    return render_template("detail_info2.html", userid=userid, stdname=stdname, pprompt=pprompt, nprompt=nprompt, filter=filter, file1=file1, file2=file2, photo=photo, share=share)

@application.route("/search", methods=["get"])
def create_info():
    data = request.args
    user = data.get('user')
    stdname = data.get('stdname')
    share = data.get('share')
    pprompt = data.get("ptext")
    nprompt = data.get("ntext")
    filter = data.get("filter_num")
    cfg =data.get("cfg")
    steps =data.get("steps")
    ptranslated_text = translate(pprompt)
    ntranslated_text = translate(nprompt)

    situation = None

    # 필터랑 파일 데이터 처리
    if filter == "":
        print("필터를 입력해주세요")

    # 필터에 따른 생성모델로 이동
    if(filter == "CompVis"):
        std_CompVis.compvis(ptranslated_text, ntranslated_text, cfg, steps)
        situation = tt.test(ptranslated_text, ntranslated_text,
                            filter, "static/testimg/"+ptranslated_text+".jpeg")
    else:
        std_tutorial.stdv1_5(
            ptranslated_text, ntranslated_text, filter, cfg, steps)
        situation = tt.test(ptranslated_text, ntranslated_text,
                            filter, "static/testimg/"+ptranslated_text+".jpeg")

    if(situation == 0):
        image_path = f"static\img\{datalist.Now_idx()}.jpeg"  # 이미지 파일 경로
        image = Image.open(image_path)  # 이미지를 로드합니다.
        image_data = BytesIO()
        image.save(image_data, format='JPEG')
        encoded_image = base64.b64encode(image_data.getvalue()).decode("utf-8")

        # 이미지 URL 생성
        url_encoded_image = urllib.parse.quote(encoded_image)
        image_url = f"data:image/jpeg;base64,{url_encoded_image}"

        result_file = f"static/img/{datalist.Now_idx()}.jpeg"
        datalist.save(datalist.Now_idx(), user, stdname, pprompt,
                      nprompt, filter, "X", "X", cfg, steps, result_file, share)
        response_data = {"page": "/"}
        image_file = f"img/{datalist.Now_idx()-1}.jpeg"
        return jsonify(response_data=response_data, image_file=image_file)
    elif(situation == 1):
        error_response = {
        "error": "error",
        "page": f"/cant_create/1/?userid={user}&stdname={stdname}&pprompt={pprompt}&nprompt={nprompt}&filter={filter}&cfg={cfg}&steps={steps}&noise='X'"
        }
        return jsonify(error_response),400
    elif(situation == 2):
        error_response = {
        "error": "error",
        "page": f"/cant_create/2/?userid={user}&stdname={stdname}&pprompt={pprompt}&nprompt={nprompt}&filter={filter}&cfg={cfg}&steps={steps}&noise='X'"
        }
        return jsonify(error_response),400

@application.route('/change_image', methods=['POST'])
def change_image():
    situation = None
    user = request.form.get('user')
    stdname = request.form.get('stdname')
    share = request.form.get('share')
    image_prompt_text = request.form.get('image_prompt_text')
    image_nprompt_text = request.form.get('image_nprompt_text')
    filter = request.form.get('filter')
    cfg = request.form.get('cfg')
    steps = request.form.get('steps')
    noise = request.form.get('noise')

    ptranslated_text = translate(image_prompt_text)
    ntranslated_text = translate(image_nprompt_text)

    print("받아온 프롬프트 데이터 : ", image_prompt_text, image_nprompt_text)
    print("번역된 프롬프트 데이터 : ", ptranslated_text, ntranslated_text)

    used_image_path = f'static/useingImage/{datalist.Now_idx()}.jpg'
    std_img_img.img_to_img(ptranslated_text, ntranslated_text,
                           filter, used_image_path, cfg, steps, noise)
    situation = tt.test(ptranslated_text, ntranslated_text,
                        filter, "static/testimg/"+ptranslated_text+".jpeg")
    if(situation == 0):
        image_path = f"static\img\{datalist.Now_idx()}.jpeg"  # 이미지 파일 경로
        image = Image.open(image_path)  # 이미지를 로드합니다.
        image_data = BytesIO()
        image.save(image_data, format='JPEG')
        encoded_image = base64.b64encode(image_data.getvalue()).decode("utf-8")

        # 이미지 URL 생성
        url_encoded_image = urllib.parse.quote(encoded_image)
        image_url = f"static/img/{datalist.Now_idx()}.jpeg"
        datalist.save(datalist.Now_idx(), user, stdname, image_prompt_text,
                      image_prompt_text, filter, used_image_path, noise, cfg, steps, image_url, share)
        response_data = {"page": "/"}
        image_file = f"img/{datalist.Now_idx()-1}.jpeg"
        return jsonify(response_data=response_data, image_file=image_file)
    elif(situation == 1):
        error_response = {
        "error": "error",
        "page": f"/cant_create/1/?userid={user}&stdname={stdname}&pprompt={image_prompt_text}&nprompt={image_nprompt_text}&filter={filter}&cfg={cfg}&steps={steps}&noise={noise}"
        }
        return jsonify(error_response),400
    elif(situation == 2):
        error_response = {
        "error": "error",
        "page": f"/cant_create/2/?userid={user}&stdname={stdname}&pprompt={image_prompt_text}&nprompt={image_nprompt_text}&filter={filter}&cfg={cfg}&steps={steps}&noise={noise}"
        }
        return jsonify(error_response),400


@application.route('/inpainting_image', methods=['POST'])
def inpainting_image():
    user = request.form.get('user')
    stdname = request.form.get('stdname')
    share = request.form.get('share')
    image_prompt_text = request.form.get('image_prompt_text')
    image_nprompt_text = request.form.get('image_nprompt_text')
    f = request.form.get('filter')

    ptranslated_text = translate(image_prompt_text)
    ntranslated_text = translate(image_nprompt_text)

    print("받아온 프롬프트 데이터 : ", image_prompt_text, ", ", image_nprompt_text)
    print("번역된 프롬프트 데이터 : ", ptranslated_text, ", ", ntranslated_text)

    image_path = f'static/uploaded/inpaint_{twoimagelist.Now_idx()}.jpeg'
    mask_image_path = f'static/useingImage/mask_{twoimagelist.Now_idx()}.jpg'
    filter = f
    inpainting.in_painting(image_prompt_text, image_nprompt_text, ptranslated_text, ntranslated_text,
                           filter, image_path, mask_image_path, user, stdname, share)
    print("사진들: ", image_path, mask_image_path)
    response_data = {"prompt": ptranslated_text}
    image_file = f"in_painting/inpaint_{twoimagelist.Now_idx()-1}.jpeg"
    return jsonify(response_data=response_data, image_file=image_file)


@application.route('/openpose_image', methods=['get'])
def openpose_image():
    data = request.args
    user = data.get('user')
    stdname = data.get('stdname')
    share = data.get('share')
    pprompt = data.get("ptext")
    nprompt = data.get("ntext")
    filter = data.get("filter_num")

    ptranslated_text = translate(pprompt)
    ntranslated_text = translate(nprompt)

    print("받아온 프롬프트 데이터 : ", pprompt, ", ", nprompt)
    print("번역된 프롬프트 데이터 : ", ptranslated_text, ", ", ntranslated_text)
    image_path = f'static/uploaded/pose_{twoimagelist.Now_idx()}.jpeg'
    open_pose.openpose(pprompt, nprompt, ptranslated_text, ntranslated_text,
                       filter, image_path, user, stdname, share)
    print(filter)
    response_data = {"prompt": ptranslated_text}
    image_file = f"openpose/openpose_{twoimagelist.Now_idx()-1}.jpeg"
    return jsonify(response_data=response_data, image_file=image_file)


@application.route("/cant_create/<int:situation>/")
def fail(situation):
    red = application.config.get("RED", 0)
    userid=request.args.get("userid")
    stdname=request.args.get("stdname")
    pprompt = request.args.get("pprompt")
    nprompt = request.args.get("nprompt")
    filter = request.args.get("filter")
    cfg = request.args.get("cfg")
    steps = request.args.get("steps")
    noise = request.args.get("noise")
    if red == 10:
        situation = situation
        application.config["RED"] = 0
        return render_template("fail.html", index=situation, userid=userid, stdname=stdname, pprompt=pprompt, nprompt=nprompt, filter=filter, cfg=cfg, steps=steps, noise=noise)
    else:
        application.config["RED"] += 1
        situation = 3
        return render_template("fail.html", index=situation, userid=userid, stdname=stdname, pprompt=pprompt, nprompt=nprompt, filter=filter, cfg=cfg, steps=steps, noise=noise)


@application.route("/get_image", methods=['POST'])
def get_image():
    image_blob = request.data
    #print("받은 이미지 데이터 : " , image_blob)

    save_path = f'static/useingImage/{datalist.Now_idx()}.jpg'
    with open(save_path, 'wb') as f:
        f.write(image_blob)
        print("저장 완료")
    return 'Image received and saved successfully!'


@application.route("/get_mask_image", methods=['POST'])
def get_mask_image():
    image_blob = request.data
    #print("받은 이미지 데이터 : " , image_blob)

    save_path = f'static/useingImage/mask_{twoimagelist.Now_idx()}.jpg'
    with open(save_path, 'wb') as f:
        f.write(image_blob)
        print("저장 완료")
    return 'Image received and saved successfully!'


if __name__ == "__main__":
    application.run(host='0.0.0.0')
