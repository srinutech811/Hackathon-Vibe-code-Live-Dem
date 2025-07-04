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
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" bgcolor="#f5f5f5">
      <Paper elevation={3} sx={{ p: 4, width: 340 }}>
        <Typography variant="h5" mb={2}>Login</Typography>
        <form onSubmit={handleSubmit}>
          <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} fullWidth margin="normal" required />
          <TextField label="Password" value={password} onChange={e => setPassword(e.target.value)} type="password" fullWidth margin="normal" required />
          {error && <Typography color="error" variant="body2">{error}</Typography>}
          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>Login</Button>
        </form>
      </Paper>
    </Box>
  );
}
