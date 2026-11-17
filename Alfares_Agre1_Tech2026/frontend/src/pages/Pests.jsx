import { useEffect, useState } from 'react'
import { getPestAlerts } from '../services/api'

export default function Pests() {
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    getPestAlerts().then(r => setAlerts(r.data)).catch(console.error)
  }, [])

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-green-900">مكافحة الآفات والأمراض</h2>
      <div className="space-y-3">
        {alerts.map(a => (
          <div key={a.id} className="card flex flex-col md:flex-row justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <span className={`w-3 h-3 rounded-full ${
                  a.severity === 'high' ? 'bg-red-500' :
                  a.severity === 'medium' ? 'bg-amber-500' : 'bg-green-500'
                }`}></span>
                <h3 className="font-bold">{a.pest_name}</h3>
              </div>
              <p className="text-sm text-gray-600 mt-1">الحقل: {a.field_id} • الثقة: {(a.confidence * 100).toFixed(0)}%</p>
              <p className="text-sm mt-2 text-green-800">{a.recommended_action}</p>
            </div>
            <div className="text-sm text-gray-500">
              {new Date(a.detected_at).toLocaleString('ar')}
            </div>
          </div>
        ))}
      </div>
      <div className="card bg-green-50 border border-green-200">
        <h3 className="font-bold mb-2">تحليل صورة بالذكاء الاصطناعي</h3>
        <p className="text-sm text-gray-600 mb-3">ارفع صورة لأوراق أو ثمار للكشف التلقائي عن الآفات والأمراض</p>
        <input type="file" accept="image/*" className="text-sm" />
      </div>
    </div>
  )
}
