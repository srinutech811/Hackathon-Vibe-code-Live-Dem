import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../services/AuthContext';
import { Box, Typography, Paper, Grid, Button, Avatar } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const { user, logout, token } = useAuth();
  const [summary, setSummary] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSummary = async () => {
      const res = await axios.get('http://localhost:8000/financial/summary', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSummary(res.data);
    };
    fetchSummary();
  }, [token]);

  return (
    <Box p={4}>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
        <div className="demo-brand">
          <img src="https://img.icons8.com/color/48/000000/money-bag.png" alt="logo" height={40} />
          Vibe FinOps
        </div>
        <Box display="flex" alignItems="center" gap={2}>
          <Avatar sx={{ bgcolor: '#1976d2' }}>{user?.username?.[0]?.toUpperCase()}</Avatar>
          <Typography variant="subtitle1">{user?.username} ({user?.role})</Typography>
          <Button color="secondary" variant="outlined" onClick={logout}>Logout</Button>
        </Box>
      </Box>
      {summary && (
        <Grid container spacing={3} mt={2}>
          <Grid item xs={12} md={4}>
            <Paper className="demo-card" sx={{ borderTop: '5px solid #1976d2' }}>
              <Typography variant="h6" color="primary">Total Budget</Typography>
              <Typography variant="h4" color="#1976d2">${summary.total_budget.toLocaleString()}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper className="demo-card" sx={{ borderTop: '5px solid #43a047' }}>
              <Typography variant="h6" color="success.main">Total Spent</Typography>
              <Typography variant="h4" color="#43a047">${summary.total_spent.toLocaleString()}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper className="demo-card" sx={{ borderTop: '5px solid #fbc02d' }}>
              <Typography variant="h6" color="warning.main">Remaining Budget</Typography>
              <Typography variant="h4" color="#fbc02d">${summary.remaining_budget.toLocaleString()}</Typography>
            </Paper>
          </Grid>
        </Grid>
      )}
      <Box mt={4}>
        <Button variant="contained" onClick={() => navigate('/transactions')} sx={{ mr: 2 }}>View Transactions</Button>
        {user?.role === 'admin' && <Button variant="outlined" onClick={() => navigate('/audit-logs')}>View Audit Logs</Button>}
      </Box>
    </Box>
  );
}
