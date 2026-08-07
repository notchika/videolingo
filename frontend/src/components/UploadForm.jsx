import { useRef, useState } from "react";

export default function UploadForm({ onFileSelected, selectedFile, duration }) {
  const inputRef = useRef(null);
  const [dragOver, setDragOver] = useState(false);

  function handleFiles(files) {
    if (files && files[0]) onFileSelected(files[0]);
  }

  return (
    <div className="panel">
      <label className="field-label">Video or audio file</label>
      <div
        className={`dropzone ${dragOver ? "dragover" : ""}`}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          handleFiles(e.dataTransfer.files);
        }}
      >
        <div className="dropzone-label">
          <strong>Click to browse</strong> or drag a video or audio file here
          <div style={{ marginTop: 6 }}>MP4, MOV, MKV, WEBM, MP3, WAV, M4A, AAC, OGG, FLAC · up to 25 minutes</div>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept="video/*,audio/*"
          hidden
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>

      {selectedFile && (
        <div className="file-chip" style={{ marginTop: 14 }}>
          <span>{selectedFile.name}</span>
          {duration != null && (
            <span className="duration">{Math.floor(duration / 60)}:{String(Math.round(duration % 60)).padStart(2, "0")}</span>
          )}
        </div>
      )}
    </div>
  );
}