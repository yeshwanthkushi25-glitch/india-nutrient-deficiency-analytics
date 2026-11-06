/**
 * app.js - Interactive Data Analytics Engine
 * Theme: "Nutrient Deficiency & The Hidden Hunger Paradox in India"
 * Grounded on ICMR-NIN 2024 & NFHS-5 Public Health Standards.
 */

// Global State Store
const AppState = {
  data: null,
  geoJson: null,
  activeZone: 'All',
  activeState: 'All',
  activeArea: 'All',
  activeDiet: 'All',
  activeMapMetric: 'protein_deficit_pct',
  selectedStateDetail: 'Maharashtra',
  map: null,
  geoJsonLayer: null,
  charts: {},
  sortKey: 'name',
  sortAsc: true,
  searchTerm: ''
};

// Metric metadata configuration
const METRIC_CONFIG = {
  protein_deficit_pct: {
    label: 'Protein Deficit (%)',
    min: 45, mid: 65, max: 85,
    unit: '%',
    palette: ['#10b981', '#f59e0b', '#ef4444', '#881337'],
    higherIsBad: true,
    desc: 'Percentage of population failing to meet ICMR-NIN 2024 protein RDA (0.83 g/kg).'
  },
  anemia_pct: {
    label: 'Anemia Prevalence (%)',
    min: 25, mid: 50, max: 75,
    unit: '%',
    palette: ['#10b981', '#f59e0b', '#ef4444', '#881337'],
    higherIsBad: true,
    desc: 'Prevalence of iron-deficiency anemia from NFHS-5 survey.'
  },
  b12_pct: {
    label: 'Vitamin B12 Deficiency (%)',
    min: 35, mid: 55, max: 80,
    unit: '%',
    palette: ['#10b981', '#f59e0b', '#ef4444', '#881337'],
    higherIsBad: true,
    desc: 'Deficiency of cobalamin impacting nerve myelination and RBC formation.'
  },
  vitd_pct: {
    label: 'Vitamin D Deficiency (%)',
    min: 60, mid: 75, max: 90,
    unit: '%',
    palette: ['#10b981', '#f59e0b', '#ef4444', '#881337'],
    higherIsBad: true,
    desc: 'Serum 25(OH)D < 20 ng/mL across urban and indoor populations.'
  },
  calcium_pct: {
    label: 'Calcium Inadequacy (%)',
    min: 40, mid: 65, max: 85,
    unit: '%',
    palette: ['#10b981', '#f59e0b', '#ef4444', '#881337'],
    higherIsBad: true,
    desc: 'Dietary calcium intake below 1000 mg/day RDA.'
  },
  hidden_hunger_index: {
    label: 'Hidden Hunger Severity (0-100)',
    min: 35, mid: 60, max: 85,
    unit: '',
    palette: ['#10b981', '#f59e0b', '#ef4444', '#881337'],
    higherIsBad: true,
    desc: 'Composite score: High caloric intake paired with micronutrient starvation.'
  },
  awareness_score: {
    label: 'Nutritional Literacy Score (0-100)',
    min: 25, mid: 50, max: 75,
    unit: '',
    palette: ['#881337', '#ef4444', '#f59e0b', '#10b981'], // Inverted for positive literacy
    higherIsBad: false,
    desc: 'Nutritional awareness, reading food labels, and understanding balanced plates.'
  }
};

const ZONE_COLORS = {
  'North': '#3b82f6',
  'Central': '#8b5cf6',
  'East': '#ec4899',
  'West': '#f97316',
  'South': '#10b981',
  'North-East': '#06b6d4',
  'Other': '#64748b'
};

// -------------------------------------------------------------
// 1. Data Bootstrap
// -------------------------------------------------------------
async function initApp() {
  try {
    // 1. Load pre-bundled or fetched data
    if (window.INDIA_NUTRITION_DATA) {
      AppState.data = window.INDIA_NUTRITION_DATA;
    } else {
      const res = await fetch('data/india_nutrition_data.json');
      AppState.data = await res.json();
    }

    // 2. Load GeoJSON
    if (window.INDIA_GEOJSON) {
      AppState.geoJson = window.INDIA_GEOJSON;
    } else {
      const resGeo = await fetch('data/india_states.geojson');
      AppState.geoJson = await resGeo.json();
    }

    console.log('Dataset loaded successfully:', AppState.data.metadata);

    // 3. Initialize components
    populateStateDropdown();
    initMap();
    initCharts();
    renderMatrixTable();
    updateExecutiveKPIs();
    renderStateScorecard(AppState.selectedStateDetail);
    initCalculator();
    setupEventListeners();

  } catch (err) {
    console.error('Initialization error:', err);
    alert('Failed to load application dataset. Please check console.');
  }
}

