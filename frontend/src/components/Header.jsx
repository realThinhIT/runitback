import React from 'react'
import { AppBar, Toolbar, Typography, Box, IconButton, Chip } from '@mui/material'
import SportsBasketballIcon from '@mui/icons-material/SportsBasketball'
import PersonIcon from '@mui/icons-material/Person'
import ViewSidebarIcon from '@mui/icons-material/ViewSidebar'

function Header({ player, onProfileClick, onToggleSidebar, sidebarOpen }) {
  return (
    <AppBar position="static" elevation={0}>
      <Toolbar>
        <SportsBasketballIcon sx={{ mr: 1.5, fontSize: 32 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 700 }}>
          RunItBackHanoi
        </Typography>
        <IconButton
          color="inherit"
          onClick={onToggleSidebar}
          sx={{ mr: 1, opacity: sidebarOpen ? 1 : 0.6 }}
        >
          <ViewSidebarIcon />
        </IconButton>
        {player ? (
          <Chip
            icon={<PersonIcon />}
            label={player.name}
            onClick={onProfileClick}
            sx={{
              bgcolor: 'rgba(255,255,255,0.2)',
              color: 'white',
              '&:hover': { bgcolor: 'rgba(255,255,255,0.3)' },
            }}
          />
        ) : (
          <IconButton color="inherit" onClick={onProfileClick}>
            <PersonIcon />
          </IconButton>
        )}
      </Toolbar>
    </AppBar>
  )
}

export default Header
