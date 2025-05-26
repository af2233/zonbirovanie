import io
import zipfile
import logging
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

from engine import run_engine


logging.basicConfig(level=logging.INFO)

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


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=4000)
