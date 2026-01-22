


# 🖼️ Scene Sorter  
### AI-Powered Scene Classification & Smart Image Organizer

**Scene Sorter** is an open-source, end-to-end AI tool that automatically classifies and organizes images into real-world scene categories such as **mountain, forest, glacier, sea, street, and buildings**.

It is designed for **travelers, photographers, dataset curators, and AI engineers** who want their images **clean, structured, and instantly usable**.

> Built with a production-ready mindset — from model training → API → UI → deployment.

---

## 🌍 Live Project

- **Frontend (UI):** https://-FRONTEND-LINK  (will upate soon when deployed) 

- **Backend API:** https:-BACKEND-LINK  (will upate soon when deployed) 

- **Swagger Docs:** https:/-BACKEND-LINK/docs 
(will upate soon when deployed) 

---

## 📸 Demo & Screenshots

_(Add images later — paths prepared)_

| Upload Images | Batch Results |
|--------------|---------------|
| ![Upload](./assets/upload.png) | ![Results](./assets/results.png) |

| ZIP Download | Swagger API |
|-------------|-------------|
| ![ZIP](./assets/zip.png) | ![Docs](./assets/docs.png) |

---

## ❓ The Real Problem (Why I Built This)

As someone who **travels a lot**, I constantly faced this problem:

- After trips, I had **hundreds of photos**
- Mountains, glaciers, streets, seas — all mixed
- Manual sorting is **slow, boring, and error-prone**
- Existing gallery apps don’t offer **semantic scene sorting**

There was **no simple tool** that could:
- Understand *what* is in an image
- Group images meaningfully
- Export them cleanly for reuse

So instead of accepting the pain, I built **Scene Sorter**.

> This project is a **problem-solver’s answer**, not just a model demo.

---

## 🧠 Model Journey (From Scratch → Production)

### Phase 1 — CNN From Scratch  
- Built a custom CNN architecture
- Trained on scene classification dataset
- **Accuracy achieved:** ~75%
- Problems:
  - Overfitting
  - Slower convergence
  - Limited generalization

➡️ Good learning phase, but **not production-grade**

---

### Phase 2 — Transfer Learning (Breakthrough)

Switched to **MobileNetV2 (ImageNet weights)**:

- Used pretrained feature extractor
- Added custom classification head
- Fine-tuned higher layers
- Applied dropout & regularization

📈 **Results:**
- **Accuracy:** ~86–87%
- Faster convergence
- Better generalization
- Lower inference latency

This is the model now running in production.

---

## 🏷️ Scene Classes

```json
["buildings", "forest", "glacier", "mountain", "sea", "street"]
````

Each prediction returns:

* label
* confidence score
* full probability vector

---

## ⚙️ How the System Works

### High-Level Flow

```
User Uploads Images
        ↓
Frontend (Next.js)
        ↓
FastAPI Backend
        ↓
Image Preprocessing (PIL + NumPy)
        ↓
TensorFlow Model (MobileNetV2)
        ↓
Class-Based Folder Sorting
        ↓
ZIP File Generation
        ↓
Download Link Returned
```

---

## 🧩 Key Features

### 🔹 Single Image Prediction

* Upload one image
* Get:

  * predicted label
  * confidence score

### 🔹 Batch Image Classification

* Upload multiple images at once
* Model runs **batch inference**
* Images grouped by predicted class

### 🔹 Automatic Folder Sorting

```
output/
├── mountain/
│   ├── img1.jpg
│   └── img2.jpg
├── glacier/
└── forest/
```

### 🔹 ZIP Export

* Entire sorted directory is compressed
* Downloadable as a single ZIP

---

## 🛠️ Tech Stack

### Frontend

* **Next.js 14**
* **TypeScript**
* **Tailwind CSS**
* Drag-and-drop uploads
* Batch preview & progress UI

### Backend

* **FastAPI**
* **Python 3.11**
* **Uvicorn**
* RESTful architecture
* Swagger documentation

### Machine Learning

* **TensorFlow / Keras**
* **MobileNetV2**
* Transfer Learning
* Softmax classification
* Batch inference optimization

### DevOps & Deployment

* **Docker**
* **Render**
* GitHub CI workflow
* Environment-based config

---

## 🧪 Testing the System

### 1️⃣ Single Image Test

* Endpoint: `POST /predict`
* Upload one image
* Returns:

```json
{
  "filename": "mountain.jpg",
  "label": "mountain",
  "confidence": 0.82
}
```

---

### 2️⃣ Batch Test

* Endpoint: `POST /predict/batch`
* Upload multiple images
* Returns:
* per-image predictions
* ZIP download link

---

## 🚀 Deployment Strategy

* Backend deployed as **Docker Web Service** on Render
* Frontend deployed separately
* Environment variables control:

  * model path
  * CORS
  * batch limits
* CPU-only deployment (no GPU required)

---

## 📈 Performance

* **Accuracy:** ~86–87%
* **Latency:** Optimized via lightweight MobileNetV2
* **Scalability:** Batch-ready, stateless API
* **Portability:** Dockerized & cloud-ready

---

## 🔮 Future Improvements (Vision)

This project is intentionally built to grow.

### Planned Enhancements

* 📱 **Mobile integration**

  * Auto-sort photos directly on device
  * No manual download required
* 🧠 Multi-model support (ViT, CLIP)
* ☁️ Cloud storage integration
* 👤 User accounts & personal galleries
* 📊 Analytics dashboard
* 🎯 Custom class training via UI

> Ultimate goal: **Photos auto-organize themselves the moment you return from a trip.**

---

## 🤝 Open Source & Contributions

This project is **fully open-source**.

You can:

* Improve the model
* Add new classes
* Optimize inference
* Enhance UI/UX
* Extend to mobile

PRs, issues, and ideas are welcome.

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 👋 Author

Built by **Parnish**
AI Engineer • ML Practitioner • Full-Stack Developer

> “A good AI project doesn’t stop at training — it ships.”

⭐ If this project impressed you, consider starring it.

```

---
