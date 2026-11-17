import { useEffect, useState } from 'react'
import { getFields } from '../services/api'

export default function Fields() {
  const [fields, setFields] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getFields()
      .then(r => setFields(r.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-12">جاري التحميل...</div>

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-green-900">إدارة الحقول</h2>
        <button className="btn-primary">+ إضافة حقل جديد</button>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {fields.map(f => (
          <div key={f.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-3">
              <h3 className="font-bold text-lg">{f.name}</h3>
              <span className={`text-xs px-2 py-1 rounded-full ${
                f.health_score >= 85 ? 'bg-green-100 text-green-800' :
                f.health_score >= 70 ? 'bg-amber-100 text-amber-800' :
                'bg-red-100 text-red-800'
              }`}>
                صحة {f.health_score}%
              </span>
            </div>
            <div className="space-y-1 text-sm text-gray-600">
              <div>📐 المساحة: <strong>{f.area_hectares} هكتار</strong></div>
              <div>🌱 المحصول: <strong>{f.crop_type}</strong></div>
              <div>🪨 التربة: {f.soil_type}</div>
              <div>📡 المستشعرات: {f.sensors_count}</div>
              <div>💧 آخر ري: {f.last_irrigation ? new Date(f.last_irrigation).toLocaleDateString('ar') : '—'}</div>
            </div>
            <div className="mt-4 flex gap-2">
              <button className="text-sm text-green-700 font-medium">التفاصيل</button>
              <button className="text-sm text-gray-500">خريطة</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
