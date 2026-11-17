import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Pricing() {
  const [plans, setPlans] = useState([])
  const [billing, setBilling] = useState('monthly')
  const [loading, setLoading] = useState(true)
  const [subscribing, setSubscribing] = useState(null)

  useEffect(() => {
    api.get('/pricing/plans')
      .then(r => setPlans(r.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const handleSubscribe = async (planId) => {
    setSubscribing(planId)
    try {
      const res = await api.post('/pricing/subscribe', {
        plan_id: planId,
        billing_cycle: billing,
        user_id: 2
      })
      alert(res.data.message + '\nالمبلغ: $' + res.data.amount)
    } catch (e) {
      alert('حدث خطأ في الاشتراك')
    } finally {
      setSubscribing(null)
    }
  }

  if (loading) return <div className="text-center py-20 text-green-700">جاري تحميل الخطط...</div>

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-green-900">خطط الأسعار</h2>
        <p className="text-gray-600 mt-2">اختر الخطة المناسبة لحجم مزرعتك واحتياجاتك</p>

        <div className="inline-flex mt-6 bg-green-100 rounded-full p-1">
          <button
            onClick={() => setBilling('monthly')}
            className={`px-5 py-2 rounded-full text-sm font-medium transition ${
              billing === 'monthly' ? 'bg-green-700 text-white' : 'text-green-800'
            }`}
          >
            شهري
          </button>
          <button
            onClick={() => setBilling('yearly')}
            className={`px-5 py-2 rounded-full text-sm font-medium transition ${
              billing === 'yearly' ? 'bg-green-700 text-white' : 'text-green-800'
            }`}
          >
            سنوي <span className="text-xs opacity-80">(وفر حتى 17%)</span>
          </button>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {plans.map(plan => {
          const price = billing === 'yearly' ? plan.price_yearly : plan.price_monthly
          const period = billing === 'yearly' ? 'سنة' : 'شهر'
          return (
            <div
              key={plan.id}
              className={`card relative flex flex-col ${
                plan.is_popular ? 'ring-2 ring-green-600 shadow-xl scale-[1.02]' : ''
              }`}
            >
              {plan.is_popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-green-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                  الأكثر شيوعًا
                </div>
              )}

              <div className="text-center mb-4">
                <h3 className="text-xl font-bold text-green-900">{plan.name_ar}</h3>
                <p className="text-sm text-gray-500 mt-1">{plan.description_ar}</p>
              </div>

              <div className="text-center mb-6">
                <span className="text-4xl font-extrabold text-green-800">${price}</span>
                <span className="text-gray-500"> / {period}</span>
                {billing === 'yearly' && (
                  <div className="text-xs text-green-600 mt-1">توفير {plan.savings_yearly_percent}%</div>
                )}
              </div>

              <ul className="space-y-2 text-sm flex-1 mb-6">
                <li className="flex items-center gap-2">
                  <span className="text-green-600">✓</span>
                  حتى {plan.max_fields === 999 ? 'غير محدود' : plan.max_fields} حقل
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-600">✓</span>
                  حتى {plan.max_drones} طائرة مسيرة
                </li>
                <li className="flex items-center gap-2">
                  <span className="text-green-600">✓</span>
                  حتى {plan.max_sensors} مستشعر IoT
                </li>
                {plan.features_ar && Object.entries(plan.features_ar).map(([key, val]) => (
                  val === true || typeof val === 'string' ? (
                    <li key={key} className="flex items-center gap-2">
                      <span className="text-green-600">✓</span>
                      {key}{typeof val === 'string' ? `: ${val}` : ''}
                    </li>
                  ) : null
                ))}
              </ul>

              <button
                onClick={() => handleSubscribe(plan.id)}
                disabled={subscribing === plan.id}
                className={`w-full py-3 rounded-xl font-bold transition ${
                  plan.is_popular
                    ? 'bg-green-700 text-white hover:bg-green-800'
                    : 'bg-green-100 text-green-800 hover:bg-green-200'
                }`}
              >
                {subscribing === plan.id ? 'جاري الاشتراك...' : 'اشترك الآن'}
              </button>
            </div>
          )
        })}
      </div>

      <div className="card bg-green-50 border border-green-200 text-center">
        <h3 className="font-bold text-lg text-green-900">هل تحتاج حلاً مخصصًا؟</h3>
        <p className="text-sm text-gray-600 mt-2">
          للشركات الزراعية الكبيرة ووكلاء المعدات والمربّين — نقدم أسعارًا مخصصة وحلولًا متكاملة.
        </p>
        <button className="mt-4 text-green-700 font-medium underline">تواصل معنا</button>
      </div>
    </div>
  )
}
