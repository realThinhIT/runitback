import React, { useState, useEffect, useCallback } from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  IconButton,
  CircularProgress,
  Divider,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material'
import InfoIcon from '@mui/icons-material/Info'
import HowToRegIcon from '@mui/icons-material/HowToReg'
import PeopleIcon from '@mui/icons-material/People'
import ExitToAppIcon from '@mui/icons-material/ExitToApp'
import RefreshIcon from '@mui/icons-material/Refresh'
import PersonIcon from '@mui/icons-material/Person'
import PhoneIcon from '@mui/icons-material/Phone'
import StarIcon from '@mui/icons-material/Star'
import LocationOnIcon from '@mui/icons-material/LocationOn'
import AccessTimeIcon from '@mui/icons-material/AccessTime'
import GroupsIcon from '@mui/icons-material/Groups'
import { getAllCourts, getOpenMatches, getAllMatches } from '../services/api'

function Sidebar({ player, refreshKey, onMatchClick }) {
  const [matches, setMatches] = useState([])
  const [myMatches, setMyMatches] = useState([])
  const [courts, setCourts] = useState([])
  const [loading, setLoading] = useState(false)
  const [menuAnchor, setMenuAnchor] = useState(null)
  const [selectedMatch, setSelectedMatch] = useState(null)
  const [selectedSection, setSelectedSection] = useState(null)

  const handleMatchCardClick = (event, match, section) => {
    setMenuAnchor(event.currentTarget)
    setSelectedMatch(match)
    setSelectedSection(section)
  }

  const handleMenuClose = () => {
    setMenuAnchor(null)
    setSelectedMatch(null)
    setSelectedSection(null)
  }

  const handleActionSelect = (template) => {
    onMatchClick?.(template)
    handleMenuClose()
  }

  const getMatchLabel = (match) => {
    const courtName = match.court_name || `Court #${match.court_id}`
    const datetime = match.datetime || `${match.date || ''} ${match.time || ''}`.trim()
    return { courtName, datetime, matchId: match.id }
  }

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const [matchesData, allMatchesData, courtsData] = await Promise.all([
        getOpenMatches(),
        player?.id ? getAllMatches() : Promise.resolve([]),
        getAllCourts(),
      ])
      setMatches(matchesData)
      if (player?.id) {
        setMyMatches(allMatchesData.filter((m) => m.player_ids?.includes(player.id)))
      }
      setCourts(courtsData)
    } catch (err) {
      console.error('Failed to fetch sidebar data:', err)
    } finally {
      setLoading(false)
    }
  }, [player?.id])

  useEffect(() => {
    fetchData()
  }, [fetchData, refreshKey])

  const statusColor = (status) => {
    switch (status) {
      case 'open': return 'success'
      case 'full': return 'warning'
      case 'completed': return 'default'
      default: return 'info'
    }
  }

  return (
    <Box
      sx={{
        width: 320,
        minWidth: 320,
        height: '100%',
        overflow: 'auto',
        bgcolor: 'background.default',
        borderLeft: '1px solid',
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header with refresh */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', px: 2, py: 1.5 }}>
        <Typography variant="h2" sx={{ fontSize: '1.1rem' }}>Dashboard</Typography>
        <IconButton size="small" onClick={fetchData} disabled={loading}>
          {loading ? <CircularProgress size={20} /> : <RefreshIcon fontSize="small" />}
        </IconButton>
      </Box>

      <Divider />

      <Box sx={{ overflow: 'auto', flex: 1, px: 2, py: 1.5 }}>
        {/* User Profile */}
        {player && (
          <>
            <Typography variant="body2" color="text.secondary" fontWeight={600} sx={{ mb: 1 }}>
              Hồ sơ của bạn
            </Typography>
            <Card variant="outlined" sx={{ mb: 2 }}>
              <CardContent sx={{ py: 1.5, px: 2, '&:last-child': { pb: 1.5 } }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                  <PersonIcon fontSize="small" color="primary" />
                  <Typography variant="body1" fontWeight={600}>{player.name}</Typography>
                </Box>
                {player.phone && (
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                    <PhoneIcon fontSize="small" color="action" />
                    <Typography variant="body2" color="text.secondary">{player.phone}</Typography>
                  </Box>
                )}
                {player.skill_level && (
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                    <StarIcon fontSize="small" color="action" />
                    <Typography variant="body2" color="text.secondary">Level: {player.skill_level}</Typography>
                  </Box>
                )}
                {player.preferred_district && (
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <LocationOnIcon fontSize="small" color="action" />
                    <Typography variant="body2" color="text.secondary">{player.preferred_district}</Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </>
        )}

        {/* My Matches */}
        {player && (
          <>
            <Typography variant="body2" color="text.secondary" fontWeight={600} sx={{ mb: 1 }}>
              Trận đấu của tôi ({myMatches.length})
            </Typography>
            {myMatches.length === 0 && !loading && (
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2, fontStyle: 'italic' }}>
                Bạn chưa tham gia trận đấu nào
              </Typography>
            )}
            {myMatches.map((match) => (
              <Card
                key={match.id}
                variant="outlined"
                onClick={(e) => handleMatchCardClick(e, match, 'my')}
                sx={{ mb: 1, borderColor: 'primary.light', cursor: 'pointer', '&:hover': { borderColor: 'primary.main', boxShadow: 1 } }}
              >
                <CardContent sx={{ py: 1, px: 2, '&:last-child': { pb: 1 } }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
                    <Typography variant="body2" fontWeight={600} noWrap sx={{ flex: 1, mr: 1 }}>
                      {match.court_name || `Court #${match.court_id}`}
                    </Typography>
                    <Chip label={match.status} color={statusColor(match.status)} size="small" />
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                    {match.datetime && (
                      <Typography variant="caption" color="text.secondary">
                        <AccessTimeIcon sx={{ fontSize: 12, mr: 0.3, verticalAlign: 'middle' }} />
                        {match.datetime}
                      </Typography>
                    )}
                    {match.skill_level && (
                      <Typography variant="caption" color="text.secondary">
                        <StarIcon sx={{ fontSize: 12, mr: 0.3, verticalAlign: 'middle' }} />
                        {match.skill_level}
                      </Typography>
                    )}
                    <Typography variant="caption" color="text.secondary">
                      <GroupsIcon sx={{ fontSize: 12, mr: 0.3, verticalAlign: 'middle' }} />
                      {match.current_players || 0}/{match.max_players || 10}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            ))}
            <Divider sx={{ my: 1.5 }} />
          </>
        )}

        {/* Open Matches */}
        <Typography variant="body2" color="text.secondary" fontWeight={600} sx={{ mb: 1 }}>
          Trận đấu mở ({matches.length})
        </Typography>
        {matches.length === 0 && !loading && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2, fontStyle: 'italic' }}>
            Chưa có trận đấu nào
          </Typography>
        )}
        {matches.map((match) => (
          <Card
            key={match.id}
            variant="outlined"
            onClick={(e) => handleMatchCardClick(e, match, 'open')}
            sx={{ mb: 1, cursor: 'pointer', '&:hover': { borderColor: 'primary.main', boxShadow: 1 } }}
          >
            <CardContent sx={{ py: 1, px: 2, '&:last-child': { pb: 1 } }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
                <Typography variant="body2" fontWeight={600} noWrap sx={{ flex: 1, mr: 1 }}>
                  {match.court_name || `Court #${match.court_id}`}
                </Typography>
                <Chip label={match.status} color={statusColor(match.status)} size="small" />
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                {match.date && (
                  <Typography variant="caption" color="text.secondary">
                    <AccessTimeIcon sx={{ fontSize: 12, mr: 0.3, verticalAlign: 'middle' }} />
                    {match.date} {match.time}
                  </Typography>
                )}
                {match.skill_level && (
                  <Typography variant="caption" color="text.secondary">
                    <StarIcon sx={{ fontSize: 12, mr: 0.3, verticalAlign: 'middle' }} />
                    {match.skill_level}
                  </Typography>
                )}
                <Typography variant="caption" color="text.secondary">
                  <GroupsIcon sx={{ fontSize: 12, mr: 0.3, verticalAlign: 'middle' }} />
                  {match.current_players || 0}/{match.max_players || 10}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        ))}

        {/* Courts */}
        <Typography variant="body2" color="text.secondary" fontWeight={600} sx={{ mt: 2, mb: 1 }}>
          Sân ({courts.length})
        </Typography>
        {courts.length === 0 && !loading && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2, fontStyle: 'italic' }}>
            Chưa có sân nào
          </Typography>
        )}
        {courts.map((court) => (
          <Card key={court.id} variant="outlined" sx={{ mb: 1 }}>
            <CardContent sx={{ py: 1, px: 2, '&:last-child': { pb: 1 } }}>
              <Typography variant="body2" fontWeight={600}>{court.name}</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                {court.district && (
                  <Typography variant="caption" color="text.secondary">
                    <LocationOnIcon sx={{ fontSize: 12, mr: 0.3, verticalAlign: 'middle' }} />
                    {court.district}
                  </Typography>
                )}
                {court.price_per_hour != null && (
                  <Typography variant="caption" color="text.secondary">
                    {Number(court.price_per_hour).toLocaleString()}đ/h
                  </Typography>
                )}
                {court.opening_hours && (
                  <Typography variant="caption" color="text.secondary">
                    <AccessTimeIcon sx={{ fontSize: 12, mr: 0.3, verticalAlign: 'middle' }} />
                    {court.opening_hours}
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>
        ))}
      </Box>

      {/* Quick action menu for match cards */}
      <Menu
        anchorEl={menuAnchor}
        open={Boolean(menuAnchor)}
        onClose={handleMenuClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
        transformOrigin={{ vertical: 'top', horizontal: 'left' }}
      >
        {selectedMatch && (() => {
          const { courtName, datetime, matchId } = getMatchLabel(selectedMatch)
          return [
            <MenuItem key="info" onClick={() => handleActionSelect(`Cho tôi biết thêm thông tin về trận đấu tại ${courtName} lúc ${datetime} (${matchId})`)}>
              <ListItemIcon><InfoIcon fontSize="small" /></ListItemIcon>
              <ListItemText>Thông tin thêm về trận này</ListItemText>
            </MenuItem>,
            <MenuItem key="join" onClick={() => handleActionSelect(`Tôi muốn tham gia trận đấu tại ${courtName} lúc ${datetime} (${matchId})`)}>
              <ListItemIcon><HowToRegIcon fontSize="small" /></ListItemIcon>
              <ListItemText>Đăng ký tham gia trận này</ListItemText>
            </MenuItem>,
            <MenuItem key="who" onClick={() => handleActionSelect(`Ai đã đăng ký chơi trận đấu tại ${courtName} lúc ${datetime} (${matchId})?`)}>
              <ListItemIcon><PeopleIcon fontSize="small" /></ListItemIcon>
              <ListItemText>Ai đang chơi trận này?</ListItemText>
            </MenuItem>,
            selectedSection === 'my' && (
              <MenuItem key="leave" onClick={() => handleActionSelect(`Tôi muốn rời trận đấu tại ${courtName} lúc ${datetime} (${matchId})`)}>
                <ListItemIcon><ExitToAppIcon fontSize="small" /></ListItemIcon>
                <ListItemText>Rời trận này</ListItemText>
              </MenuItem>
            ),
          ]
        })()}
      </Menu>
    </Box>
  )
}

export default Sidebar
