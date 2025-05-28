import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useYoutubeStore = defineStore('youtube', () => {
  const videos = ref([])
  const laterVideos = ref([])

  const YOUTUBE_API_URL = 'http://localhost:8000/finances'
  const loaddata = function (keyword) {
    axios.get(`${YOUTUBE_API_URL}/youtube/`, {
      params: {
        q: keyword
      }
    })
    .then(response => {
      videos.value = response.data.items
    })
    .catch(err => {
      console.error('유튜브 검색 실패:', err)
    })
  }

  const findVideo = (id) => videos.value.find(v => v.id.videoId === id)

  const addVideo = (video) => laterVideos.value.push(video)
  const deleteVideo = (video) => {
    const idx = laterVideos.value.indexOf(video)
    if (idx !== -1) laterVideos.value.splice(idx, 1)
  }

  const loadFromLocalStorage = () => {
    const localData = JSON.parse(localStorage.getItem('youtube') || '{}')
    laterVideos.value = localData.laterVideos || []
    videos.value = localData.videos || []
  }

  return {
    videos,
    laterVideos,
    loaddata,
    findVideo,
    addVideo,
    deleteVideo,
    loadFromLocalStorage,
  }
})