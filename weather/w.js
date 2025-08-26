// Helper function
const $ = (sel) => document.querySelector(sel);

const q = $('#q');
const btnFind = $('#find');
const btnGeo = $('#geo');

const els = {
  temp: $('#temp'),
  summary: $('#summary'),
  meta: $('#meta'),
  place: $('#place'),
  wind: $('#wind'),
  hum: $('#hum')
};

// ✅ Your OpenWeatherMap API key
const API_KEY = "050d5f793c5a2ddfb384631ea79bafcf";

// Fetch weather by city
async function fetchWeatherCity(city) {
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=metric`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("City not found");
  return res.json();
}

// Fetch weather by location
async function fetchWeatherCoords(lat, lon) {
  const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Location fetch failed");
  return res.json();
}

function showLoading() {
  els.summary.textContent = 'Loading…';
}
function showError(msg) {
  els.summary.textContent = msg;
  els.temp.textContent = '--°';
  els.meta.textContent = '—';
  els.place.textContent = '—';
  els.wind.textContent = 'Wind: —';
  els.hum.textContent = 'Humidity: —';
}

function renderWeather(data) {
  els.temp.textContent = Math.round(data.main.temp) + "°C";
  els.summary.textContent = `${data.weather[0].description} 🌤️`;
  els.meta.textContent = `Updated: ${new Date().toLocaleString()}`;
  els.place.textContent = `${data.name}, ${data.sys.country}`;
  els.wind.textContent = `Wind: ${data.wind.speed} m/s`;
  els.hum.textContent = `Humidity: ${data.main.humidity}%`;
}

async function renderByCity(name) {
  if (!name) return;
  try {
    showLoading();
    const data = await fetchWeatherCity(name);
    renderWeather(data);
  } catch {
    showError("City not found");
  }
}

async function renderByLocation(lat, lon) {
  try {
    showLoading();
    const data = await fetchWeatherCoords(lat, lon);
    renderWeather(data);
  } catch {
    showError("Could not load weather");
  }
}

// Events
btnFind.addEventListener('click', () => renderByCity(q.value.trim()));
q.addEventListener('keydown', (e) => { if (e.key === 'Enter') renderByCity(q.value.trim()) });

btnGeo.addEventListener('click', () => {
  if (!navigator.geolocation) return showError("Geolocation not supported");
  showLoading();
  navigator.geolocation.getCurrentPosition(
    (pos) => renderByLocation(pos.coords.latitude, pos.coords.longitude),
    () => showError("Location permission denied")
  );
});

// On load
window.addEventListener('load', () => { q.value = ''; });
