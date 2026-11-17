import { useState } from 'react'
import { predictYield } from '../services/api'

export default function AI() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handlePredict = async () => {
    setLoading(true)
    try {
      const res = await predictYield({
        field_id: 'fld-001',
        crop_type: 'قمح',
        area_hectares: 12.5,
        planting_date: '2026-11-01',
        soil_quality: 0.82,
        irrigation_score: 0.88
      })
      setResult(res.data)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-green-900">الذكاء الاصطناعي والتحليلات</h2>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-bold text-lg mb-3">تنبؤ الإنتاجية</h3>
          <p className="text-sm text-gray-600 mb-4">نموذج تعلم آلي يعتمد على بيانات التربة والري والطقس والتاريخ الزراعي</p>
          <button className="btn-primary" onClick={handlePredict} disabled={loading}>
            {loading ? 'جاري الحساب...' : 'احسب التوقعات'}
          </button>
          {result && (
            <div className="mt-4 p-4 bg-green-50 rounded-lg">
              <div className="text-3xl font-bold text-green-800">{result.predicted_yield_ton_ha} طن/هكتار</div>
              <div className="text-sm mt-1">الإجمالي المتوقع: {result.total_predicted_tons} طن</div>
              <div className="text-xs text-gray-500 mt-2">الثقة: {(result.confidence * 100).toFixed(0)}%</div>
            </div>
          )}
        </div>

        <div className="card">
          <h3 className="font-bold text-lg mb-3">مراقبة صحة المحاصيل</h3>
          <ul className="text-sm space-y-2 text-gray-700">
            <li>✅ تحليل صور جوية بالـ AI</li>
            <li>✅ عد النباتات ورسم خرائط الكثافة</li>
            <li>✅ كشف الحالات الشاذة مبكرًا</li>
            <li>✅ تكامل مع الطائرات المسيرة والأقمار الصناعية</li>
            <li>✅ تنبيهات فورية عند انخفاض الصحة</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
