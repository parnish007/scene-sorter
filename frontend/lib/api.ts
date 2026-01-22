export type ImagePrediction = {
  filename: string;
  label: string;
  confidence: number;
};

export type BatchPredictResponse = {
  job_id: string;
  summary: {
    total: number;
    by_class: Record<string, number>;
  };
  results: ImagePrediction[];
  download_url: string; // relative like /download/{job_id}
};

function getApiBaseUrl(): string {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!base) {
    // Fallback for dev if env missing
    return "http://localhost:8000";
  }
  return base.replace(/\/+$/, "");
}

export async function batchPredict(files: File[]): Promise<{
  data: BatchPredictResponse;
  downloadUrl: string; // absolute URL
}> {
  const apiBaseUrl = getApiBaseUrl();

  const form = new FormData();
  for (const f of files) {
    // Backend expects: files: List[UploadFile] = File(...)
    form.append("files", f);
  }

  const res = await fetch(`${apiBaseUrl}/predict/batch`, {
    method: "POST",
    body: form
  });

  if (!res.ok) {
    let detail = `Request failed with status ${res.status}`;
    try {
      const payload = await res.json();
      if (payload?.detail) detail = payload.detail;
    } catch {
      // ignore
    }
    throw new Error(detail);
  }

  const data = (await res.json()) as BatchPredictResponse;

  const downloadUrl = data.download_url.startsWith("http")
    ? data.download_url
    : `${apiBaseUrl}${data.download_url}`;

  return { data, downloadUrl };
}
