import { useEffect, useState } from 'react'
import { getDashboard, getKPIs } from '../services/api'

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [kpis, setKpis] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getDashboard(), getKPIs()])
      .then(([s, k]) => {
        setSummary(s.data)
        setKpis(k.data)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20 text-green-700">جاري تحميل البيانات...</div>
  if (!summary) return <div className="text-center py-20">تعذر الاتصال بالخادم. تأكد من تشغيل الـ Backend.</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-green-900">لوحة التحكم</h2>
        <span className="text-sm text-gray-500">آخر تحديث: {new Date(summary.last_update).toLocaleString('ar')}</span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <div className="text-3xl mb-1">🌾</div>
          <div className="stat-value">{summary.total_fields}</div>
          <div className="text-sm text-gray-600">حقول نشطة</div>
        </div>
        <div className="card text-center">
          <div className="text-3xl mb-1">🌱</div>
          <div className="stat-value">{summary.active_crops}</div>
          <div className="text-sm text-gray-600">محاصيل حالية</div>
        </div>
        <div className="card text-center">
          <div className="text-3xl mb-1">💚</div>
          <div className="stat-value">{summary.health_score}%</div>
          <div className="text-sm text-gray-600">صحة المزرعة</div>
        </div>
        <div className="card text-center">
          <div className="text-3xl mb-1">🔔</div>
          <div className="stat-value text-amber-600">{summary.alerts_count}</div>
          <div className="text-sm text-gray-600">تنبيهات</div>
        </div>
      </div>

      {kpis && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="card">
            <div className="text-sm text-gray-500">توقعات الإنتاجية</div>
            <div className="stat-value">{kpis.yield_prediction} طن/هكتار</div>
          </div>
          <div className="card">
            <div className="text-sm text-gray-500">كفاءة المياه</div>
            <div className="stat-value">{kpis.water_efficiency}%</div>
          </div>
          <div className="card">
            <div className="text-sm text-gray-500">توفير الأسمدة</div>
            <div className="stat-value">{kpis.fertilizer_savings}%</div>
          </div>
          <div className="card">
            <div className="text-sm text-gray-500">مستشعرات IoT</div>
            <div className="stat-value">{kpis.iot_sensors_online}</div>
          </div>
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-bold text-lg mb-3">الطقس الحالي</h3>
          <div className="flex items-center gap-4">
            <div className="text-5xl">☀️</div>
            <div>
              <div className="text-3xl font-bold">{summary.weather_summary.temp}°C</div>
              <div className="text-gray-600">{summary.weather_summary.condition}</div>
              <div className="text-sm">رطوبة {summary.weather_summary.humidity}% • احتمال مطر {summary.weather_summary.rain_probability}%</div>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="font-bold text-lg mb-3">التنبيهات الأخيرة</h3>
          <div className="space-y-2">
            {summary.recent_alerts.map(a => (
              <div key={a.id} className={`p-3 rounded-lg text-sm ${
                a.severity === 'high' ? 'bg-red-50 border-r-4 border-red-500' :
                a.severity === 'medium' ? 'bg-amber-50 border-r-4 border-amber-500' :
                'bg-blue-50 border-r-4 border-blue-400'
              }`}>
                <div className="font-medium">{a.message}</div>
                <div className="text-xs text-gray-500 mt-1">{a.time}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
