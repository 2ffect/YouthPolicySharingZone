import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLocationStore = defineStore('location', () => {
  const latitude = ref('latitude', null)
  const longitude = ref('longitude', null)

  const fetchCurrentLocation = () => {
    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        pos => {
          latitude.value = pos.coords.latitude
          longitude.value = pos.coords.longitude
          resolve({ latitude: latitude.value, longitude: longitude.value })
        },
        err => reject(err),
        { enableHighAccuracy: true }
      )
    })
  }

  return { latitude, longitude, fetchCurrentLocation }
}, {persist: true})
