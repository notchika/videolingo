import { useEffect, useRef, useState } from "react";
import UploadForm from "./components/UploadForm.jsx";
import LanguageSelector from "./components/LanguageSelector.jsx";
import JobStatus from "./components/JobStatus.jsx";
import { fetchLanguages, uploadMedia, startProcessing, getStatus } from "./api";

export default function App() {
  const [languages, setLanguages] = useState([]);
  const [file, setFile] = useState(null);
  const [duration, setDuration] = useState(null);
  const [targetLanguage, setTargetLanguage] = useState("");
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [uploadError, setUploadError] = useState(null);
  const [busy, setBusy] = useState(false);
  const pollRef = useRef(null);

  useEffect(() => {
    fetchLanguages().then(setLanguages).catch(() => setUploadError("Could not reach the server."));
    return () => clearInterval(pollRef.current);
  }, []);

  async function handleFileSelected(selected) {
    setFile(selected);
    setDuration(null);
    setUploadError(null);
    setJobId(null);
    setStatus(null);

    try {
      setBusy(true);
      const res = await uploadMedia(selected);
      setJobId(res.job_id);
      setDuration(res.duration_seconds);
    } catch (e) {
      setUploadError(e.message);
      setFile(null);
    } finally {
      setBusy(false);
    }
  }

  async function handleGenerate() {
    if (!jobId || !targetLanguage) return;
    setBusy(true);
    setUploadError(null);
    try {
      await startProcessing(jobId, targetLanguage);
      pollRef.current = setInterval(async () => {
        const s = await getStatus(jobId);
        setStatus(s);
        if (s.status === "done" || s.status === "failed") {
          clearInterval(pollRef.current);
          setBusy(false);
        }
      }, 1500);
    } catch (e) {
      setUploadError(e.message);
      setBusy(false);
    }
  }

  function handleReset() {
    clearInterval(pollRef.current);
    setFile(null);
    setDuration(null);
    setTargetLanguage("");
    setJobId(null);
    setStatus(null);
    setUploadError(null);
    setBusy(false);
  }

  const canGenerate = jobId && targetLanguage && !busy;
  const finished = status && (status.status === "done" || status.status === "failed");

  return (
    <>
      <p className="eyebrow">Video or audio → subtitles</p>
      <h1>VideoLingo</h1>
      <p className="subtitle">
        Upload a video or audio message under 25 minutes, pick a subtitle language,
        and get back a timestamped .srt / .vtt file — transcribed and translated locally.
      </p>

      <UploadForm onFileSelected={handleFileSelected} selectedFile={file} duration={duration} />

      {languages.length > 0 && (
        <LanguageSelector languages={languages} value={targetLanguage} onChange={setTargetLanguage} />
      )}

      {uploadError && <div className="error-box">{uploadError}</div>}

      {jobId && !status && (
        <button className="primary" disabled={!canGenerate} onClick={handleGenerate}>
          {busy ? "Working…" : "Generate subtitles"}
        </button>
      )}

      <JobStatus status={status} />

      {finished && (
        <button className="primary" style={{ marginTop: 4 }} onClick={handleReset}>
          Transcribe another file
        </button>
      )}
    </>
  );
}