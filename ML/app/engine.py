import os
import random
import zipfile
import torch
from torchvision.utils import save_image
from PIL import Image
from tqdm import tqdm
from pathlib import Path
from tempfile import TemporaryDirectory

from models import UNet, get_transforms


# Параметры
SEED = 666
DROPOUT = 0.2
IMG_SIZE = 320
BATCH_SIZE = 16
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
CHECKPOINT = Path('../models/model_45_mln_52_iou.pth')


def set_seed(seed: int = SEED):
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)


def safe_extract(zip_path: Path, extract_to: Path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        total_size = sum(file.file_size for file in zip_ref.infolist())
        max_size = 1024 * 1024 * 1024  # 1 GB

        if total_size > max_size:
            raise ValueError("Archive too big")

        zip_ref.extractall(path=extract_to)


def predict(model: torch.nn.Module, input_path: Path, result_path: Path, batch_size: int = BATCH_SIZE):
    X_trans, _ = get_transforms(IMG_SIZE)
    input_files = sorted(f for f in os.listdir(input_path) if f.lower().endswith(('.png', '.jpg', '.jpeg')))

    for batch_start in tqdm(range(0, len(input_files), batch_size)):
        batch_files = input_files[batch_start:batch_start + batch_size]
        batch_images = []

        for fname in batch_files:
            try:
                img = Image.open(input_path / fname).convert("RGB")
                img_tensor = X_trans(img)
                batch_images.append(img_tensor)
            except Exception as e:
                print(f"Error loading image {fname}: {e}")
                continue

        if not batch_images:
            continue

        batch_tensor = torch.stack(batch_images).to(DEVICE)

        with torch.inference_mode():
            preds = model(batch_tensor)

        for fname, pred in zip(batch_files, preds):
            base = Path(fname).stem
            save_path = result_path / f"{base}_pred.png"
            save_image(pred, save_path)


def run_engine(zip_bytes: bytes) -> dict[str, bytes]:
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        input_dir = tmpdir / "input"
        result_dir = tmpdir / "result"
        input_dir.mkdir()
        result_dir.mkdir()

        zip_path = tmpdir / "input.zip"
        with open(zip_path, "wb") as f:
            f.write(zip_bytes)

        set_seed()

        try:
            safe_extract(zip_path, extract_to=input_dir)
        except Exception as e:
            raise RuntimeError(f"Failed to extract archive: {e}")

        model = UNet(dropout=DROPOUT).to(DEVICE)
        model.load_state_dict(torch.load(CHECKPOINT, map_location=DEVICE, weights_only=True))

        predict(model=model, input_path=input_dir, result_path=result_dir)

        result = {}
        for file in os.listdir(result_dir):
            fpath = result_dir / file
            with open(fpath, 'rb') as f:
                result[file] = f.read()

        return result
