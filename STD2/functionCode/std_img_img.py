import torch
from torch import autocast
from diffusers import AutoencoderKL
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import DPMSolverMultistepScheduler
from PIL import Image
from torch import autocast
from RealESRGAN import RealESRGAN


def img_to_img(pprompt, nprompt, filter, image_path, cfg, steps, noise_strength):
    device = "cuda"
    model_id_or_path = "runwayml/stable-diffusion-v1-5"
    if filter == "MintReal":
        ckpt_diff = r"Stable-diffusion\MintReal_diffuser"
        ckpt_path = r"Stable-diffusion\MintRealistic A2 FP16.safetensors"
        vae_repo = "lint/anime_vae"
    elif filter == "Ghibli1":
        ckpt_diff = r"Stable-diffusion\ghibliJin_diffuser"
        ckpt_path = r"Stable-diffusion\ghibliStyleMix_v10.ckpt"
        vae_repo = "lint/anime_vae"
    elif filter == "CetusMix":
        ckpt_diff = r"Stable-diffusion\cetusMix_diffuser"
        ckpt_path = r"Stable-diffusion\cetusMix_Whalefall2.safetensors"
        vae_repo = "redstonehero/kl-f8-anime2"
    elif filter == "MajicMix":
        ckpt_diff = r"Stable-diffusion\majicmix_diffuser"
        ckpt_path = r"Stable-diffusion\majicmixRealistic_betterV2V25.safetensors"
        vae_repo = "lint/anime_vae"
    print(ckpt_diff)
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(ckpt_diff, torch_dtype=torch.float16, num_hidden_layers=11)
    pipe.safety_checker = None
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config)
    pipe.vae = AutoencoderKL.from_pretrained(vae_repo)
    #pipe.load_textual_inversion(r"function\EasyNegative.safetensors")
    pipe = pipe.to(device)

    image = Image.open(image_path).convert("RGB")
    init_image = image.resize((512, 512))

    prompt = pprompt + ", (masterpiece:1.2), best quality, ultra-detailed, illustration"
    negative_prompt = nprompt + ", (worst quality:1.6),(low quality:1.6),  easynegative"

    with autocast('cuda'):
        images = pipe(prompt=prompt,
                      negative_prompt=negative_prompt,
                      image=init_image,
                      strength=float(noise_strength),
                      guidance_scale=float(cfg),
                      num_inference_steps=int(steps)
                      ).images[0]
    # -------------------high res.fix-----------------------------

    model = RealESRGAN('cuda', scale=2)
    model.load_weights('weights/RealESRGAN_x4plus_anime_6B.pth')
    sr_image = model.predict(images)
    sr_image = sr_image.resize((512, 512))

    with autocast("cuda"):
        image = pipe(prompt=prompt,
                     negative_prompt=negative_prompt,
                     image=sr_image,
                     strength=0.4,
                     guidance_scale=7,
                     num_inference_steps=100,
                     ).images[0]
    image.save("static/testimg/"+pprompt+".jpeg")
    # -------------------------------------------------------------------------
