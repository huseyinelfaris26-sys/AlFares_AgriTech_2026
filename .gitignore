const apiRoutes = {
  overview: '/api/overview',
  regions: '/api/regions',
  fields: '/api/fields',
  alerts: '/api/alerts',
  forecast: '/api/forecast'
};

async function loadData() {
  const [summary, regions, fields, alerts, forecast] = await Promise.all([
    fetch(apiRoutes.overview).then((res) => res.json()),
    fetch(apiRoutes.regions).then((res) => res.json()),
    fetch(apiRoutes.fields).then((res) => res.json()),
    fetch(apiRoutes.alerts).then((res) => res.json()),
    fetch(apiRoutes.forecast).then((res) => res.json())
  ]);

  renderSummary(summary);
  renderRegions(regions);
  renderFields(fields);
  renderAlerts(alerts);
  renderForecast(forecast);
}

function renderSummary(summary) {
  const cards = [
    { label: 'الحالة', value: summary.status, trend: 'مستقر' },
    { label: 'وقت التشغيل', value: summary.uptime, trend: '++ 1.4%' },
    { label: 'الحقول النشطة', value: summary.activeFields, trend: '12 مجمعة' },
    { label: 'كفاءة الري', value: `${summary.irrigationEfficiency}%`, trend: '+8%' },
    { label: 'مخاطر الملوحة', value: summary.soilSalinityRisk, trend: 'مراقبة' },
    { label: 'مؤشر الإنتاج', value: `${summary.productivityIndex}%`, trend: '+4%' }
  ];

  const container = document.getElementById('summary-cards');
  container.innerHTML = cards.map((card) => `
    <div class="stat-card">
      <span class="stat-label">${card.label}</span>
      <div class="stat-value">${card.value}</div>
      <span class="stat-trend">${card.trend}</span>
    </div>
  `).join('');
}

function renderRegions(regions) {
  const container = document.getElementById('regions-grid');
  container.innerHTML = regions.map((region) => `
    <div class="region-card">
      <h4>${region.name}</h4>
      <p>${region.area}</p>
      <div class="meter"><span style="width:${region.productivity}%"></span></div>
      <p>إنتاجية: ${region.productivity}%</p>
      <p>رطوبة: ${region.moisture}%</p>
    </div>
  `).join('');
}

function renderFields(fields) {
  const container = document.getElementById('fields-table');
  container.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>الحقل</th>
          <th>المنطقة</th>
          <th>الرطوبة</th>
          <th>الملوحة</th>
          <th>الري</th>
          <th>الكفاءة</th>
        </tr>
      </thead>
      <tbody>
        ${fields.map((field) => {
          const badgeClass = field.efficiency >= 85 ? 'good' : field.efficiency >= 75 ? 'warn' : 'alert';
          return `
            <tr>
              <td>${field.name}</td>
              <td>${field.region}</td>
              <td>${field.soilMoisture}%</td>
              <td>${field.salinity} ds/m</td>
              <td>${field.irrigation}</td>
              <td><span class="badge ${badgeClass}">${field.efficiency}%</span></td>
            </tr>
          `;
        }).join('')}
      </tbody>
    </table>
  `;
}

function renderAlerts(alerts) {
  const container = document.getElementById('alerts-list');
  container.innerHTML = alerts.map((alert) => `
    <div class="alert-item ${alert.type === 'critical' ? 'critical' : alert.type === 'warning' ? 'warning' : 'info'}">
      <h4>${alert.title}</h4>
      <p>${alert.location} • ${alert.severity}</p>
      <small>${alert.detail}</small>
    </div>
  `).join('');
}

function renderForecast(forecast) {
  const container = document.getElementById('forecast-grid');
  container.innerHTML = forecast.map((item) => `
    <div class="forecast-item">
      <strong>${item.day}</strong>
      <div>الأمطار: ${item.rainfall} مم</div>
      <div>الحرارة: ${item.temp}°</div>
      <div>توصية: ${item.recommendation}</div>
    </div>
  `).join('');
}

loadData().catch((error) => {
  console.error('Failed to load dashboard data', error);
  document.getElementById('summary-cards').innerHTML = '<div class="stat-card"><span class="stat-label">خطأ</span><div class="stat-value">تعذر تحميل البيانات</div></div>';
});