// -------------------------------------------------------------
// 2. Filter Bar & KPI Deck Logic
// -------------------------------------------------------------
function populateStateDropdown() {
  const select = document.getElementById('state-filter');
  select.innerHTML = '<option value="All">All 36 States & UTs</option>';
  
  const states = Object.keys(AppState.data.states).sort();
  states.forEach(st => {
    const opt = document.createElement('option');
    opt.value = st;
    opt.textContent = st;
    select.appendChild(opt);
  });
}

function getFilteredStateList() {
  const statesObj = AppState.data.states;
  return Object.values(statesObj).filter(st => {
    if (AppState.activeZone !== 'All' && st.zone !== AppState.activeZone) return false;
    if (AppState.activeState !== 'All' && st.name !== AppState.activeState) return false;
    return true;
  });
}

function updateExecutiveKPIs() {
  const filtered = getFilteredStateList();
  if (filtered.length === 0) return;

  const count = filtered.length;
  const avgProteinDef = filtered.reduce((acc, s) => acc + s.protein_deficit_pct, 0) / count;
  const avgHH = filtered.reduce((acc, s) => acc + s.hidden_hunger_index, 0) / count;
  const avgCalSuff = filtered.reduce((acc, s) => acc + s.calorie_sufficiency_pct, 0) / count;
  const avgAnemia = filtered.reduce((acc, s) => acc + s.anemia_pct, 0) / count;
  const avgVitD = filtered.reduce((acc, s) => acc + s.vitd_pct, 0) / count;
  const avgB12 = filtered.reduce((acc, s) => acc + s.b12_pct, 0) / count;
  const avgLit = filtered.reduce((acc, s) => acc + s.awareness_score, 0) / count;

  document.getElementById('kpi-protein-def').textContent = `${avgProteinDef.toFixed(1)}%`;
  document.getElementById('kpi-hidden-hunger').textContent = avgHH.toFixed(1);
  document.getElementById('kpi-calorie-suff').textContent = `${avgCalSuff.toFixed(1)}%`;
  document.getElementById('kpi-anemia').textContent = `${avgAnemia.toFixed(1)}%`;
  document.getElementById('kpi-vitd-b12').textContent = `${avgVitD.toFixed(1)}%`;
  document.getElementById('kpi-literacy').textContent = avgLit.toFixed(1);
}

// -------------------------------------------------------------
// 3. Leaflet India Map & Choropleth Layer
// -------------------------------------------------------------
function getColorForValue(val, config) {
  if (val === undefined || val === null || isNaN(val)) return '#cbd5e1';
  const { min, mid, max, palette, higherIsBad } = config;
  
  if (higherIsBad) {
    if (val < min) return palette[0];
    if (val < mid) return palette[1];
    if (val < max) return palette[2];
    return palette[3];
  } else {
    // For literacy: lower is worse
    if (val < min) return palette[0];
    if (val < mid) return palette[1];
    if (val < max) return palette[2];
    return palette[3];
  }
}

function canonicalizeGeoName(name) {
  if (!name) return '';
  const clean = name.trim();
  if (clean === 'Dadra and Nagar Haveli' || clean === 'Daman and Diu') {
    return 'Dadra and Nagar Haveli and Daman and Diu';
  }
  return clean;
}

function initMap() {
  if (AppState.map) AppState.map.remove();

  AppState.map = L.map('india-map', {
    center: [22.8, 80.0],
    zoom: 4.4,
    minZoom: 4,
    maxZoom: 7,
    zoomSnap: 0.2,
    zoomControl: true,
    attributionControl: false
  });

  // Clean tile layer
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(AppState.map);

  renderGeoJsonLayer();
  updateMapLegend();
}

