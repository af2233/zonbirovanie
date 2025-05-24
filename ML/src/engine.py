import torch
from torchvision.utils import save_image

import os
import random
import zipfile
from PIL import Image
from tqdm import tqdm
from pathlib import Path

from model import UNet, get_transforms

# гиперпараметры 
SEED = 666

DATA_PATH = Path('photos')
MODELS_PATH = Path('models')
ACHIEVE_PATH = Path('input.zip')
INPUT_PATH = DATA_PATH 
RESULT_PATH = DATA_PATH / 'result'
CHECKOPOINT = MODELS_PATH / 'model_43iou.pth'

DROPOUT = 0.2 # параметр который нужен для создания модели
IMG_SIZE = 256
BATCH_SIZE = 16 

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu' # на чем будет все будет работать, если нет nvidia & cuda не советую запускать


def set_seed(seed: int = SEED) -> None:

    random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)


def safe_extract(zip_path: Path,
                 extract_to: Path = INPUT_PATH) -> None:
    
    if not os.path.exists(INPUT_PATH):
        os.mkdir(INPUT_PATH)

    if not os.path.exists(RESULT_PATH):
        os.mkdir(RESULT_PATH)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        total_size = sum(file.file_size for file in zip_ref.infolist())
        extracted_size = 0
        max_size = 1024 * 1024 * 1024  # 1 Gb (можно изменить)
        
        if total_size > max_size:
            raise ValueError("Achieve too big")
        
        for file in zip_ref.infolist():
            extracted_size += file.file_size
            if extracted_size > max_size:
                raise ValueError("Extracted archieve too big")
            zip_ref.extract(file, extract_to)


def predict(model: torch.nn.Module,
            input_path: str = INPUT_PATH,
            result_path: str = RESULT_PATH,
            batch_size: int = BATCH_SIZE) -> None:
    
    X_trans, _ = get_transforms(IMG_SIZE) # получаем трансформации
    input_images_paths = sorted(list(os.walk(input_path))[0][2]) # собираем названия всех изображений

    for batch_start in tqdm(range(0, max(len(input_images_paths), batch_size), batch_size)):
        # изображения объеднияем в батч, так как модель будет обрабатывать небольшой батч и 1 изображение одинаково по скорости (но не по памяти)
        batch_end = min(batch_start + batch_size, len(input_images_paths))
        batch_files = input_images_paths[batch_start:batch_end]
        print(f"Processing batch {batch_start//batch_size + 1}: files {batch_start}-{batch_end-1}")
        
        batch_images = []
        for img_path in batch_files:
            try:
                img = Image.open(f'{input_path}/{img_path}')
                img_tensor = X_trans(img)
                batch_images.append(img_tensor)
                # изображение преобразовано в тензор, размерность которого - (3, 256, 256)
                #  3 канала RGB, 256х256 - размер изображения
            except Exception as e:
                print(f"Error processing {img_path}: {str(e)}")
                continue
        
        batch_images = torch.stack(batch_images).to(DEVICE)
        # размерность batch_images - (5, 3, 256, 256) - то есть 5 изображений
        with torch.inference_mode():
            pred = model(batch_images) # получаем маски, разменость которых так же (5, 3, 256, 256)
    

        for img_path, pred_tensor in zip(batch_files, pred):
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            save_path = os.path.join(RESULT_PATH, f"{base_name}_pred.png")
            # сохраняем каждую маску как фотографию
            save_image(pred_tensor, save_path)


def main():

    set_seed()
    # создаем модель и загружаем веса
    unet_model = UNet(dropout=DROPOUT).to(DEVICE)
    unet_model.load_state_dict(torch.load(f=CHECKOPOINT, map_location=DEVICE, weights_only=True))
    # распаковываем и делаем маски
    safe_extract(zip_path=ACHIEVE_PATH, extract_to=INPUT_PATH)
    predict(model=unet_model, input_path="photos/input")

        


if __name__ == '__main__':
    main()