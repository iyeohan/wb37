import os
import torch
from torch import autocast
from RealESRGAN import RealESRGAN
from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import DPMSolverMultistepScheduler
from diffusers import AutoencoderKL


SAVE_PATH = os.path.join(
    os.environ['USERPROFILE'], 'Desktop', 'STD2', 'static', 'img')


def stdv1_5(pp, np, filter, cfg, steps):
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)

    def uniquify(path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + ' (' + str(counter) + ') ' + extension
            counter += 1

        return path
    
    prompt = pp+", (masterpiece:1.2), best quality, ultra-detailed, illustration"
    negative_prompt = np+"badhandv4,(worst quality:1.6),(low quality:1.6),  easynegative"
    if filter == "PastelMix":
        ckpt_path = r"Stable-diffusion\pastelmix-fp16.safetensors"
        vae_repo = "lint/anime_vae"
    elif filter == "Ghibli1":
        ckpt_path = r"Stable-diffusion\ghibliStyleMix_v10.ckpt"
        vae_repo = "lint/anime_vae"
    elif filter == "MintReal":
        ckpt_path = r"Stable-diffusion\MintRealistic A2 FP16.safetensors"
        vae_repo = "lint/anime_vae"
    elif filter == "CetusMix":
        ckpt_path = r"Stable-diffusion\cetusMix_Whalefall2.safetensors"
        vae_repo = "lint/anime_vae"
    elif filter == "MajicMix":
        ckpt_path = r"Stable-diffusion\majicmixRealistic_betterV2V25.safetensors"
        vae_repo = "lint/anime_vae"
    else:
        print("체크포인트를 찾을 수 없습니다.")

    print(f"Characters in prompt: {prompt,len(prompt)}, limit: 200")
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16)
    pipe = StableDiffusionPipeline.from_ckpt(
        ckpt_path, torch_dtype=torch.float16, num_hidden_layers=11)
    pipe.safety_checker = None
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config)
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe.load_textual_inversion(r"function\EasyNegative.safetensors")
    pipe.load_textual_inversion(r"function\badhandv4.pt")
    pipe = pipe.to('cuda')
    # pipe.load_lora_weights(lora_path)

    generator = torch.Generator(device="cuda").manual_seed(-1)

    with autocast('cuda'):
        image = pipe(prompt=prompt,
                     negative_prompt=negative_prompt,
                     guidance_scale=float(cfg),  # cfg 스케일
                     num_inference_steps=int(steps),
                     ).images[0]

    # -------------------high res.fix-----------------------------
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16)
    pipe = StableDiffusionImg2ImgPipeline.from_ckpt(
        ckpt_path, torch_dtype=torch.float16, num_hidden_layers=11)
    pipe.safety_checker = None
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config)
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    pipe.load_textual_inversion(r"function\EasyNegative.safetensors")
    pipe.load_textual_inversion(r"function\badhandv4.pt")
    pipe = pipe.to('cuda')

    model = RealESRGAN('cuda', scale=2)
    model.load_weights('weights/RealESRGAN_x4.pth')
    sr_image = model.predict(image)
    sr_image = sr_image.resize((512, 512))
    sr_image.save('up_image.png')

    with autocast('cuda'):
        images = pipe(prompt=prompt,
                      negative_prompt=negative_prompt,
                      image=sr_image,
                      strength=0.5,
                      num_inference_steps=30,
                      ).images[0]
    images.save("static/testimg/"+pp+".jpeg")
    # -------------------------------------------------------------------------