function renderGeoJsonLayer() {
  if (!AppState.geoJson) return;
  if (AppState.geoJsonLayer) AppState.map.removeLayer(AppState.geoJsonLayer);

  const cfg = METRIC_CONFIG[AppState.activeMapMetric];

  AppState.geoJsonLayer = L.geoJSON(AppState.geoJson, {
    style: function (feature) {
      const rawName = feature.properties.st_nm;
      const stateName = canonicalizeGeoName(rawName);
      const stData = AppState.data.states[stateName];
      const val = stData ? stData[AppState.activeMapMetric] : null;

      const isSelected = (stateName === AppState.selectedStateDetail);

      return {
        fillColor: getColorForValue(val, cfg),
        weight: isSelected ? 3 : 1.2,
        opacity: 1,
        color: isSelected ? '#0f172a' : '#ffffff',
        dashArray: isSelected ? '' : '',
        fillOpacity: isSelected ? 0.95 : 0.78
      };
    },
    onEachFeature: function (feature, layer) {
      const rawName = feature.properties.st_nm;
      const stateName = canonicalizeGeoName(rawName);
      const stData = AppState.data.states[stateName];

      const val = stData ? `${stData[AppState.activeMapMetric]}${cfg.unit}` : 'N/A';
      const pop = stData ? `${stData.population_cr} Cr` : '-';
      const zone = stData ? stData.zone : '-';

      const tooltipContent = `
        <div style="font-family: var(--font-main); font-size: 0.8rem; line-height: 1.4;">
          <strong style="color: #0f172a; font-size: 0.88rem;">${stateName}</strong><br/>
          <span style="color: #64748b;">Zone: ${zone} | Pop: ${pop}</span><br/>
          <span style="color: #2563eb; font-weight: 700;">${cfg.label}: ${val}</span>
        </div>
      `;
      layer.bindTooltip(tooltipContent, { sticky: true, className: 'custom-map-tooltip' });

      layer.on({
        mouseover: function (e) {
          const l = e.target;
          l.setStyle({ weight: 2.5, color: '#1e293b', fillOpacity: 0.92 });
          l.bringToFront();
        },
        mouseout: function (e) {
          AppState.geoJsonLayer.resetStyle(e.target);
        },
        click: function () {
          if (AppState.data.states[stateName]) {
            AppState.selectedStateDetail = stateName;
            renderStateScorecard(stateName);
            AppState.geoJsonLayer.eachLayer(l => AppState.geoJsonLayer.resetStyle(l));
          }
        }
      });
    }
  }).addTo(AppState.map);
}

function updateMapLegend() {
  const cfg = METRIC_CONFIG[AppState.activeMapMetric];
  document.getElementById('legend-metric-label').textContent = cfg.label;
  document.getElementById('legend-min').textContent = `${cfg.min}${cfg.unit}`;
  document.getElementById('legend-mid').textContent = `${cfg.mid}${cfg.unit}`;
  document.getElementById('legend-max').textContent = `${cfg.max}+${cfg.unit}`;

  // Update gradient bar color
  const gradEl = document.getElementById('legend-gradient');
  gradEl.style.background = `linear-gradient(to right, ${cfg.palette.join(', ')})`;
}

