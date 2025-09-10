import torch
import cv2
from PIL import Image
import os
from torch import autocast
from diffusers import ControlNetModel
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import StableDiffusionControlNetPipeline
from diffusers import EulerAncestralDiscreteScheduler
from diffusers import UniPCMultistepScheduler
from diffusers import AutoencoderKL
from RealESRGAN import RealESRGAN
from controlnet_aux import OpenposeDetector
import twoimagelist

device = "cuda"
model_id_or_path = "runwayml/stable-diffusion-v1-5"
ckpt_path = r"Stable-diffusion\cetusMix_Whalefall2.safetensors"

vae_repo = "redstonehero/kl-f8-anime2"
ckpt_repo = "lllyasviel/sd-controlnet-openpose"


def openpose(kpp, knp, pp, np, filter, poseimg_path, user, stdname, share):
    prompt = pp +", (masterpiece:1.0), (best quality:1.4), (ultra highres:1.2), (photorealistic:1.4), (8k, RAW photo:1.2), (soft focus:1.4)"
    
    negative_prompt = np+", badhandv4,(worst quality:1.6),(low quality:1.6), (normal quality:2),  easynegative"
    if filter == "MintReal":
        ckpt_path = r"Stable-diffusion\MintReal_diffuser"
        vae_repo = "lint/anime_vae"
    elif filter == "Ghibli1":
        ckpt_path = "nitrosocke/Ghibli-Diffusion"
        vae_repo = "lint/anime_vae"
    elif filter == "CetusMix":
        ckpt_path = r"Stable-diffusion\cetusMix_diffuser"
        vae_repo = "redstonehero/kl-f8-anime2"
    elif filter == "MajicMix":
        ckpt_path = r"Stable-diffusion\majicmix_diffuser"
        vae_repo = "lint/anime_vae"
    # -------------------high res.fix-----------------------------
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        ckpt_path, num_hidden_layers=11, torch_dtype=torch.float16)
    pipe.safety_checker = None
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
        pipe.scheduler.config)
    pipe.load_textual_inversion(r"function\EasyNegative.safetensors")
    pipe.load_textual_inversion(r"function\badhandv4.pt")
    pipe = pipe.to('cuda')
    model = RealESRGAN('cuda', scale=2)
    model.load_weights('weights/RealESRGAN_x4plus_anime_6B.pth')
    image = Image.open(poseimg_path).convert("RGB")
    init_image = image.resize((512, 512))
    sr_image = model.predict(image)
    sr_image = sr_image.resize((512, 512))
    sr_image.save('up_image.png')

    with autocast("cuda"):
        image = pipe(prompt=prompt,
                     negative_prompt=negative_prompt,
                     image=sr_image,
                     strength=0.1,
                     guidance_scale=11,
                     num_inference_steps=200,
                     ).images[0]
    upscaled_image = f'static/uploaded/pose_{twoimagelist.Now_idx()}.jpeg'
    image.save(upscaled_image)
    image.save('up_image.png')
    # -------------------------------------------------------------------------
    # -----------------------------------------------------------------
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/control_v11p_sd15_openpose", torch_dtype=torch.float16
    )
    controlnet.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        ckpt_path, controlnet=controlnet, num_hidden_layers=11, torch_dtype=torch.float16
    )
    pipe.safety_checker = None
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
        pipe.scheduler.config)
    pipe.load_textual_inversion(r"function\EasyNegative.safetensors")
    pipe.load_textual_inversion(r"function\badhandv4.pt")
    pipe = pipe.to('cuda')

    # -------------------------------------openpose------------------------------------------
    processor = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
    # r"C:\Users\user\Desktop\SD_OUTPUT\a 20 yo woman,blonde,(hi-... (15) .png"
    image_path = upscaled_image

    image = Image.open(image_path).convert("RGB")
    init_image = image.resize((512, 512))
    init_image = processor(init_image, hand_and_face=True)
    init_image.save(f"static/openpose/pose_{twoimagelist.Now_idx()}.jpeg")
    image_path = rf"static\openpose\pose_{twoimagelist.Now_idx()}.jpeg"
    image = Image.open(image_path).convert("RGB")
    init_image = image.resize((512, 512))
    # ----------------------------------------------------------------------------------------
    generator = torch.Generator(device="cuda").manual_seed(3698311310)

    with autocast('cuda'):
        images = pipe(prompt=prompt,
                      negative_prompt=negative_prompt,
                      image=init_image,
                      guidance_scale=7,
                      num_inference_steps=30,
                      ).images[0]

    images.save(f"static/openpose/{pp}.jpeg")

    # -------------------high res.fix-----------------------------

    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        ckpt_path, num_hidden_layers=11, torch_dtype=torch.float16)
    pipe.safety_checker = None
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
        pipe.scheduler.config)
    pipe.load_textual_inversion(r"function\EasyNegative.safetensors")
    pipe.load_textual_inversion(r"function\badhandv4.pt")
    pipe = pipe.to('cuda')

    with autocast('cuda'):
        images = pipe(prompt=prompt,
                      negative_prompt=negative_prompt,
                      image=images,
                      strength=0.2,
                      guidance_scale=9,
                      num_inference_steps=30,
                      ).images[0]

    images.save(f"static/openpose/{pp}.jpeg")

    model = RealESRGAN('cuda', scale=2)
    model.load_weights('weights/RealESRGAN_x4plus_anime_6B.pth')
    sr_image = model.predict(images)
    sr_image = sr_image.resize((512, 512))
    sr_image.save(f"static/openpose/{pp}.jpeg")

    with autocast("cuda"):
        image = pipe(prompt=prompt,
                     negative_prompt=negative_prompt,
                     image=sr_image,
                     strength=0.3,
                     guidance_scale=7,
                     num_inference_steps=30,
                     ).images[0]
    os.remove(f"static/openpose/{pp}.jpeg")
    result_image = f"static/openpose/openpose_{twoimagelist.Now_idx()}.jpeg"
    image.save(result_image)
    twoimagelist.save(twoimagelist.Now_idx(), user, stdname, kpp,
                      knp, filter, poseimg_path, "", result_image, share)
    # -------------------------------------------------------------------------
