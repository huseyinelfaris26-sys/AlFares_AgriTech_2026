const express = require('express');
const path = require('path');

const app = express();
const PORT = Number(process.env.PORT) || 3000;

// Demonstration data only. Replace with validated sensor/weather integrations before
// using measurements to make real irrigation or crop-management decisions.
const dashboardData = {
  summary: {
    status: 'مستقر',
    uptime: '99.7%',
    activeFields: 12,
    irrigationEfficiency: 88,
    soilSalinityRisk: 'منخفض',
    productivityIndex: 76,
    energySavings: 21,
    weatherWindow: 'مستقر خلال 72 ساعة'
  },
  regions: [
    { name: 'الرقة', area: '2,840 هكتار', productivity: 81, moisture: 62 },
    { name: 'الحسكة', area: '3,120 هكتار', productivity: 86, moisture: 68 },
    { name: 'دير الزور', area: '2,560 هكتار', productivity: 73, moisture: 58 }
  ],
  fields: [
    { id: 'F-101', name: 'حقل القمح الشرقي', region: 'الرقة', area: '180 هكتار', soilMoisture: 64, salinity: 2.4, irrigation: 'مجدول', efficiency: 92 },
    { id: 'F-102', name: 'مزرعة الذرة الشمالية', region: 'الحسكة', area: '220 هكتار', soilMoisture: 54, salinity: 3.1, irrigation: 'مستديم', efficiency: 81 },
    { id: 'F-103', name: 'مساحة الخضراوات', region: 'دير الزور', area: '140 هكتار', soilMoisture: 71, salinity: 2.1, irrigation: 'دقيق', efficiency: 94 },
    { id: 'F-104', name: 'حقل العدس الغربي', region: 'الرقة', area: '170 هكتار', soilMoisture: 48, salinity: 4.2, irrigation: 'مراقب', efficiency: 74 }
  ],
  alerts: [
    { id: 1, type: 'warning', title: 'زيادة ملوحة التربة', location: 'حقل العدس الغربي', severity: 'متوسط', detail: 'بيانات تجريبية: راجع القياس الميداني قبل اتخاذ إجراء.' },
    { id: 2, type: 'info', title: 'اكتشاف رطوبة مناسبة', location: 'مساحة الخضراوات', severity: 'منخفض', detail: 'بيانات تجريبية لمراقبة الري المتوازن.' },
    { id: 3, type: 'critical', title: 'انخفاض في تدفق المياه', location: 'مزرعة الذرة الشمالية', severity: 'عالي', detail: 'بيانات تجريبية: تحقق من الحساس ومصدر المياه.' }
  ],
  forecast: [
    { day: 'اليوم', rainfall: 0, temp: 29, recommendation: 'بيانات تجريبية؛ تحقق من التوقع المحلي' },
    { day: 'غدًا', rainfall: 2, temp: 27, recommendation: 'بيانات تجريبية؛ تحقق من التوقع المحلي' },
    { day: 'بعد غد', rainfall: 4, temp: 26, recommendation: 'بيانات تجريبية؛ تحقق من التوقع المحلي' },
    { day: 'بعد 3 أيام', rainfall: 1, temp: 30, recommendation: 'بيانات تجريبية؛ تحقق من التوقع المحلي' }
  ]
};

app.disable('x-powered-by');
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'no-referrer');
  res.setHeader('X-Frame-Options', 'DENY');
  next();
});
app.use(express.static(path.join(__dirname, 'public'), { maxAge: '1h' }));

app.get('/api/overview', (req, res) => res.json(dashboardData.summary));
app.get('/api/regions', (req, res) => res.json(dashboardData.regions));
app.get('/api/fields', (req, res) => res.json(dashboardData.fields));
app.get('/api/alerts', (req, res) => res.json(dashboardData.alerts));
app.get('/api/forecast', (req, res) => res.json(dashboardData.forecast));
app.get('/api/system', (req, res) => {
  res.json({ status: 'online', version: '1.1.0', dataMode: 'demo' });
});

app.get('/api/*', (req, res) => {
  res.status(404).json({ error: 'مسار API غير موجود' });
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`JaziraAgri-OS running at http://localhost:${PORT}`);
});