// -------------------------------------------------------------
// 4. Dynamic State Scorecard Side Panel
// -------------------------------------------------------------
function renderStateScorecard(stateName) {
  const st = AppState.data.states[stateName];
  if (!st) return;

  document.getElementById('panel-state-name').textContent = st.name;
  document.getElementById('panel-zone-badge').textContent = `${st.zone} Zone`;
  document.getElementById('panel-state-meta').textContent = `Capital: ${st.capital} | Population: ${st.population_cr} Cr`;

  // Status Badge
  const statusBadge = document.getElementById('panel-status-badge');
  if (st.hidden_hunger_index >= 70) {
    statusBadge.textContent = 'Critical Hidden Hunger';
    statusBadge.className = 'state-status-badge badge-danger';
  } else if (st.hidden_hunger_index >= 55) {
    statusBadge.textContent = 'Moderate Deficit';
    statusBadge.className = 'state-status-badge badge-warning';
  } else {
    statusBadge.textContent = 'Relatively Balanced';
    statusBadge.className = 'state-status-badge badge-success';
  }

  // Stats
  document.getElementById('panel-cal-stat').textContent = `${st.calorie_intake} kcal (${st.calorie_sufficiency_pct}% RDA)`;
  document.getElementById('panel-carb-stat').textContent = `${st.carb_share_pct}% of energy`;
  document.getElementById('panel-protein-stat').textContent = `${st.protein_deficit_pct}% (${st.protein_intake_g}g vs ${st.protein_rda_g}g)`;
  document.getElementById('panel-anemia-stat').textContent = `${st.anemia_pct}%`;
  document.getElementById('panel-vitd-stat').textContent = `${st.vitd_pct}%`;
  document.getElementById('panel-b12-stat').textContent = `${st.b12_pct}%`;
  document.getElementById('panel-calc-stat').textContent = `${st.calcium_pct}%`;
  document.getElementById('panel-lit-stat').textContent = `${st.awareness_score} / 100`;

  // Urban vs Rural
  document.getElementById('panel-urban-anemia').textContent = `${st.urban_anemia}%`;
  document.getElementById('panel-rural-anemia').textContent = `${st.rural_anemia}%`;
  document.getElementById('panel-double-burden').textContent = `${st.double_burden_pct}%`;

  // Tailored recommendation
  let advice = '';
  if (st.zone === 'North' || st.zone === 'West') {
    advice = `High dairy and wheat consumption exists, but Vitamin B12 deficiency (${st.b12_pct}%) remains severe due to widespread vegetarianism without bioavailable supplementation. Add roasted chana, sattu, and sprouted moong.`;
  } else if (st.zone === 'East' || st.zone === 'Central') {
    advice = `Heavy rice dependency (${st.carb_share_pct}% carb share) with high microcytic anemia (${st.anemia_pct}%). Incorporate local drumstick leaves (moringa), lemon with meals to boost iron, and affordable egg/soya protein.`;
  } else if (st.zone === 'South') {
    advice = `Polished white rice staples create high caloric sufficiency (${st.calorie_sufficiency_pct}%) but an acute protein gap (${st.protein_deficit_pct}%). Increase ragi (finger millet), curd/buttermilk, and sesame (til) for calcium.`;
  } else {
    advice = `Dietary literacy is relatively higher (${st.awareness_score}/100), but Vitamin D (${st.vitd_pct}%) remains suppressed due to indoor lifestyle. Target 20 minutes of midday sunlight and fortified foods.`;
  }
  document.getElementById('panel-recommendation').textContent = advice;
}

// -------------------------------------------------------------
// 5. Interactive Charts (Chart.js)
// -------------------------------------------------------------
function initCharts() {
  renderParadoxChart();
  renderScatterChart();
  renderDemographicChart();
}

function renderParadoxChart() {
  const ctx = document.getElementById('paradoxChart').getContext('2d');
  
  // National benchmark paradox: Calories & Carbs are surplus, whereas Protein and Micronutrients are severely deficient
  const labels = ['Calories', 'Carbohydrates', 'Protein', 'Iron (Anemia Free)', 'Vitamin B12', 'Vitamin D', 'Calcium'];
  // Values represent % Fulfillment of ICMR-NIN RDA
  const intakeFulfillment = [108.0, 142.0, 68.0, 43.0, 38.0, 24.0, 42.0];
  const rdaTarget = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0];

  const colors = intakeFulfillment.map(v => v >= 100 ? '#f59e0b' : '#ef4444');

  if (AppState.charts.paradox) AppState.charts.paradox.destroy();

  AppState.charts.paradox = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Actual Intake (% of Body Requirement RDA)',
          data: intakeFulfillment,
          backgroundColor: colors,
          borderRadius: 6,
          barPercentage: 0.6
        },
        {
          label: 'ICMR-NIN RDA Requirement (100% Benchmark)',
          data: rdaTarget,
          type: 'line',
          borderColor: '#0f172a',
          borderWidth: 2,
          borderDash: [5, 5],
          pointRadius: 0,
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { font: { family: 'Plus Jakarta Sans', size: 11 } } },
        tooltip: {
          callbacks: {
            label: function (ctx) {
              return `${ctx.dataset.label}: ${ctx.raw}%`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 160,
          title: { display: true, text: '% of Daily Physiological Requirement', font: { size: 10, weight: 'bold' } },
          grid: { color: '#f1f5f9' }
        },
        x: {
          grid: { display: false },
          ticks: { font: { size: 11, weight: '600' } }
        }
      }
    }
  });
}

