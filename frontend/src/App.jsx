import React, { useState, useEffect, useCallback } from 'react'
import { Box, Snackbar, Alert } from '@mui/material'
import Header from './components/Header'
import Chat from './components/Chat'
import Sidebar from './components/Sidebar'
import RegisterModal from './components/RegisterModal'

function App() {
  const [player, setPlayer] = useState(null)
  const [showRegister, setShowRegister] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [sidebarRefreshKey, setSidebarRefreshKey] = useState(0)
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'info' })
  const [prepopulatedInput, setPrepopulatedInput] = useState(null)

  const handleMatchUpdate = useCallback(() => {
    setSidebarRefreshKey((k) => k + 1)
  }, [])

  // Load player from localStorage on mount
  useEffect(() => {
    const savedPlayer = localStorage.getItem('runitback_player')
    if (savedPlayer) {
      try {
        setPlayer(JSON.parse(savedPlayer))
      } catch (e) {
        localStorage.removeItem('runitback_player')
        setShowRegister(true)
      }
    } else {
      // Prompt user to log in if not logged in
      setShowRegister(true)
    }
  }, [])

  const handleRegister = (newPlayer) => {
    if (newPlayer) {
      setPlayer(newPlayer)
      localStorage.setItem('runitback_player', JSON.stringify(newPlayer))
      setNotification({
        open: true,
        message: `Chào mừng ${newPlayer.name}!`,
        severity: 'success',
      })
    } else {
      // Logout
      setPlayer(null)
      localStorage.removeItem('runitback_player')
      setNotification({
        open: true,
        message: 'Đã đăng xuất',
        severity: 'info',
      })
    }
  }

  const handleCloseNotification = () => {
    setNotification((prev) => ({ ...prev, open: false }))
  }

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header
        player={player}
        onProfileClick={() => setShowRegister(true)}
        onToggleSidebar={() => setSidebarOpen((prev) => !prev)}
        sidebarOpen={sidebarOpen}
      />
      <Box sx={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        <Chat player={player} onMatchUpdate={handleMatchUpdate} prepopulatedInput={prepopulatedInput} />
        {sidebarOpen && (
          <Sidebar
            player={player}
            refreshKey={sidebarRefreshKey}
            onMatchClick={(template) => setPrepopulatedInput({ text: template, ts: Date.now() })}
          />
        )}
      </Box>

      <RegisterModal
        open={showRegister}
        onClose={() => { if (player) setShowRegister(false) }}
        onRegister={handleRegister}
        existingPlayer={player}
        required={!player}
      />

      <Snackbar
        open={notification.open}
        autoHideDuration={4000}
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          onClose={handleCloseNotification}
          severity={notification.severity}
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Box>
  )
}

export default App
