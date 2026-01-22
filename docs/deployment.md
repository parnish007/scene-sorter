Got it 👍
Below is the **final, clean, copy-paste ready content** for:

📄 **`C:\Users\AB\Desktop\scene-sorter\docs\deployment.md`**

---

````md
# Deployment Guide – Scene Sorter Backend

This document explains how to run and deploy the Scene Sorter backend locally and using Docker.

---

## 1. Local Development (Recommended for Testing)

### Step 1: Go to backend folder
```bash
cd backend
````

### Step 2: Create virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate virtual environment

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Verify

Open in browser:

* [http://localhost:8000/health](http://localhost:8000/health)
* [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 2. Using the API

### Batch prediction flow

1. Upload multiple images to `/predict/batch`
2. Backend:

   * runs ML inference
   * organizes images into class folders
   * creates a ZIP file
3. Download ZIP using `/download/{job_id}`

---

## 3. Docker Deployment

### Step 1: Build Docker image

From `backend/` directory:

```bash
docker build -t scene-sorter-backend .
```

### Step 2: Run Docker container

```bash
docker run -p 8000:8000 scene-sorter-backend
```

Backend will be available at:

* [http://localhost:8000](http://localhost:8000)

---

## 4. Folder Storage Behavior

Temporary files are created under:

```
.scene_sorter_tmp/
  └── {job_id}/
      ├── raw/
      ├── organized/
      └── zips/
```

Each job is isolated to support multiple concurrent users.

---

## 5. Production Considerations (Future Improvements)

* Use cloud storage (AWS S3 / Supabase Storage) instead of local temp folders
* Add authentication & rate limiting
* Add async job queue for large batches
* Enable HTTPS with Nginx or a cloud load balancer
* Add scheduled cleanup of old jobs

---

## 6. Environment Variables (Optional)

You can override defaults using environment variables:

* `SCENE_SORTER_MODEL_PATH`
* `SCENE_SORTER_LABELS_PATH`
* `SCENE_SORTER_TEMP_ROOT`

---

## 7. Status

✅ Backend is production-structured
✅ Docker-ready
✅ Scalable design


```

---

## ✅ Deployment docs are now COMPLETE

At this point:
- Backend code ✅
- Docs folder ✅
- Deployment instructions ✅

