import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../services/AuthContext';
import { Box, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function Transactions() {
  const { token } = useAuth();
  const [transactions, setTransactions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTransactions = async () => {
      const res = await axios.get('http://localhost:8000/financial/transactions', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTransactions(res.data);
    };
    fetchTransactions();
  }, [token]);

  return (
    <Box p={4}>
      <Typography variant="h4" mb={2}>Transactions</Typography>
      <Button variant="outlined" onClick={() => navigate('/dashboard')} sx={{ mb: 2 }}>Back to Dashboard</Button>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Department</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map(txn => (
              <TableRow key={txn.id}>
                <TableCell>{txn.id}</TableCell>
                <TableCell>{txn.department}</TableCell>
                <TableCell>${txn.amount.toLocaleString()}</TableCell>
                <TableCell>{txn.category}</TableCell>
                <TableCell>{txn.date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
