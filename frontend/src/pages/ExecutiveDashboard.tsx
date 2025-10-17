import React, { useEffect, useState } from "react";
import { 
  Box, Grid, Card, CardContent, Typography, LinearProgress,
  Chip, Paper, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Alert
} from "@mui/material";
import { 
  TrendingUp, TrendingDown, AttachMoney, Assignment,
  Warning, CheckCircle, Schedule
} from "@mui/icons-material";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function ExecutiveDashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [performance, setPerformance] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [analyticsRes, performanceRes] = await Promise.all([
        api.get("/analytics/dashboard"),
        api.get("/analytics/project-performance")
      ]);
      setAnalytics(analyticsRes.data);
      setPerformance(performanceRes.data);
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
    } finally {
      setLoading(false);
    }
  };

  const MetricCard = ({ title, value, subtitle, icon, color = "primary", trend = null }) => (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div" color={color}>
              {value}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {subtitle}
            </Typography>
          </Box>
          <Box color={`${color}.main`}>
            {icon}
          </Box>
        </Box>
        {trend && (
          <Box display="flex" alignItems="center" mt={1}>
            {trend > 0 ? <TrendingUp color="success" /> : <TrendingDown color="error" />}
            <Typography variant="body2" color={trend > 0 ? "success.main" : "error.main"}>
              {Math.abs(trend)}% from last month
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  const getHealthColor = (health) => {
    if (health >= 80) return "success";
    if (health >= 60) return "warning";
    return "error";
  };

  if (loading) return <LinearProgress />;

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Executive Dashboard
      </Typography>
      <Typography variant="body1" color="textSecondary" gutterBottom>
        Welcome back, {user?.first_name} {user?.last_name}
      </Typography>

      {analytics && (
        <>
          {/* Key Metrics */}
          <Grid container spacing={3} mb={3}>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard
                title="Active Projects"
                value={analytics.projects.active}
                subtitle={`${analytics.projects.completion_rate.toFixed(1)}% completion rate`}
                icon={<Assignment fontSize="large" />}
                color="primary"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard
                title="Budget Variance"
                value={`$${analytics.budget.variance.toLocaleString()}`}
                subtitle={`${analytics.budget.variance_percentage.toFixed(1)}% of planned`}
                icon={<AttachMoney fontSize="large" />}
                color={analytics.budget.variance >= 0 ? "success" : "error"}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard
                title="Task Completion"
                value={`${analytics.tasks.completion_rate.toFixed(1)}%`}
                subtitle={`${analytics.tasks.overdue} overdue tasks`}
                icon={<CheckCircle fontSize="large" />}
                color="info"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard
                title="High Risks"
                value={analytics.risks.high_risk}
                subtitle={`${analytics.risks.open} open risks total`}
                icon={<Warning fontSize="large" />}
                color="warning"
              />
            </Grid>
          </Grid>

          {/* Alerts */}
          {analytics.risks.high_risk > 0 && (
            <Alert severity="warning" sx={{ mb: 3 }}>
              You have {analytics.risks.high_risk} high-risk items requiring immediate attention.
            </Alert>
          )}

          {analytics.tasks.overdue > 0 && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {analytics.tasks.overdue} tasks are overdue and need immediate action.
            </Alert>
          )}

          {/* Project Performance Table */}
          <Paper sx={{ mb: 3 }}>
            <Box p={2}>
              <Typography variant="h6" gutterBottom>
                Project Performance Overview
              </Typography>
            </Box>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Project Name</TableCell>
                    <TableCell align="right">Progress</TableCell>
                    <TableCell align="right">Task Completion</TableCell>
                    <TableCell align="right">Budget Performance</TableCell>
                    <TableCell align="right">Risk Score</TableCell>
                    <TableCell align="right">Overall Health</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {performance.slice(0, 10).map((project) => (
                    <TableRow key={project.project_id}>
                      <TableCell component="th" scope="row">
                        {project.project_name}
                      </TableCell>
                      <TableCell align="right">
                        <Box display="flex" alignItems="center">
                          <Box width="100%" mr={1}>
                            <LinearProgress 
                              variant="determinate" 
                              value={project.completion_percentage} 
                            />
                          </Box>
                          <Box minWidth={35}>
                            <Typography variant="body2" color="textSecondary">
                              {project.completion_percentage}%
                            </Typography>
                          </Box>
                        </Box>
                      </TableCell>
                      <TableCell align="right">
                        {project.task_completion_rate.toFixed(1)}%
                      </TableCell>
                      <TableCell align="right">
                        <Chip 
                          label={`${project.budget_performance.toFixed(1)}%`}
                          color={project.budget_performance >= 0 ? "success" : "error"}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="right">
                        <Chip 
                          label={project.risk_score.toFixed(1)}
                          color={project.risk_score <= 5 ? "success" : project.risk_score <= 10 ? "warning" : "error"}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="right">
                        <Chip 
                          label={`${project.overall_health.toFixed(0)}%`}
                          color={getHealthColor(project.overall_health)}
                          size="small"
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </>
      )}
    </Box>
  );
}