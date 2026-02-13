import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Chat API
export const sendMessage = async (message, playerId = null, conversationHistory = []) => {
  const response = await api.post('/chat', {
    message,
    player_id: playerId,
    conversation_history: conversationHistory,
  })
  return response.data
}

// Player API
export const createPlayer = async (playerData) => {
  const response = await api.post('/players', playerData)
  return response.data
}

export const getPlayerByPhone = async (phone) => {
  try {
    const response = await api.get(`/players/${phone}`)
    return response.data
  } catch (error) {
    if (error.response?.status === 404) {
      return null
    }
    throw error
  }
}

// Courts API
export const getAllCourts = async () => {
  const response = await api.get('/courts')
  return response.data
}

// Matches API
export const getAllMatches = async () => {
  const response = await api.get('/matches')
  return response.data
}

export const getOpenMatches = async () => {
  const response = await api.get('/matches/open')
  return response.data
}

export const joinMatch = async (matchId, playerId) => {
  const response = await api.post(`/matches/${matchId}/join?player_id=${playerId}`)
  return response.data
}

export default api
