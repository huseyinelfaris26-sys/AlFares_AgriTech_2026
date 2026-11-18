export default function ResultCard({ result }) {
  if (!result) return null;

  const isHealthy = result.disease === "Healthy";

  return (
    <div className={`result-card ${isHealthy ? "healthy" : "diseased"}`}>
      <h2>{isHealthy ? "✅ النبات سليم" : "⚠️ تم رصد مرض"}</h2>
      <div className="result-grid">
        <div>
          <strong>المحصول:</strong> {result.crop}
        </div>
        <div>
          <strong>المرض:</strong> {result.disease}
        </div>
        <div>
          <strong>الثقة:</strong> {(result.confidence * 100).toFixed(1)}%
        </div>
      </div>

      {!isHealthy && result.treatment && (
        <div className="treatment">
          <h3>🌿 العلاج العضوي</h3>
          <p>{result.treatment.organic}</p>
          <h3>🧪 العلاج الكيميائي</h3>
          <p>{result.treatment.chemical}</p>
          <h3>🛡️ الوقاية</h3>
          <p>{result.treatment.prevention}</p>
        </div>
      )}

      <details>
        <summary>Top 3 Diagnoses</summary>
        <ul>
          {result.top_3.map((t, i) => (
            <li key={i}>{t.label} — {(t.prob * 100).toFixed(1)}%</li>
          ))}
        </ul>
      </details>
    </div>
  );
}
