import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Drones() {
  const [drones, setDrones] = useState([])
  const [missions, setMissions] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    drone_id: '',
    field_id: 1,
    mission_type: 'crop_health',
    altitude_m: 80,
    notes: ''
  })

  const load = () => {
    Promise.all([
      api.get('/drones/'),
      api.get('/drones/missions/list'),
      api.get('/drones/stats')
    ])
      .then(([d, m, s]) => {
        setDrones(d.data)
        setMissions(m.data)
        setStats(s.data)
        if (d.data.length) setForm(f => ({ ...f, drone_id: d.data[0].id }))
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const createMission = async (e) => {
    e.preventDefault()
    try {
      const res = await api.post('/drones/missions', {
        ...form,
        drone_id: Number(form.drone_id),
        field_id: Number(form.field_id),
        altitude_m: Number(form.altitude_m)
      })
      alert(res.data.message)
      setShowForm(false)
      load()
    } catch (err) {
      alert(err.response?.data?.detail || 'خطأ في جدولة المهمة')
    }
  }

  const startMission = async (id) => {
    try {
      await api.post(`/drones/missions/${id}/start`)
      load()
    } catch (err) {
      alert(err.response?.data?.detail || 'خطأ')
    }
  }

  const completeMission = async (id) => {
    try {
      await api.post(`/drones/missions/${id}/complete?images_count=135`)
      load()
    } catch (err) {
      alert(err.response?.data?.detail || 'خطأ')
    }
  }

  const statusColor = (s) => {
    const map = {
      idle: 'bg-green-100 text-green-800',
      flying: 'bg-blue-100 text-blue-800',
      charging: 'bg-amber-100 text-amber-800',
      maintenance: 'bg-gray-100 text-gray-700',
      offline: 'bg-red-100 text-red-800',
      planned: 'bg-purple-100 text-purple-800',
      in_progress: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800'
    }
    return map[s] || 'bg-gray-100'
  }

  const missionTypeAr = {
    mapping: 'رسم خرائط',
    crop_health: 'صحة المحصول',
    pest_scout: 'استكشاف آفات',
    irrigation_check: 'فحص الري',
    orthomosaic: 'أورثوموزاييك'
  }

  if (loading) return <div className="text-center py-20">جاري التحميل...</div>

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-green-900">الطائرات المسيرة</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          + جدولة مهمة جديدة
        </button>
      </div>

      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="card text-center">
            <div className="stat-value">{stats.total_drones}</div>
            <div className="text-sm text-gray-600">طائرات</div>
          </div>
          <div className="card text-center">
            <div className="stat-value text-blue-600">{stats.flying_now}</div>
            <div className="text-sm text-gray-600">في الجو الآن</div>
          </div>
          <div className="card text-center">
            <div className="stat-value">{stats.completed_missions}</div>
            <div className="text-sm text-gray-600">مهام مكتملة</div>
          </div>
          <div className="card text-center">
            <div className="stat-value">{stats.total_area_mapped_ha}</div>
            <div className="text-sm text-gray-600">هكتار ممسوح</div>
          </div>
        </div>
      )}

      {showForm && (
        <div className="card border-2 border-green-200">
          <h3 className="font-bold mb-4">جدولة مهمة طيران</h3>
          <form onSubmit={createMission} className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">الطائرة</label>
              <select
                className="w-full mt-1 border rounded-lg p-2"
                value={form.drone_id}
                onChange={e => setForm({ ...form, drone_id: e.target.value })}
              >
                {drones.map(d => (
                  <option key={d.id} value={d.id}>{d.name} ({d.model}) — {d.status}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">نوع المهمة</label>
              <select
                className="w-full mt-1 border rounded-lg p-2"
                value={form.mission_type}
                onChange={e => setForm({ ...form, mission_type: e.target.value })}
              >
                <option value="crop_health">صحة المحصول</option>
                <option value="pest_scout">استكشاف آفات</option>
                <option value="mapping">رسم خرائط</option>
                <option value="irrigation_check">فحص الري</option>
                <option value="orthomosaic">أورثوموزاييك</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">رقم الحقل</label>
              <input
                type="number"
                className="w-full mt-1 border rounded-lg p-2"
                value={form.field_id}
                onChange={e => setForm({ ...form, field_id: e.target.value })}
              />
            </div>
            <div>
              <label className="text-sm font-medium">الارتفاع (متر)</label>
              <input
                type="number"
                className="w-full mt-1 border rounded-lg p-2"
                value={form.altitude_m}
                onChange={e => setForm({ ...form, altitude_m: e.target.value })}
              />
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium">ملاحظات</label>
              <input
                type="text"
                className="w-full mt-1 border rounded-lg p-2"
                value={form.notes}
                onChange={e => setForm({ ...form, notes: e.target.value })}
                placeholder="اختياري"
              />
            </div>
            <div className="md:col-span-2 flex gap-3">
              <button type="submit" className="btn-primary">حفظ المهمة</button>
              <button type="button" onClick={() => setShowForm(false)} className="text-gray-600">إلغاء</button>
            </div>
          </form>
        </div>
      )}

      <div>
        <h3 className="font-bold text-lg mb-3">أسطول الطائرات</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {drones.map(d => (
            <div key={d.id} className="card flex items-start gap-4">
              <div className="text-4xl">🚁</div>
              <div className="flex-1">
                <div className="flex justify-between">
                  <h4 className="font-bold">{d.name}</h4>
                  <span className={`text-xs px-2 py-1 rounded-full ${statusColor(d.status)}`}>
                    {d.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{d.model}</p>
                <div className="mt-2 text-sm space-y-1">
                  <div>🔋 البطارية: <strong>{d.battery_level}%</strong></div>
                  <div>📷 الكاميرا: {d.camera_type}</div>
                  <div>⏱️ أقصى طيران: {d.max_flight_time_min} دقيقة</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="font-bold text-lg mb-3">سجل المهام</h3>
        <div className="space-y-3">
          {missions.map(m => (
            <div key={m.id} className="card flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className={`text-xs px-2 py-0.5 rounded-full ${statusColor(m.status)}`}>
                    {m.status}
                  </span>
                  <strong>{missionTypeAr[m.mission_type] || m.mission_type}</strong>
                </div>
                <div className="text-sm text-gray-600 mt-1">
                  {m.drone_name} → {m.field_name}
                  {m.area_covered_ha && ` • ${m.area_covered_ha} هكتار`}
                  {m.images_captured > 0 && ` • ${m.images_captured} صورة`}
                </div>
                {m.notes && <div className="text-xs text-gray-500 mt-1">{m.notes}</div>}
              </div>
              <div className="flex gap-2">
                {m.status === 'planned' && (
                  <button onClick={() => startMission(m.id)} className="text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-lg">
                    بدء
                  </button>
                )}
                {m.status === 'in_progress' && (
                  <button onClick={() => completeMission(m.id)} className="text-sm bg-green-100 text-green-800 px-3 py-1 rounded-lg">
                    إكمال
                  </button>
                )}
              </div>
            </div>
          ))}
          {missions.length === 0 && <p className="text-gray-500 text-sm">لا توجد مهام بعد</p>}
        </div>
      </div>
    </div>
  )
              }
