import React, { useEffect, useState } from "react";
import { Button, Grid, Paper, List, ListItem, ListItemText, Box } from "@mui/material";
import api from "../api/axios";
import TaskTree from "../components/TaskTree";
import { useAuth } from "../context/AuthContext";

export default function ProjectsPage(){
  const [projects, setProjects] = useState<any[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [tasks, setTasks] = useState<any[]>([]);
  const { logout } = useAuth();

  const loadProjects = async ()=> {
    const r = await api.get("/projects/");
    setProjects(r.data);
  };
  const loadTasks = async (projId:number | null) => {
    const r = await api.get("/tasks/", { params: { project_id: projId }});
    setTasks(r.data);
  };

  useEffect(()=>{ loadProjects(); }, []);

  useEffect(()=>{ loadTasks(selected); }, [selected]);

  return (
    <Grid container spacing={2}>
      <Grid item xs={3}>
        <Paper sx={{p:2}}>
          <Button variant="outlined" onClick={async () => { const name = prompt("Project name"); if(name){ await api.post("/projects/", {name}); await loadProjects(); }}}>Add Project</Button>
          <List>
            {projects.map(p => (
              <ListItem key={p.id} button selected={selected===p.id} onClick={()=>setSelected(p.id)}>
                <ListItemText primary={p.name} />
              </ListItem>
            ))}
          </List>
          <Box sx={{mt:2}}>
            <Button color="error" onClick={()=>logout()}>Logout</Button>
          </Box>
        </Paper>
      </Grid>
      <Grid item xs={9}>
        <TaskTree tasks={tasks} onRefresh={()=>loadTasks(selected)} projectId={selected}/>
      </Grid>
    </Grid>
  );
}