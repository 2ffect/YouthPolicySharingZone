<template>
  <div class="main-container">
    <h2 class="highlight">청년센터 찾기</h2>
    <p class="subtitle">청년센터의 위치를 검색해보세요.</p>

    <form class="search-form" @submit.prevent="searchCenter">
      <input type="text" v-model="keyword" placeholder="검색어를 입력하세요" />
      <button type="submit">검색</button>
    </form>

    <div class="map-section">
      <!-- 검색 결과 -->
      <div class="search-results box">
        <h3 class="box-title">📍 검색 결과</h3>
        <ul>
          <li
            v-for="(place, index) in searchResults"
            :key="index"
            @click="focusPlace(index)"
          >
            <strong>{{ place.place_name }}</strong>
            <br />
            {{ place.address_name }}
            <span v-if="place.distance"> ({{ (place.distance / 1000).toFixed(2) }} km)</span>
          </li>
        </ul>
      </div>

      <!-- 지도 -->
      <div class="map-box" id="map"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useLocationStore } from '@/stores/location'

const MAP_API_KEY = import.meta.env.VITE_MAP_API_KEY
const keyword = ref('')
const searchResults = ref([])
let map = null
let ps = null
let markers = []
let infowindow = null
const maxDistance = 5000

const locationStore = useLocationStore()

const initMap = (lat, lng) => {
  const container = document.getElementById('map')
  const options = {
    center: new window.kakao.maps.LatLng(lat, lng),
    level: 3,
  }
  map = new window.kakao.maps.Map(container, options)
  ps = new window.kakao.maps.services.Places()
}

const getDistance = (lat1, lng1, lat2, lng2) => {
  const R = 6371e3
  const toRad = deg => deg * Math.PI / 180
  const phi1 = toRad(lat1), phi2 = toRad(lat2)
  const deltaPhi = toRad(lat2 - lat1)
  const deltaLambda = toRad(lng2 - lng1)
  const a = Math.sin(deltaPhi / 2) ** 2 + Math.cos(phi1) * Math.cos(phi2) * Math.sin(deltaLambda / 2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

const searchCenter = () => {
  if (!keyword.value || !ps || !map) return
  markers.forEach(m => m.marker.setMap(null))
  markers = []
  if (infowindow) infowindow.close()
  searchResults.value = []

  ps.keywordSearch(keyword.value, (data, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      const bounds = new window.kakao.maps.LatLngBounds()
      const enrichedData = data.map((place) => {
        const lat = parseFloat(place.y)
        const lng = parseFloat(place.x)
        const distance = getDistance(locationStore.latitude, locationStore.longitude, lat, lng)
        return { ...place, distance, lat, lng }
      })

      enrichedData.sort((a, b) => a.distance - b.distance)

      enrichedData.forEach((place) => {
        const marker = new window.kakao.maps.Marker({
          position: new window.kakao.maps.LatLng(place.lat, place.lng),
        })
        const markerObj = { place, marker }
        markers.push(markerObj)
        searchResults.value.push(place)

        if (place.distance <= maxDistance) {
          marker.setMap(map)
          bounds.extend(marker.getPosition())
          marker.addListener('click', () => showInfo(place, marker))
        }
      })

      if (!bounds.isEmpty()) {
        map.setBounds(bounds)
      } else {
        map.setCenter(new window.kakao.maps.LatLng(locationStore.latitude, locationStore.longitude))
      }

      if (markers.length > 0) {
        const { place, marker } = markers[0]
        showInfo(place, marker)
      }
    }
  })
}

const showInfo = (place, marker) => {
  if (infowindow) infowindow.close()
  infowindow = new window.kakao.maps.InfoWindow({
    content: `<div style="padding:5px;font-size:14px;">${place.place_name}</div>`
  })
  infowindow.open(map, marker)
}

const focusPlace = (index) => {
  const { place, marker } = markers[index]
  map.panTo(marker.getPosition())
  marker.setMap(map)
  showInfo(place, marker)
}

const loadKakaoMap = (callback) => {
  if (window.kakao && window.kakao.maps) {
    window.kakao.maps.load(callback)
  } else {
    if (!document.querySelector('#kakao-map-script')) {
      const script = document.createElement('script')
      script.id = 'kakao-map-script'
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${MAP_API_KEY}&libraries=services&autoload=false`
      script.onload = () => window.kakao.maps.load(callback)
      document.head.appendChild(script)
    } else {
      const wait = setInterval(() => {
        if (window.kakao && window.kakao.maps) {
          clearInterval(wait)
          window.kakao.maps.load(callback)
        }
      }, 100)
    }
  }
}

onMounted(() => {
  locationStore.fetchCurrentLocation()
  loadKakaoMap(() => {
    initMap(locationStore.latitude, locationStore.longitude)
  })
})
</script>

<style scoped>
.main-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Pretendard', sans-serif;
}

.highlight {
  color: #0064ff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 1.8rem;
  text-align: center;
}

.subtitle {
  font-size: 14px;
  color: #666;
  margin: 12px 0 20px;
  text-align: center;
}

.search-form {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 24px;
}

.search-form input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.search-form button {
  all: unset;
  background-color: #0064ff;
  color: white;
  font-size: 14px;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-form button:hover {
  background-color: #0053d6;
}

.map-section {
  display: flex;
  gap: 24px;
}

.search-results {
  flex: 1.2;
  max-height: 600px;
  overflow-y: auto;
  border-radius: 12px;
  background-color: #f9f9f9;
  padding: 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.search-results ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.search-results li {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  font-size: 14px;
}

.search-results li:hover {
  background-color: #e6f2ff;
}

.map-box {
  flex: 2;
  height: 600px;
  border-radius: 12px;
  border: 1px solid #ddd;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>
