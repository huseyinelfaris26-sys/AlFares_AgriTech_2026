import { useState } from "react";
import { predictDisease } from "../services/api";

export default function UploadImage({ onResult }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const result = await predictDisease(file);
      onResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleUpload} className="upload-card">
      <label className="drop-zone">
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={(e) => setFile(e.target.files[0])}
          hidden
        />
        {file ? (
          <img src={URL.createObjectURL(file)} alt="preview" className="preview" />
        ) : (
          <span>📷 اضغط لاختيار صورة ورقة نبات</span>
        )}
      </label>
      <button type="submit" disabled={loading || !file}>
        {loading ? "⏳ جارٍ التحليل..." : "🔍 فحص الصورة"}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