function renderScatterChart() {
  const ctx = document.getElementById('scatterChart').getContext('2d');
  const states = Object.values(AppState.data.states);

  const scatterData = states.map(s => ({
    x: s.awareness_score,
    y: s.hidden_hunger_index,
    r: Math.max(5, Math.sqrt(s.population_cr) * 3.5),
    state: s.name,
    zone: s.zone,
    pop: s.population_cr
  }));

  if (AppState.charts.scatter) AppState.charts.scatter.destroy();

  AppState.charts.scatter = new Chart(ctx, {
    type: 'bubble',
    data: {
      datasets: [{
        label: 'States / UTs',
        data: scatterData,
        backgroundColor: function (context) {
          const raw = context.raw;
          if (!raw) return '#3b82f6';
          return ZONE_COLORS[raw.zone] || '#3b82f6';
        },
        borderColor: 'rgba(255, 255, 255, 0.8)',
        borderWidth: 1.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function (ctx) {
              const d = ctx.raw;
              return `${d.state} (${d.zone}): Awareness ${d.x}/100, Hidden Hunger ${d.y}, Pop ${d.pop} Cr`;
            }
          }
        }
      },
      scales: {
        x: {
          title: { display: true, text: 'Nutritional Literacy Score (0–100)', font: { size: 11, weight: 'bold' } },
          min: 25,
          max: 75,
          grid: { color: '#f1f5f9' }
        },
        y: {
          title: { display: true, text: 'Hidden Hunger Severity Index (0–100)', font: { size: 11, weight: 'bold' } },
          min: 45,
          max: 85,
          grid: { color: '#f1f5f9' }
        }
      }
    }
  });
}

function renderDemographicChart() {
  const ctx = document.getElementById('demographicChart').getContext('2d');
  const demoList = AppState.data.demographics;

  const labels = demoList.map(d => d.label);
  const proteinDef = demoList.map(d => d.protein_deficit_pct);
  const anemia = demoList.map(d => d.anemia_pct);
  const vitd = demoList.map(d => d.vitd_pct);
  const b12 = demoList.map(d => d.b12_pct);

  if (AppState.charts.demographic) AppState.charts.demographic.destroy();

  AppState.charts.demographic = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Protein Deficit (%)',
          data: proteinDef,
          backgroundColor: '#3b82f6',
          borderRadius: 4
        },
        {
          label: 'Anemia Prevalence (%)',
          data: anemia,
          backgroundColor: '#ef4444',
          borderRadius: 4
        },
        {
          label: 'Vitamin D Deficiency (%)',
          data: vitd,
          backgroundColor: '#f59e0b',
          borderRadius: 4
        },
        {
          label: 'Vitamin B12 Deficiency (%)',
          data: b12,
          backgroundColor: '#8b5cf6',
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { font: { family: 'Plus Jakarta Sans', size: 11 } } },
        tooltip: {
          callbacks: {
            label: function (ctx) {
              return `${ctx.dataset.label}: ${ctx.raw}%`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 95,
          title: { display: true, text: 'Prevalence Rate (%)', font: { size: 10, weight: 'bold' } },
          grid: { color: '#f1f5f9' }
        },
        x: {
          grid: { display: false },
          ticks: { font: { size: 10, weight: '600' } }
        }
      }
    }
  });
}

