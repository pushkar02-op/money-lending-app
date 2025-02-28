// src/components/KeyMetrics.js
import React from "react";
import { Card, CardContent, Typography, Grid } from "@mui/material";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#0088FE", "#00C49F"];

const KeyMetrics = ({ loans }) => {
  const totalLoans = loans.length;
  const totalAmountLent = loans.reduce(
    (acc, loan) => acc + (loan.amount || 0),
    0
  );
  const activeLoans = loans.filter((loan) => loan.status === "active").length;
  const completedLoans = loans.filter(
    (loan) => loan.status === "completed"
  ).length;

  const pieData = [
    { name: "Active", value: activeLoans },
    { name: "Completed", value: completedLoans },
  ];

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Typography variant="subtitle1">Total Loans</Typography>
            <Typography variant="h4">{totalLoans}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Typography variant="subtitle1">Total Amount Lent</Typography>
            <Typography variant="h4">₹ {totalAmountLent.toFixed(2)}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Typography variant="subtitle1">Active Loans</Typography>
            <Typography variant="h4">{activeLoans}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={3}>
        <Card>
          <CardContent>
            <Typography variant="subtitle1">Completed Loans</Typography>
            <Typography variant="h4">{completedLoans}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>
              Loan Status Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {pieData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default KeyMetrics;
