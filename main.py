from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QueryModel(BaseModel):
    query: str

@app.post("/api/satquery")
async def satquery_endpoint(data: QueryModel):
    q = data.query.lower()
    if "building" in q or "structure" in q or "detect changes" in q:
        return {
            "summary": "Significant land-use changes detected in the selected area.",
            "detections": [
                {"title": "23 New Structures", "desc": "Newly constructed buildings detected."},
                {"title": "14% Vegetation Decrease", "desc": "Vegetation cover has decreased."},
                {"title": "2 Water-body Changes", "desc": "Water bodies area/shape changed."},
                {"title": "7.4 km Road Expansion", "desc": "New road networks detected."}
            ],
            "confidence": 94.2,
            "source": "Sentinel-2 • 28 Aug 2026"
        }
    elif "flood" in q or "water" in q:
        return {
            "summary": "Water body contraction and flood inundation span calculated at 18.4 km² across coastal basin.",
            "detections": [
                {"title": "18.4 km² Inundation", "desc": "Active flood zone span detected."}
            ],
            "confidence": 92.8,
            "source": "Sentinel-2 • 28 Aug 2026"
        }
    else:
        return {
            "summary": f"Processed query '{data.query}': Identified active land-use shifts and regional modifications.",
            "detections": [
                {"title": "General Land Shift", "desc": "Topographical alterations observed."}
            ],
            "confidence": 94.2,
            "source": "Sentinel-2 • 28 Aug 2026"
        }

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename, "status": "success", "message": "Satellite raster ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)