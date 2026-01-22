
# 📄 `docs/system_design.md`

```md
# System Design – Scene Sorter

## Overview
Scene Sorter is an AI-powered backend system that automatically classifies images by environment
(buildings, forest, glacier, mountain, sea, street) and organizes them into structured folders.
Users upload multiple images, and the system returns a downloadable ZIP with class-wise folders.

---

## High-Level Architecture

```

Client (Web UI)
|
|  (multipart upload)
v
FastAPI Backend
|
|--> Image Validation
|--> Preprocessing
|--> ML Inference (TensorFlow/Keras)
|--> Folder Organization
|--> ZIP Creation
|
v
Download ZIP

```

---

## Core Components

### 1. API Layer
- FastAPI
- Handles:
  - file uploads
  - validation
  - responses
- Endpoints:
  - `/health`
  - `/predict`
  - `/predict/batch`
  - `/download/{job_id}`

### 2. ML Inference Layer
- TensorFlow/Keras model
- Loaded once at startup (singleton)
- Batch inference for performance

### 3. Storage Layer (Temporary)
Each batch request gets an isolated workspace:

```

.scene_sorter_tmp/
└── job_id/
├── raw/
├── organized/
└── zips/

```

This design:
- supports concurrent users
- avoids filename collisions
- simplifies cleanup

---

## Design Decisions

- **Batch inference** instead of per-image calls → faster & scalable
- **Job-based directories** → concurrency-safe
- **ZIP-based output** → simple UX for users
- **Stateless API** → easy deployment

---

## Scalability Considerations (Future)
- Replace local temp storage with S3 / Supabase Storage
- Add async job queue (Celery / Redis)
- Add auth + rate limiting
```

---

# 📄 `docs/api_contract.md`

```md
# API Contract – Scene Sorter

Base URL:
```

[http://localhost:8000](http://localhost:8000)

````

---

## 1. Health Check

### GET `/health`

**Response**
```json
{
  "status": "ok",
  "message": "Scene Sorter API is running"
}
````

---

## 2. Single Image Prediction

### POST `/predict`

**Request**

* `multipart/form-data`
* field: `file` (image)

**Response**

```json
{
  "filename": "image.jpg",
  "label": "mountain",
  "confidence": 0.93
}
```

---

## 3. Batch Image Prediction (Main Feature)

### POST `/predict/batch`

**Request**

* `multipart/form-data`
* field: `files[]` (multiple images)

**Response**

```json
{
  "job_id": "abc123",
  "summary": {
    "total": 10,
    "by_class": {
      "mountain": 4,
      "sea": 2,
      "forest": 2,
      "buildings": 1,
      "street": 1
    }
  },
  "results": [
    {
      "filename": "img1.jpg",
      "label": "mountain",
      "confidence": 0.94
    }
  ],
  "download_url": "/download/abc123"
}
```

---

## 4. Download Organized ZIP

### GET `/download/{job_id}`

**Response**

* File download: `organized_photos_{job_id}.zip`

**Error**

```json
{
  "detail": "Zip not found. Run /predict/batch first."
}
```

````

---

# 📄 `docs/model_details.md`

```md
# Model Details – Scene Classification

## Dataset
Intel Image Classification Dataset

## Classes
- buildings
- forest
- glacier
- mountain
- sea
- street

Total classes: 6

---

## Model
- Framework: TensorFlow / Keras
- Model file: `best_finetuned_model.keras`
- Architecture: CNN-based (fine-tuned)

---

## Input Specification
- Image size: 224 × 224
- Channels: RGB (3)
- Data type: float32
- Normalization: pixel values scaled to [0, 1]

---

## Output
- Probability vector of shape `(6,)`
- Softmax activation
- Top-1 class selected for prediction

---

## Labels Mapping
Stored in:
````

model/exported/labels.json

````

Example:
```json
{
  "class_names": ["buildings", "forest", "glacier", "mountain", "sea", "street"]
}
````

---

## Notes

* Preprocessing must exactly match training preprocessing
* Model is loaded once at backend startup for performance

````

---

# 📄 `docs/deployment.md`

```md
# Deployment Guide – Scene Sorter Backend

## Local Development

### 1. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run server

```bash
uvicorn app.main:app --reload
```

Open:

* [http://localhost:8000/docs](http://localhost:8000/docs)
* [http://localhost:8000/health](http://localhost:8000/health)

---

## Docker Deployment

### Build image

```bash
docker build -t scene-sorter-backend .
```

### Run container

```bash
docker run -p 8000:8000 scene-sorter-backend
```

---

## Production Notes

* Use Nginx as reverse proxy
* Store temp files on mounted volume or cloud storage
* Add HTTPS, rate limiting, and authentication if public-facing

```

---

## ✅ Docs folder is now COMPLETE

You now have:
- System design documentation
- Clear API contract
- Model explanation
- Deployment instructions

This makes your project:
- 📌 **Interview-ready**
- 📌 **Open-source ready**
- 📌 **LinkedIn / GitHub professional**

---

### Next step?
Say one of these:
- **“Test backend now”**
- **“Start frontend docs & code”**
- **“README.md final version”**

You’ve officially built a *full AI system*, not just a model 👏
```
