import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Fields from './pages/Fields'
import Crops from './pages/Crops'
import Irrigation from './pages/Irrigation'
import Pests from './pages/Pests'
import AI from './pages/AI'
import Pricing from './pages/Pricing'
import Drones from './pages/Drones'
import './styles/index.css'

function Layout({ children }) {
  const navItems = [
    { to: '/', label: 'لوحة التحكم', icon: '📊' },
    { to: '/fields', label: 'الحقول', icon: '🌾' },
    { to: '/crops', label: 'المحاصيل', icon: '🌱' },
    { to: '/irrigation', label: 'الري والتسميد', icon: '💧' },
    { to: '/pests', label: 'الآفات', icon: '🐛' },
    { to: '/drones', label: 'الطائرات', icon: '🚁' },
    { to: '/ai', label: 'الذكاء الاصطناعي', icon: '🤖' },
    { to: '/pricing', label: 'الأسعار', icon: '💰' },
  ]

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-gradient-to-l from-green-800 to-green-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🌾</span>
            <div>
              <h1 className="text-xl font-bold">Alfares Agri Tech 2026</h1>
              <p className="text-green-100 text-sm">منصة الفارس للزراعة الذكية</p>
            </div>
          </div>
          <div className="text-sm bg-white/20 px-3 py-1 rounded-full">
            مزرعة تجريبية • متصل
          </div>
        </div>
      </header>

      <nav className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 flex gap-1 overflow-x-auto">
          {navItems.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `px-4 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${
                  isActive
                    ? 'border-green-600 text-green-700'
                    : 'border-transparent text-gray-600 hover:text-green-700'
                }`
              }
            >
              <span className="ml-1">{item.icon}</span> {item.label}
            </NavLink>
          ))}
        </div>
      </nav>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6">
        {children}
      </main>

      <footer className="bg-green-900 text-green-100 text-center py-4 text-sm">
        © 2026 Alfares_Agreı_Tech2026 — منصة زراعية ذكية متكاملة
      </footer>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/fields" element={<Fields />} />
          <Route path="/crops" element={<Crops />} />
          <Route path="/irrigation" element={<Irrigation />} />
          <Route path="/pests" element={<Pests />} />
          <Route path="/drones" element={<Drones />} />
          <Route path="/ai" element={<AI />} />
          <Route path="/pricing" element={<Pricing />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
