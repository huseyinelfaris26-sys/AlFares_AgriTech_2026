import { useEffect, useState } from 'react'
import { getCrops } from '../services/api'

export default function Crops() {
  const [crops, setCrops] = useState([])

  useEffect(() => {
    getCrops().then(r => setCrops(r.data)).catch(console.error)
  }, [])

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-green-900">تخطيط المحاصيل</h2>
      <div className="grid gap-4">
        {crops.map(c => (
          <div key={c.id} className="card flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h3 className="font-bold text-lg">{c.name}</h3>
              <p className="text-sm text-gray-500">{c.scientific_name} • صنف: {c.variety}</p>
              <div className="mt-2 flex gap-4 text-sm">
                <span>📅 الزراعة: {c.planting_date}</span>
                <span>🎯 الهدف: {c.target_yield} طن/هكتار</span>
              </div>
            </div>
            <div className="text-left">
              <span className="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                {c.growth_stage}
              </span>
              <div className="text-sm text-gray-500 mt-1">الحالة: {c.current_status}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
