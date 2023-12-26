import os
import traceback

from .utils import *
import numpy as np
from PIL import Image,ImageChops
from urllib.parse import urljoin,quote

def mockup_render(spu,img):
    http_path = "https://clkj-image-qd.oss-cn-qingdao.aliyuncs.com/comfyui-yoy/"
    dir_path = r"custom_nodes/comfyui-yoy/data/"
    spu_path = os.path.join(dir_path,spu)
    base_file = os.path.join(spu_path,"base.png")
    mask_file = os.path.join(spu_path,"mask.png")
    texture_file = os.path.join(spu_path,"texture.png")
    if spu not in os.listdir(dir_path):
        # download
        try:
            product_pre = urljoin(http_path,quote(spu,"utf-8")+"/")
            os.mkdir(spu_path)
            read_image(urljoin(product_pre,"base.png")).save(base_file)
            read_image(urljoin(product_pre,"mask.png")).save(mask_file)
            read_image(urljoin(product_pre,"texture.png")).save(texture_file)
        except:
            traceback.print_exc()

    base_img = Image.open(base_file)
    mask_img = Image.open(mask_file)
    if "texture.png" in os.listdir(spu_path):
        texture_img = Image.open(texture_file)
        tmp_texture = Image.new("RGBA", texture_img.size, "white")
        tmp_texture.paste(texture_img,(0,0),texture_img)

    tmp1_base = Image.new("RGBA",base_img.size,(0,0,0,0))
    tmp2_base = Image.new("RGBA", base_img.size, (255, 255, 255, 255))
    mask_size = np.where(np.array(mask_img)[:,:,3] > 200)
    h = max(mask_size[0]) - min(mask_size[0])
    w = max(mask_size[1]) - min(mask_size[1])
    left_top = min(mask_size[1]), min(mask_size[0])

    tmp1_base.paste(img.resize((w, h)), left_top)
    tmp2_base.paste(tmp1_base,(0,0),mask_img)
    # base_img.paste(tmp_base,(0,0),mask_img)
    base_img = ImageChops.multiply(base_img, tmp2_base)

    if "texture.png" in os.listdir(spu_path):
        final_img = ImageChops.multiply(base_img,tmp_texture)
        # base_img.paste(texture_img,(0,0),texture_img)
    else:
        final_img = base_img

    return base_img

class MOCKUP:
    @classmethod
    def INPUT_TYPES(s):
        res = requests.get("https://clkj-image-qd.oss-cn-qingdao.aliyuncs.com/comfyui-yoy/product.txt")
        products = res.text.split("\r\n")
        return {"required": {
            "image": ("IMAGE",),
             "product":(products,),
                }}

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "yoy_nodes"
    CATEGORY = "yoy_nodes"

    def yoy_nodes(self, image,product):
        image_np = img_tensor_to_np(image)
        image = Image.fromarray(image_np)
        res_img = mockup_render(product,image)
        processed_image_tensor = img_np_to_tensor(np.array(res_img))
        return (processed_image_tensor,)

NODE_CLASS_MAPPINGS = {
    "MOCKUP":MOCKUP,
}
