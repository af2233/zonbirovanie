from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from engine import run_engine
import io
import zipfile

app = FastAPI()

# Разрешаем CORS (для фронта)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # замените на свой домен в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process/")
async def process(file: UploadFile = File(...)):
    try:
        zip_bytes = await file.read()
        results = run_engine(zip_bytes)

        if not results:
            return JSONResponse(content={"error": "No output generated"}, status_code=500)

        archive_buffer = io.BytesIO()
        with zipfile.ZipFile(archive_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for fname, img_bytes in results.items():
                zf.writestr(fname, img_bytes)

        archive_buffer.seek(0)

        return StreamingResponse(
            archive_buffer,
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": "attachment; filename=results.zip"}
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
