import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../services/AuthContext';
import { Box, Typography, Paper, Grid, Button } from '@mui/material';
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
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h4">Financial Dashboard</Typography>
        <Box>
          <Typography variant="subtitle1" sx={{ mr: 2, display: 'inline' }}>{user?.username} ({user?.role})</Typography>
          <Button color="secondary" onClick={logout}>Logout</Button>
        </Box>
      </Box>
      {summary && (
        <Grid container spacing={3} mt={2}>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">Total Budget</Typography>
              <Typography variant="h5">${summary.total_budget.toLocaleString()}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">Total Spent</Typography>
              <Typography variant="h5">${summary.total_spent.toLocaleString()}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6">Remaining Budget</Typography>
              <Typography variant="h5">${summary.remaining_budget.toLocaleString()}</Typography>
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
