import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../services/AuthContext';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function AuditLogs() {
  const { token } = useAuth();
  const [logs, setLogs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLogs = async () => {
      const res = await axios.get('http://localhost:8000/audit/logs', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLogs(res.data);
    };
    fetchLogs();
  }, [token]);

  return (
    <Box p={4}>
      <div className="demo-brand">
        <img src="https://img.icons8.com/color/48/000000/money-bag.png" alt="logo" height={40} />
        Vibe FinOps
      </div>
      <Paper className="demo-card">
        <Typography variant="h5" mb={2} color="primary" align="center">Audit Logs</Typography>
        <Button variant="outlined" onClick={() => navigate('/dashboard')} sx={{ mb: 2 }}>Back to Dashboard</Button>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow sx={{ background: '#e3f0ff' }}>
                <TableCell>ID</TableCell>
                <TableCell>User</TableCell>
                <TableCell>Action</TableCell>
                <TableCell>Timestamp</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {logs.map(log => (
                <TableRow key={log.id}>
                  <TableCell>{log.id}</TableCell>
                  <TableCell>{log.user}</TableCell>
                  <TableCell>{log.action}</TableCell>
                  <TableCell>{log.timestamp}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
}
