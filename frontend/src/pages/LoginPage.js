import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../services/AuthContext';
import { Box, Button, TextField, Typography, Paper } from '@mui/material';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
      <Box sx={{ width: 370 }}>
        <div className="demo-brand">
          <img src="https://img.icons8.com/color/48/000000/money-bag.png" alt="logo" height={40} />
          Vibe FinOps
        </div>
        <Paper elevation={4} className="demo-card">
          <Typography variant="h5" mb={2} align="center" color="primary">Sign in to Demo</Typography>
          <form onSubmit={handleSubmit}>
            <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} fullWidth margin="normal" required autoFocus />
            <TextField label="Password" value={password} onChange={e => setPassword(e.target.value)} type="password" fullWidth margin="normal" required />
            {error && <Typography color="error" variant="body2" align="center" sx={{ mt: 1 }}>{error}</Typography>}
            <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2, py: 1.2, fontWeight: 'bold' }}>Login</Button>
          </form>
          <Typography variant="caption" color="text.secondary" display="block" align="center" sx={{ mt: 2 }}>
            Demo users: employee1, manager1, admin1<br />Password: password1, password2, password3
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
}
