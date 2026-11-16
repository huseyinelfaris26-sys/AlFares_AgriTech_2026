const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

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
    { id: 1, type: 'warning', title: 'زيادة ملوحة التربة', location: 'حقل العدس الغربي', severity: 'متوسط', detail: 'يج�� تقليل الري خلال الـ 24 ساعة القادمة.' },
    { id: 2, type: 'info', title: 'اكتشاف رطوبة مناسبة', location: 'مساحة الخضراوات', severity: 'منخفض', detail: 'المنطقة مناسبة للري المتوازن.' },
    { id: 3, type: 'critical', title: 'انخفاض في تدفق المياه', location: 'مزرعة الذرة الشمالية', severity: 'عالي', detail: 'تم تفعيل تنبيه التوازن المائي.' }
  ],
  forecast: [
    { day: 'اليوم', rainfall: 0, temp: 29, recommendation: 'تجنب الري الزيادة' },
    { day: 'غدًا', rainfall: 2, temp: 27, recommendation: 'ري خفيف' },
    { day: 'بعد غد', rainfall: 4, temp: 26, recommendation: 'مراقبة تملح التربة' },
    { day: 'في 3 أيام', rainfall: 1, temp: 30, recommendation: 'توزيع متوازن' }
  ]
};

app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/overview', (req, res) => {
  res.json(dashboardData.summary);
});

app.get('/api/regions', (req, res) => {
  res.json(dashboardData.regions);
});

app.get('/api/fields', (req, res) => {
  res.json(dashboardData.fields);
});

app.get('/api/alerts', (req, res) => {
  res.json(dashboardData.alerts);
});

app.get('/api/forecast', (req, res) => {
  res.json(dashboardData.forecast);
});

app.get('/api/system', (req, res) => {
  res.json({
    status: 'online',
    environment: 'production',
    version: '1.0.0',
    lastSync: '2026-11-16T16:40:00Z'
  });
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`JaziraAgri-OS running at http://localhost:${PORT}`);
});
