const routes = {
  overview: '/api/overview',
  regions: '/api/regions',
  fields: '/api/fields',
  alerts: '/api/alerts',
  forecast: '/api/forecast'
};

let fieldData = [];
const numberFormat = new Intl.NumberFormat('ar');

async function getJson(url) {
  const response = await fetch(url, { headers: { Accept: 'application/json' } });
  if (!response.ok) throw new Error(`تعذر تحميل البيانات (${response.status})`);
  return response.json();
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[char]);
}

function setStatus(message, state = '') {
  const status = document.getElementById('status-message');
  status.textContent = message;
  status.className = `status-message ${state}`.trim();
}

function renderSummary(summary) {
  const cards = [
    ['حالة النظام', summary.status, 'مؤشر تجريبي'],
    ['وقت التشغيل', summary.uptime, 'بيانات توضيحية'],
    ['الحقول النشطة', numberFormat.format(summary.activeFields), 'ضمن العينة'],
    ['كفاءة الري', `${numberFormat.format(summary.irrigationEfficiency)}٪`, 'مؤشر توضيحي'],
    ['مخاطر الملوحة', summary.soilSalinityRisk, 'تتطلب قياسًا ميدانيًا'],
    ['مؤشر الإنتاج', `${numberFormat.format(summary.productivityIndex)}٪`, 'مؤشر توضيحي']
  ];
  document.getElementById('summary-cards').innerHTML = cards.map(([label, value, note]) => `
    <article class="stat-card"><span class="stat-label">${escapeHtml(label)}</span>
      <strong class="stat-value">${escapeHtml(value)}</strong><span class="stat-trend">${escapeHtml(note)}</span></article>
  `).join('');
}

function renderRegions(regions) {
  document.getElementById('regions-grid').innerHTML = regions.map((region) => {
    const productivity = Math.max(0, Math.min(100, Number(region.productivity) || 0));
    return `<article class="region-card"><div class="region-heading"><h3>${escapeHtml(region.name)}</h3><span>${escapeHtml(region.area)}</span></div>
      <div class="meter" role="progressbar" aria-label="مؤشر الإنتاجية" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${productivity}"><span style="width:${productivity}%"></span></div>
      <div class="region-metrics"><span>الإنتاجية <b>${numberFormat.format(productivity)}٪</b></span><span>الرطوبة <b>${numberFormat.format(region.moisture)}٪</b></span></div></article>`;
  }).join('');
}

function renderFields(fields) {
  fieldData = Array.isArray(fields) ? fields : [];
  document.getElementById('field-count').textContent = `${numberFormat.format(fieldData.length)} حقول في العينة`;
  filterFields();
}

function filterFields() {
  const query = document.getElementById('field-search').value.trim().toLocaleLowerCase('ar');
  const filtered = fieldData.filter((field) => `${field.name} ${field.region} ${field.id}`.toLocaleLowerCase('ar').includes(query));
  const container = document.getElementById('fields-table');
  if (!filtered.length) {
    container.innerHTML = '<p class="empty-state">لا توجد حقول تطابق البحث.</p>';
    return;
  }
  container.innerHTML = `<table><thead><tr><th>الحقل</th><th>المنطقة</th><th>الرطوبة</th><th>الملوحة</th><th>الري</th><th>الكفاءة</th></tr></thead><tbody>${filtered.map((field) => {
    const efficiency = Number(field.efficiency) || 0;
    const badge = efficiency >= 85 ? 'good' : efficiency >= 75 ? 'warn' : 'alert';
    return `<tr><td><strong>${escapeHtml(field.name)}</strong><small>${escapeHtml(field.id)} · ${escapeHtml(field.area)}</small></td><td>${escapeHtml(field.region)}</td><td>${numberFormat.format(field.soilMoisture)}٪</td><td>${escapeHtml(field.salinity)} dS/m</td><td>${escapeHtml(field.irrigation)}</td><td><span class="badge ${badge}">${numberFormat.format(efficiency)}٪</span></td></tr>`;
  }).join('')}</tbody></table>`;
}

function renderAlerts(alerts) {
  document.getElementById('alert-count').textContent = `${numberFormat.format(alerts.length)} تنبيهات تجريبية`;
  document.getElementById('alerts-list').innerHTML = alerts.map((alert) => {
    const type = ['critical', 'warning', 'info'].includes(alert.type) ? alert.type : 'info';
    return `<article class="alert-item ${type}"><div class="alert-title"><h3>${escapeHtml(alert.title)}</h3><span class="badge ${type === 'critical' ? 'alert' : type === 'warning' ? 'warn' : 'good'}">${escapeHtml(alert.severity)}</span></div><p>${escapeHtml(alert.location)}</p><small>${escapeHtml(alert.detail)}</small></article>`;
  }).join('');
}

function renderForecast(forecast) {
  document.getElementById('forecast-grid').innerHTML = forecast.map((item) => `
    <article class="forecast-item"><strong>${escapeHtml(item.day)}</strong><span>🌧 ${numberFormat.format(item.rainfall)} مم</span><span>🌡 ${numberFormat.format(item.temp)}°</span><p>${escapeHtml(item.recommendation)}</p></article>
  `).join('');
}

async function loadData() {
  const button = document.getElementById('refresh-button');
  button.disabled = true;
  button.textContent = 'جارٍ التحديث…';
  setStatus('جارٍ تحميل بيانات العرض…');
  try {
    const [summary, regions, fields, alerts, forecast] = await Promise.all(Object.entries(routes).map(async ([key, url]) => [key, await getJson(url)]));
    const data = Object.fromEntries([summary, regions, fields, alerts, forecast]);
    renderSummary(data.overview);
    renderRegions(data.regions);
    renderFields(data.fields);
    renderAlerts(data.alerts);
    renderForecast(data.forecast);
    document.getElementById('last-updated').textContent = `آخر تحديث: ${new Intl.DateTimeFormat('ar', { timeStyle: 'short' }).format(new Date())}`;
    setStatus('تم تحديث بيانات العرض بنجاح.', 'success');
  } catch (error) {
    console.error('Dashboard load failed:', error);
    setStatus(navigator.onLine ? 'تعذر تحميل البيانات. حاول مرة أخرى.' : 'أنت غير متصل. قد تكون البيانات المحفوظة متاحة بعد أول تحميل.', 'error');
  } finally {
    button.disabled = false;
    button.textContent = 'تحديث البيانات';
  }
}

document.getElementById('refresh-button').addEventListener('click', loadData);
document.getElementById('field-search').addEventListener('input', filterFields);
window.addEventListener('online', () => { document.getElementById('connection-label').textContent = 'متصل'; });
window.addEventListener('offline', () => { document.getElementById('connection-label').textContent = 'غير متصل · وضع غير متصل'; });
document.getElementById('connection-label').textContent = navigator.onLine ? 'متصل' : 'غير متصل · وضع غير متصل';

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('/service-worker.js').catch((error) => console.warn('Offline support unavailable:', error)));
}

loadData();