// -------------------------------------------------------------
// 6. Multi-Nutrient Heatmap Matrix Table
// -------------------------------------------------------------
function renderMatrixTable() {
  const tbody = document.getElementById('matrix-table-body');
  tbody.innerHTML = '';

  let list = Object.values(AppState.data.states);

  // Search filter
  if (AppState.searchTerm) {
    const q = AppState.searchTerm.toLowerCase();
    list = list.filter(s => s.name.toLowerCase().includes(q) || s.zone.toLowerCase().includes(q));
  }

  // Zone / State filter
  if (AppState.activeZone !== 'All') {
    list = list.filter(s => s.zone === AppState.activeZone);
  }
  if (AppState.activeState !== 'All') {
    list = list.filter(s => s.name === AppState.activeState);
  }

  // Sorting
  list.sort((a, b) => {
    let va = a[AppState.sortKey];
    let vb = b[AppState.sortKey];
    if (typeof va === 'string') {
      return AppState.sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
    }
    return AppState.sortAsc ? va - vb : vb - va;
  });

  list.forEach(st => {
    const tr = document.createElement('tr');
    tr.dataset.state = st.name;

    const chipClass = (val, low, high) => {
      if (val < low) return 'cell-chip chip-low';
      if (val < high) return 'cell-chip chip-med';
      return 'cell-chip chip-high';
    };

    tr.innerHTML = `
      <td><strong>${st.name}</strong></td>
      <td><span style="color: ${ZONE_COLORS[st.zone] || '#475569'}; font-weight: 700;">${st.zone}</span></td>
      <td class="table-num">${st.population_cr}</td>
      <td class="table-num">${st.calorie_sufficiency_pct}%</td>
      <td class="table-num">${st.carb_share_pct}%</td>
      <td><span class="${chipClass(st.protein_deficit_pct, 60, 72)}">${st.protein_deficit_pct}%</span></td>
      <td><span class="${chipClass(st.anemia_pct, 45, 60)}">${st.anemia_pct}%</span></td>
      <td><span class="${chipClass(st.vitd_pct, 70, 80)}">${st.vitd_pct}%</span></td>
      <td><span class="${chipClass(st.b12_pct, 50, 65)}">${st.b12_pct}%</span></td>
      <td><span class="cell-chip ${st.awareness_score < 40 ? 'chip-high' : (st.awareness_score < 55 ? 'chip-med' : 'chip-low')}">${st.awareness_score}</span></td>
      <td><span class="${chipClass(st.hidden_hunger_index, 55, 70)}">${st.hidden_hunger_index}</span></td>
    `;

    tr.addEventListener('click', () => {
      AppState.selectedStateDetail = st.name;
      renderStateScorecard(st.name);
      if (AppState.geoJsonLayer) {
        AppState.geoJsonLayer.eachLayer(l => AppState.geoJsonLayer.resetStyle(l));
      }
      document.getElementById('choropleth-section').scrollIntoView({ behavior: 'smooth' });
    });

    tbody.appendChild(tr);
  });
}

// -------------------------------------------------------------
// 7. Personal Body-Needs Calculator ("Check Your Plate")
// -------------------------------------------------------------
function initCalculator() {
  const inputs = [
    'calc-age', 'calc-gender', 'calc-activity', 'calc-diet',
    'item-roti', 'item-rice', 'item-dal', 'item-dairy',
    'item-paneer', 'item-egg-meat', 'item-greens', 'item-snacks',
    'item-tea-iron'
  ];

  inputs.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', runCalculator);
      el.addEventListener('change', runCalculator);
    }
  });

  // Step buttons (+ / -)
  document.querySelectorAll('.btn-step').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.target;
      const dir = parseInt(btn.dataset.dir);
      const input = document.getElementById(targetId);
      if (input) {
        let cur = parseFloat(input.value) || 0;
        let step = parseFloat(input.step) || 1;
        cur = Math.max(0, cur + (dir * step));
        input.value = cur;
        runCalculator();
      }
    });
  });

  runCalculator();
}

