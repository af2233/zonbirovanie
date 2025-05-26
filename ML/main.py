from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from engine import run_engine
import io, zipfile, httpx

app = FastAPI()

@app.post("/process")
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
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://django-app/get-file/",
                files={"file": ("result.zip", archive_buffer.getvalue(), "application/zip")}
            )

        return {"status": "forwarded", "upstream_status": response.status_code}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)