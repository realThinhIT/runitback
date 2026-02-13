import React from 'react'
import { Box, Paper, Typography, Avatar } from '@mui/material'
import SportsBasketballIcon from '@mui/icons-material/SportsBasketball'
import PersonIcon from '@mui/icons-material/Person'

function Message({ message, isUser }) {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        mb: 2,
        px: 2,
      }}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: isUser ? 'row-reverse' : 'row',
          alignItems: 'flex-start',
          maxWidth: '80%',
        }}
      >
        <Avatar
          sx={{
            bgcolor: isUser ? 'secondary.main' : 'primary.main',
            width: 36,
            height: 36,
            mx: 1,
          }}
        >
          {isUser ? <PersonIcon /> : <SportsBasketballIcon />}
        </Avatar>
        <Paper
          elevation={0}
          sx={{
            p: 2,
            bgcolor: isUser ? 'secondary.main' : 'background.paper',
            color: isUser ? 'white' : 'text.primary',
            borderRadius: isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
            border: isUser ? 'none' : '1px solid #e0e0e0',
          }}
        >
          <Typography
            variant="body1"
            sx={{
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
            }}
          >
            {message}
          </Typography>
        </Paper>
      </Box>
    </Box>
  )
}

export default Message
