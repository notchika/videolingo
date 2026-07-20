const BASE_URL = "http://localhost:8000";

export async function fetchLanguages() {
  const res = await fetch(`${BASE_URL}/languages`);
  if (!res.ok) throw new Error("Failed to load languages");
  return res.json();
}

export async function uploadVideo(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE_URL}/upload`, { method: "POST", body: form });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(err.detail || "Upload failed");
  }
  return res.json();
}

export async function startProcessing(jobId, targetLanguage) {
  const res = await fetch(`${BASE_URL}/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ job_id: jobId, target_language: targetLanguage }),
  });
  if (!res.ok) throw new Error("Failed to start processing");
  return res.json();
}

export async function getStatus(jobId) {
  const res = await fetch(`${BASE_URL}/status/${jobId}`);
  if (!res.ok) throw new Error("Failed to fetch status");
  return res.json();
}

export function downloadUrl(jobId, format) {
  return `${BASE_URL}/download/${jobId}/${format}`;
}