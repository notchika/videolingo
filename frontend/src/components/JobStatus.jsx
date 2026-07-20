import { downloadUrl } from "../api";

const STAGES = ["extracting_audio", "transcribing", "translating", "generating_subtitles", "done"];

const STAGE_LABELS = {
  extracting_audio: "Audio",
  transcribing: "Transcribe",
  translating: "Translate",
  generating_subtitles: "Subtitles",
  done: "Done",
};

export default function JobStatus({ status }) {
  if (!status) return null;

  const currentIndex = STAGES.indexOf(status.status);
  const failed = status.status === "failed";

  return (
    <div className="panel">
      <div className="cue-timeline">
        {STAGES.map((stage, i) => {
          let cls = "cue-block";
          if (failed && i === Math.max(currentIndex, 0)) cls += " failed";
          else if (i < currentIndex || status.status === "done") cls += " done";
          else if (i === currentIndex) cls += " active";
          return <div key={stage} className={cls} title={STAGE_LABELS[stage]} />;
        })}
      </div>

      <div className="status-row">
        <span className="message">{status.progress_message}</span>
        <span>{status.status}</span>
      </div>

      {status.detected_source_language && (
        <div className="detected-lang">
          Detected source language: {status.detected_source_language}
        </div>
      )}

      {failed && status.error && (
        <div className="error-box">{status.error}</div>
      )}

      {status.status === "done" && (
        <div className="download-row">
          <a className="download-btn" href={downloadUrl(status.job_id, "srt")}>Download .srt</a>
          <a className="download-btn" href={downloadUrl(status.job_id, "vtt")}>Download .vtt</a>
        </div>
      )}
    </div>
  );
}