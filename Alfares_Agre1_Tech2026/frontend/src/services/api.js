import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 15000,
})

export const getDashboard = () => api.get('/dashboard/summary')
export const getKPIs = () => api.get('/dashboard/kpis')
export const getFields = () => api.get('/fields/')
export const getCrops = () => api.get('/crops/')
export const getIrrigationStatus = (fieldId) => api.get(`/irrigation/status/${fieldId}`)
export const getPestAlerts = () => api.get('/pests/alerts')
export const getWeather = () => api.get('/weather/current')
export const getForecast = () => api.get('/weather/forecast')
export const getNDVI = (fieldId) => api.get(`/satellite/ndvi/${fieldId}`)
export const predictYield = (data) => api.post('/ai/yield-prediction', data)

export default api
