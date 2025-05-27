import io, zipfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from engine import run_engine


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:3000",
    "http://frontend:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

@app.post("/predict")
async def process(file: UploadFile = File(...)):
    try:
        zip_bytes = await file.read()
        results = run_engine(zip_bytes)

        # Пакуем данные в zip
        archive_buffer = io.BytesIO()
        with zipfile.ZipFile(archive_buffer, 'w') as zf:
            for fname, img_bytes in results.items():
                zf.writestr(fname, img_bytes)

        archive_buffer.seek(0)

        # Отправляем по адресу
        return StreamingResponse(
            archive_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=result.zip"}
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
