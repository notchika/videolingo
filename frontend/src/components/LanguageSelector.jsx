export default function LanguageSelector({ languages, value, onChange }) {
  return (
    <div className="panel">
      <label className="field-label">Subtitle language</label>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="" disabled>Choose a language</option>
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>{lang.name}</option>
        ))}
      </select>
    </div>
  );
}