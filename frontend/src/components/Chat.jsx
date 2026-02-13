import React, { useState, useRef, useEffect } from 'react'
import {
  Box,
  TextField,
  IconButton,
  Paper,
  Typography,
  CircularProgress,
  Chip,
} from '@mui/material'
import SendIcon from '@mui/icons-material/Send'
import Message from './Message'
import { sendMessage } from '../services/api'

const MATCH_ACTIONS = new Set(['join_match', 'create_match', 'leave_match'])

const SUGGESTIONS = [
  'Có trận nào phù hợp với trình độ của tôi không?',
  'Ngày mai tôi rảnh, bạn gợi ý trận nào tôi có thể tham gia được không?',
  'Sân nào gần khu vực của tôi nhất?',
  'Tôi muốn tạo trận mới ở trình độ của tôi gần nhà tôi',
]

function Chat({ player, onMatchUpdate, prepopulatedInput }) {
  const [messages, setMessages] = useState([
    {
      text: 'Xin chào! Tôi là trợ lý RunItBackHanoi. Tôi có thể giúp bạn tìm trận đấu bóng rổ phù hợp, tham gia trận đấu, hoặc tra cứu thông tin sân. Bạn cần gì hôm nay?',
      isUser: false,
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    if (prepopulatedInput?.text) {
      setInput(prepopulatedInput.text)
      setTimeout(() => inputRef.current?.focus(), 0)
    }
  }, [prepopulatedInput])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')

    // Add user message
    setMessages((prev) => [...prev, { text: userMessage, isUser: true }])
    setIsLoading(true)

    try {
      // Build conversation history from existing messages (exclude the initial greeting)
      const history = messages.slice(1).map((msg) => ({
        role: msg.isUser ? 'user' : 'assistant',
        content: msg.text,
      }))

      const response = await sendMessage(userMessage, player?.id, history)
      setMessages((prev) => [...prev, { text: response.response, isUser: false }])

      // Refresh sidebar when a match-related action occurred
      if (response.action_result && MATCH_ACTIONS.has(response.action_result.type)) {
        onMatchUpdate?.()
      }
    } catch (error) {
      console.error('Error sending message:', error)
      setMessages((prev) => [
        ...prev,
        {
          text: 'Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.',
          isUser: false,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSuggestionClick = (text) => {
    setInput(text)
    setTimeout(() => inputRef.current?.focus(), 0)
  }

  const hasUserMessage = messages.length > 1

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        flex: 1,
        minWidth: 0,
        bgcolor: 'background.default',
      }}
    >
      {/* Messages area */}
      <Box
        sx={{
          flex: 1,
          overflowY: 'auto',
          py: 2,
        }}
      >
        {messages.map((msg, index) => (
          <Message key={index} message={msg.text} isUser={msg.isUser} />
        ))}
        {!hasUserMessage && !isLoading && (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, px: 2, ml: 6, mt: 1, maxWidth: 600 }}>
            {SUGGESTIONS.map((text) => (
              <Chip
                key={text}
                label={text}
                variant="outlined"
                onClick={() => handleSuggestionClick(text)}
                sx={{
                  cursor: 'pointer',
                  height: 'auto',
                  '& .MuiChip-label': { whiteSpace: 'normal', py: 0.75 },
                  '&:hover': { bgcolor: 'primary.50', borderColor: 'primary.main' },
                }}
              />
            ))}
          </Box>
        )}
        {isLoading && (
          <Box sx={{ display: 'flex', justifyContent: 'flex-start', px: 2, mb: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', ml: 6 }}>
              <CircularProgress size={24} sx={{ color: 'primary.main' }} />
              <Typography variant="body2" sx={{ ml: 1, color: 'text.secondary' }}>
                Đang suy nghĩ...
              </Typography>
            </Box>
          </Box>
        )}
        <div ref={messagesEndRef} />
      </Box>

      {/* Input area */}
      <Paper
        elevation={3}
        sx={{
          p: 2,
          borderRadius: 0,
          borderTop: '1px solid #e0e0e0',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', maxWidth: 800, mx: 'auto' }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder={
              player
                ? 'Nhập tin nhắn... (VD: "Tìm trận chơi tối nay ở Cầu Giấy")'
                : 'Nhập tin nhắn...'
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            inputRef={inputRef}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 3,
                bgcolor: 'background.default',
              },
            }}
          />
          <IconButton
            color="primary"
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            sx={{
              ml: 1,
              bgcolor: 'primary.main',
              color: 'white',
              '&:hover': { bgcolor: 'primary.dark' },
              '&.Mui-disabled': { bgcolor: 'grey.300', color: 'grey.500' },
            }}
          >
            <SendIcon />
          </IconButton>
        </Box>
        {!player && (
          <Typography
            variant="caption"
            sx={{ display: 'block', textAlign: 'center', mt: 1, color: 'text.secondary' }}
          >
            Đăng ký để được ghi nhận khi tham gia trận đấu
          </Typography>
        )}
      </Paper>
    </Box>
  )
}

export default Chat
