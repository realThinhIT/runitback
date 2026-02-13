import React, { useState } from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography,
  Alert,
  CircularProgress,
} from '@mui/material'
import SportsBasketballIcon from '@mui/icons-material/SportsBasketball'
import { createPlayer, getPlayerByPhone } from '../services/api'

const SKILL_LEVELS = [
  { value: 'Beginner', label: 'Beginner - Mới chơi, đang học cơ bản' },
  { value: 'Intermediate', label: 'Intermediate - Chơi được, hiểu chiến thuật' },
  { value: 'Advanced', label: 'Advanced - Chơi tốt, thi đấu thường xuyên' },
]

const DISTRICTS = [
  'Ba Đình',
  'Hoàn Kiếm',
  'Hai Bà Trưng',
  'Đống Đa',
  'Cầu Giấy',
  'Thanh Xuân',
  'Hoàng Mai',
  'Long Biên',
  'Tây Hồ',
  'Nam Từ Liêm',
  'Bắc Từ Liêm',
  'Hà Đông',
]

function RegisterModal({ open, onClose, onRegister, existingPlayer, required }) {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    skill_level: 'Intermediate',
    preferred_district: 'Cầu Giấy',
  })
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [mode, setMode] = useState('register') // 'register' or 'login'

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    setError('')
  }

  const handleSubmit = async () => {
    setError('')

    if (mode === 'login') {
      // Login with phone
      if (!formData.phone) {
        setError('Vui lòng nhập số điện thoại')
        return
      }
      setIsLoading(true)
      try {
        const player = await getPlayerByPhone(formData.phone)
        if (player) {
          onRegister(player)
          onClose()
        } else {
          setError('Không tìm thấy tài khoản. Vui lòng đăng ký mới.')
          setMode('register')
        }
      } catch (err) {
        setError('Đã có lỗi xảy ra. Vui lòng thử lại.')
      } finally {
        setIsLoading(false)
      }
    } else {
      // Register new player
      if (!formData.name || !formData.phone) {
        setError('Vui lòng điền đầy đủ thông tin')
        return
      }
      setIsLoading(true)
      try {
        const player = await createPlayer(formData)
        onRegister(player)
        onClose()
      } catch (err) {
        setError('Đã có lỗi xảy ra. Vui lòng thử lại.')
      } finally {
        setIsLoading(false)
      }
    }
  }

  const handleLogout = () => {
    onRegister(null)
    onClose()
  }

  // If showing existing player info
  if (existingPlayer) {
    return (
      <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <SportsBasketballIcon sx={{ mr: 1, color: 'primary.main' }} />
            Thông tin của bạn
          </Box>
        </DialogTitle>
        <DialogContent>
          <Box sx={{ py: 2 }}>
            <Typography variant="body1" gutterBottom>
              <strong>Tên:</strong> {existingPlayer.name}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Số điện thoại:</strong> {existingPlayer.phone}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Trình độ:</strong> {existingPlayer.skill_level}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Khu vực:</strong> {existingPlayer.preferred_district}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>ID:</strong> {existingPlayer.id}
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleLogout} color="error">
            Đăng xuất
          </Button>
          <Button onClick={onClose} variant="contained">
            Đóng
          </Button>
        </DialogActions>
      </Dialog>
    )
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth disableEscapeKeyDown={required}>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <SportsBasketballIcon sx={{ mr: 1, color: 'primary.main' }} />
          {mode === 'login' ? 'Đăng nhập' : 'Đăng ký thành viên'}
        </Box>
      </DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 1 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {mode === 'login' ? (
            <TextField
              fullWidth
              label="Số điện thoại"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              margin="normal"
              placeholder="0912345678"
            />
          ) : (
            <>
              <TextField
                fullWidth
                label="Họ và tên"
                name="name"
                value={formData.name}
                onChange={handleChange}
                margin="normal"
                required
              />
              <TextField
                fullWidth
                label="Số điện thoại"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                margin="normal"
                required
                placeholder="0912345678"
              />
              <FormControl fullWidth margin="normal">
                <InputLabel>Trình độ</InputLabel>
                <Select
                  name="skill_level"
                  value={formData.skill_level}
                  label="Trình độ"
                  onChange={handleChange}
                >
                  {SKILL_LEVELS.map((level) => (
                    <MenuItem key={level.value} value={level.value}>
                      {level.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl fullWidth margin="normal">
                <InputLabel>Khu vực ưa thích</InputLabel>
                <Select
                  name="preferred_district"
                  value={formData.preferred_district}
                  label="Khu vực ưa thích"
                  onChange={handleChange}
                >
                  {DISTRICTS.map((district) => (
                    <MenuItem key={district} value={district}>
                      {district}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </>
          )}

          <Typography
            variant="body2"
            sx={{ mt: 2, textAlign: 'center', color: 'text.secondary' }}
          >
            {mode === 'login' ? (
              <>
                Chưa có tài khoản?{' '}
                <Button size="small" onClick={() => setMode('register')}>
                  Đăng ký
                </Button>
              </>
            ) : (
              <>
                Đã có tài khoản?{' '}
                <Button size="small" onClick={() => setMode('login')}>
                  Đăng nhập
                </Button>
              </>
            )}
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        {!required && <Button onClick={onClose}>Hủy</Button>}
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={isLoading}
          startIcon={isLoading ? <CircularProgress size={20} /> : null}
        >
          {mode === 'login' ? 'Đăng nhập' : 'Đăng ký'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default RegisterModal
