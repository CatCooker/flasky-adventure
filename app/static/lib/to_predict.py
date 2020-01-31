import torch
from PIL import Image
import numpy as np
model_path = "app/static/model/vggmodel_fc2_epc50.pth"
class_ = {
    "0": "其他垃圾/一次性快餐盒",
    "1": "其他垃圾/污损塑料",
    "2": "其他垃圾/烟蒂",
    "3": "其他垃圾/牙签",
    "4": "其他垃圾/破碎花盆及碟碗",
    "5": "其他垃圾/竹筷",
    "6": "厨余垃圾/剩饭剩菜",
    "7": "厨余垃圾/大骨头",
    "8": "厨余垃圾/水果果皮",
    "9": "厨余垃圾/水果果肉",
    "10": "厨余垃圾/茶叶渣",
    "11": "厨余垃圾/菜叶菜根",
    "12": "厨余垃圾/蛋壳",
    "13": "厨余垃圾/鱼骨",
    "14": "可回收物/充电宝",
    "15": "可回收物/包",
    "16": "可回收物/化妆品瓶",
    "17": "可回收物/塑料玩具",
    "18": "可回收物/塑料碗盆",
    "19": "可回收物/塑料衣架",
    "20": "可回收物/快递纸袋",
    "21": "可回收物/插头电线",
    "22": "可回收物/旧衣服",
    "23": "可回收物/易拉罐",
    "24": "可回收物/枕头",
    "25": "可回收物/毛绒玩具",
    "26": "可回收物/洗发水瓶",
    "27": "可回收物/玻璃杯",
    "28": "可回收物/皮鞋",
    "29": "可回收物/砧板",
    "30": "可回收物/纸板箱",
    "31": "可回收物/调料瓶",
    "32": "可回收物/酒瓶",
    "33": "可回收物/金属食品罐",
    "34": "可回收物/锅",
    "35": "可回收物/食用油桶",
    "36": "可回收物/饮料瓶",
    "37": "有害垃圾/干电池",
    "38": "有害垃圾/软膏",
    "39": "有害垃圾/过期药物"
}
garbage_t = {
    "厨余垃圾":"kitchen",
    "其他垃圾":"other",
    "有害垃圾":"harmful",
    "可回收物":"recycle"
}
def model_predict(model_path,img_file):
    model = None
    img = Image.open(img_file)
    # Image._show(img)
    img = img.resize((224, 224))
    img = np.array(img)
    img = np.transpose(img, (2, 0, 1))  # 将aixs修改为 channel，height，width
    img = img.astype('float32')
    img = img / 255.0
    img = torch.from_numpy(img)
    img = img.unsqueeze(0)
    if torch.cuda.is_available():
        model = torch.load(model_path).cuda()
        img = img.cuda()
    pred = model(img)
    acc = torch.softmax(pred,dim=1)
    pred = pred.argmax(dim=1).item()
    possibility = round(acc[0][pred].item(),2) * 100
    label = class_[str(int(pred))]
    label = label.split('/')
    print(label)
    print(possibility)
    return label,possibility