function runCalculator() {
  const age = parseInt(document.getElementById('calc-age').value) || 25;
  const gender = document.getElementById('calc-gender').value;
  const activity = document.getElementById('calc-activity').value;
  const diet = document.getElementById('calc-diet').value;

  const roti = parseFloat(document.getElementById('item-roti').value) || 0;
  const rice = parseFloat(document.getElementById('item-rice').value) || 0;
  const dal = parseFloat(document.getElementById('item-dal').value) || 0;
  const dairy = parseFloat(document.getElementById('item-dairy').value) || 0;
  const paneer = parseFloat(document.getElementById('item-paneer').value) || 0;
  const eggMeat = parseFloat(document.getElementById('item-egg-meat').value) || 0;
  const greens = parseFloat(document.getElementById('item-greens').value) || 0;
  const snacks = parseFloat(document.getElementById('item-snacks').value) || 0;
  const teaInhibitor = document.getElementById('item-tea-iron').checked;

  // 1. Calculate Personal RDA Requirements (ICMR-NIN 2024 Standards)
  let calReq = (gender === 'Male') ? 2110 : 1660;
  if (activity === 'Moderate') calReq += 300;
  if (activity === 'Heavy') calReq += 700;

  let protReq = (gender === 'Male') ? 54.0 : 46.0;
  let ironReq = (gender === 'Female' && age <= 50) ? 29.0 : 19.0;
  let calcReq = (age >= 50 && gender === 'Female') ? 1200 : 1000;

  // 2. Meal Nutritional Values
  // Roti: ~105 kcal, 3.2g protein, 1.2mg iron, 12mg calcium
  // Rice bowl: ~170 kcal, 3.0g protein, 0.4mg iron, 10mg calcium
  // Dal bowl: ~150 kcal, 7.5g protein, 2.5mg iron, 40mg calcium
  // Dairy cup: ~120 kcal, 6.0g protein, 0.1mg iron, 240mg calcium
  // Paneer/soya: ~180 kcal, 14.0g protein, 1.5mg iron, 180mg calcium
  // Egg/meat: ~160 kcal, 14.0g protein, 2.2mg iron (heme), 30mg calcium
  // Greens cup: ~35 kcal, 2.2g protein, 2.8mg iron, 80mg calcium
  // Snacks/namkeen: ~190 kcal, 2.0g protein, 0.5mg iron, 15mg calcium

  const totalCal = Math.round(
    roti * 105 + rice * 170 + dal * 150 + dairy * 120 +
    paneer * 180 + eggMeat * 160 + greens * 35 + snacks * 190
  );

  const totalProt = (
    roti * 3.2 + rice * 3.0 + dal * 7.5 + dairy * 6.0 +
    paneer * 14.0 + eggMeat * 14.0 + greens * 2.2 + snacks * 2.0
  );

  let totalIron = (
    roti * 1.2 + rice * 0.4 + dal * 2.5 + dairy * 0.1 +
    paneer * 1.5 + eggMeat * 2.2 + greens * 2.8 + snacks * 0.5
  );

  // If tea/chai consumed with meal, non-heme iron absorption drops ~55%
  if (teaInhibitor) {
    totalIron = totalIron * 0.45;
  }

  const totalCalcium = Math.round(
    roti * 12 + rice * 10 + dal * 40 + dairy * 240 +
    paneer * 180 + eggMeat * 30 + greens * 80 + snacks * 15
  );

  // Vitamin B12 Status
  let b12Score = (dairy * 20) + (eggMeat * 45) + (paneer * 15);
  if (diet === 'Vegetarian' && dairy < 2 && paneer === 0) b12Score = 20;

  // 3. Render Outputs
  const calPct = Math.round((totalCal / calReq) * 100);
  const protPct = Math.round((totalProt / protReq) * 100);
  const ironPct = Math.round((totalIron / ironReq) * 100);
  const calcPct = Math.round((totalCalcium / calcReq) * 100);

  document.getElementById('calc-cal-label').textContent = `${totalCal.toLocaleString()} / ${calReq.toLocaleString()} kcal (${calPct}%)`;
  document.getElementById('calc-cal-fill').style.width = `${Math.min(calPct, 100)}%`;

  document.getElementById('calc-protein-label').textContent = `${totalProt.toFixed(1)} / ${protReq.toFixed(1)} g (${protPct}% RDA)`;
  document.getElementById('calc-protein-fill').style.width = `${Math.min(protPct, 100)}%`;

  document.getElementById('calc-iron-label').textContent = `${totalIron.toFixed(1)} / ${ironReq.toFixed(1)} mg (${ironPct}% RDA)`;
  document.getElementById('calc-iron-fill').style.width = `${Math.min(ironPct, 100)}%`;

  document.getElementById('calc-calc-label').textContent = `${totalCalcium} / ${calcReq} mg (${calcPct}% RDA)`;
  document.getElementById('calc-calc-fill').style.width = `${Math.min(calcPct, 100)}%`;

  const b12Label = document.getElementById('calc-b12-label');
  const b12Fill = document.getElementById('calc-b12-fill');
  if (b12Score >= 70) {
    b12Label.textContent = 'Likely Adequate';
    b12Fill.className = 'progress-fill prog-green';
    b12Fill.style.width = '85%';
  } else if (b12Score >= 40) {
    b12Label.textContent = 'Borderline / Moderate Risk';
    b12Fill.className = 'progress-fill prog-yellow';
    b12Fill.style.width = '45%';
  } else {
    b12Label.textContent = 'High Deficiency Risk (Vegetarian / Low Dairy)';
    b12Fill.className = 'progress-fill prog-red';
    b12Fill.style.width = '25%';
  }

  // Diagnosis Badge
  const verdictTitle = document.getElementById('calc-verdict-title');
  const verdictDesc = document.getElementById('calc-verdict-desc');
  const verdictBadge = document.getElementById('calc-verdict-badge');

  if (calPct >= 95 && protPct < 70) {
    verdictBadge.className = 'diagnosis-badge-banner';
    verdictTitle.textContent = `🚨 The Hidden Hunger Paradox Confirmed!`;
    verdictDesc.textContent = `You are consuming ${calPct}% of your daily energy needs (calories), but only ${protPct}% of your required protein and ${ironPct}% bioavailable iron. Your body is energy-full yet nutrient-starved.`;
  } else if (protPct >= 85 && ironPct >= 80) {
    verdictBadge.className = 'diagnosis-badge-banner';
    verdictBadge.style.backgroundColor = 'var(--emerald-soft)';
    verdictBadge.style.borderColor = '#a7f3d0';
    verdictTitle.textContent = `✅ Well-Balanced Nutrient Plate`;
    verdictTitle.style.color = '#065f46';
    verdictDesc.textContent = `Excellent job! You are meeting both your macronutrient (protein) and micronutrient targets without excessive empty caloric density.`;
    verdictDesc.style.color = '#047857';
  } else {
    verdictBadge.className = 'diagnosis-badge-banner';
    verdictTitle.textContent = `⚠️ Moderate Nutritional Gap Detected`;
    verdictDesc.textContent = `Your diet fulfills ${protPct}% of your protein and ${calcPct}% of your calcium target. See below for simple Indian kitchen swaps.`;
  }
}

