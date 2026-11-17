import { useEffect, useState } from 'react'
import { getIrrigationStatus } from '../services/api'

export default function Irrigation() {
  const [status, setStatus] = useState(null)

  useEffect(() => {
    getIrrigationStatus('fld-001').then(r => setStatus(r.data)).catch(console.error)
  }, [])

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-green-900">الري والتسميد الدقيق</h2>
      
      {status && (
        <div className="grid md:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="font-bold mb-4">حالة الرطوبة — الحقل الشمالي</h3>
            <div className="text-center mb-4">
              <div className="text-5xl font-bold text-blue-600">{status.soil_moisture}%</div>
              <div className="text-sm text-gray-500">النطاق الأمثل: {status.optimal_range[0]}% – {status.optimal_range[1]}%</div>
            </div>
            <div className="space-y-2">
              {status.sensors.map(s => (
                <div key={s.id} className="flex justify-between text-sm bg-blue-50 p-2 rounded">
                  <span>عمق {s.depth_cm} سم</span>
                  <strong>{s.moisture}%</strong>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3 className="font-bold mb-4">التوصيات</h3>
            <div className="space-y-3">
              <div className="p-3 bg-blue-50 rounded-lg">
                <div className="font-medium">💧 الري</div>
                <div className="text-sm">ري خفيف 12 مم — الرطوبة تقترب من الحد الأدنى</div>
              </div>
              <div className="p-3 bg-green-50 rounded-lg">
                <div className="font-medium">🧪 التسميد</div>
                <div className="text-sm">إضافة 25 كغ/هكتار نيتروجين خلال 3 أيام</div>
              </div>
            </div>
            <button className="btn-primary mt-4 w-full">جدولة ري جديد</button>
          </div>
        </div>
      )}
    </div>
  )
}
