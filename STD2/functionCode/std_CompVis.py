import torch
from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import DPMSolverMultistepInverseScheduler
from diffusers import DPMSolverMultistepScheduler
from diffusers import AutoencoderKL
from torch import autocast
from RealESRGAN import RealESRGAN

device = "cuda"
#model_id = "CompVis/stable-diffusion-v1-4"
model_id = "runwayml/stable-diffusion-v1-5"
ckpt_path = r"Stable-diffusion\pastelmix-fp16.safetensors"
vae_repo = "lint/anime_vae"


def compvis(prompt,np, cfg, steps):
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config)
    pipe.safety_checker = None
    pipe = pipe.to(device)
    pprompt = prompt + ", (masterpiece:1.2), best quality, ultra-detailed, illustration"
    with autocast(device):
        images = pipe(prompt=pprompt, negative_prompt=np,
                      guidance_scale=float(cfg), num_inference_steps=int(steps),).images[0]
    # images.save("static/unupscale/"+pprompt+"_.jpeg")
    # -------------------high res.fix-----------------------------
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        model_id, torch_dtype=torch.float16)
    pipe.safety_checker = None
    pipe = pipe.to('cuda')

    model = RealESRGAN('cuda', scale=2)
    model.load_weights('weights/RealESRGAN_x4.pth')
    sr_image = model.predict(images)
    sr_image = sr_image.resize((512, 512))
    sr_image.save('up_image.png')

    with autocast('cuda'):
        images = pipe(prompt=pprompt,
                      negative_prompt=np,
                      image=sr_image,
                      strength=0.5,
                      num_inference_steps=30,
                      ).images[0]
    #image_path = uniquify(os.path.join(SAVE_PATH, (prompt[:25] + '...')if len(prompt) > 25 else prompt) + '.png')
    images.save("static/testimg/"+prompt+".jpeg")
    # -------------------------------------------------------------------------