// -------------------------------------------------------------
// 8. Event Listeners & Filter Coordination
// -------------------------------------------------------------
function setupEventListeners() {
  // Zone Filter
  document.getElementById('zone-filter').addEventListener('change', (e) => {
    AppState.activeZone = e.target.value;
    updateExecutiveKPIs();
    renderMatrixTable();
    if (AppState.charts.scatter) renderScatterChart();
  });

  // State Filter
  document.getElementById('state-filter').addEventListener('change', (e) => {
    AppState.activeState = e.target.value;
    if (e.target.value !== 'All') {
      AppState.selectedStateDetail = e.target.value;
      renderStateScorecard(e.target.value);
    }
    updateExecutiveKPIs();
    renderMatrixTable();
  });

  // Reset Filters
  document.getElementById('reset-filters-btn').addEventListener('click', () => {
    AppState.activeZone = 'All';
    AppState.activeState = 'All';
    AppState.activeArea = 'All';
    AppState.activeDiet = 'All';
    AppState.searchTerm = '';
    document.getElementById('zone-filter').value = 'All';
    document.getElementById('state-filter').value = 'All';
    document.getElementById('area-filter').value = 'All';
    document.getElementById('diet-filter').value = 'All';
    document.getElementById('table-search-input').value = '';
    updateExecutiveKPIs();
    renderMatrixTable();
    renderGeoJsonLayer();
  });

  // Map Metric Layer Toggles
  document.querySelectorAll('#map-metric-buttons button').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#map-metric-buttons button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.activeMapMetric = btn.dataset.metric;
      renderGeoJsonLayer();
      updateMapLegend();
    });
  });

  // Matrix Table Search
  document.getElementById('table-search-input').addEventListener('input', (e) => {
    AppState.searchTerm = e.target.value;
    renderMatrixTable();
  });

  // Matrix Table Column Header Sorting
  document.querySelectorAll('#states-matrix-table th').forEach(th => {
    th.addEventListener('click', () => {
      const sortKey = th.dataset.sort;
      if (AppState.sortKey === sortKey) {
        AppState.sortAsc = !AppState.sortAsc;
      } else {
        AppState.sortKey = sortKey;
        AppState.sortAsc = true;
      }
      renderMatrixTable();
    });
  });
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);
