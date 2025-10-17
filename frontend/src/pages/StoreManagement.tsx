import React, { useEffect, useState } from "react";
import { 
  Box, Grid, Paper, List, ListItem, ListItemText, IconButton, 
  Button, Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, FormControl, InputLabel, Select, MenuItem,
  Chip, Typography
} from "@mui/material";
import { Add, Edit, Delete, Store as StoreIcon } from "@mui/icons-material";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

export default function StoreManagement() {
  const [stores, setStores] = useState([]);
  const [open, setOpen] = useState(false);
  const [editingStore, setEditingStore] = useState(null);
  const [formData, setFormData] = useState({
    store_number: "",
    name: "",
    region: "",
    district: "",
    format: ""
  });
  const { user } = useAuth();

  useEffect(() => {
    loadStores();
  }, []);

  const loadStores = async () => {
    try {
      const response = await api.get("/stores/");
      setStores(response.data);
    } catch (error) {
      console.error("Failed to load stores:", error);
    }
  };

  const handleSubmit = async () => {
    try {
      if (editingStore) {
        await api.put(`/stores/${editingStore.id}`, formData);
      } else {
        await api.post("/stores/", formData);
      }
      await loadStores();
      handleClose();
    } catch (error) {
      console.error("Failed to save store:", error);
    }
  };

  const handleClose = () => {
    setOpen(false);
    setEditingStore(null);
    setFormData({
      store_number: "",
      name: "",
      region: "",
      district: "",
      format: ""
    });
  };

  const handleEdit = (store) => {
    setEditingStore(store);
    setFormData({
      store_number: store.store_number,
      name: store.name,
      region: store.region || "",
      district: store.district || "",
      format: store.format || ""
    });
    setOpen(true);
  };

  const handleDelete = async (storeId) => {
    if (window.confirm("Are you sure you want to delete this store?")) {
      try {
        await api.delete(`/stores/${storeId}`);
        await loadStores();
      } catch (error) {
        console.error("Failed to delete store:", error);
      }
    }
  };

  const canManageStores = user?.role === "admin" || user?.role === "manager";

  return (
    <Box p={3}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Store Management</Typography>
        {canManageStores && (
          <Button 
            variant="contained" 
            startIcon={<Add />}
            onClick={() => setOpen(true)}
          >
            Add Store
          </Button>
        )}
      </Box>

      <Grid container spacing={3}>
        {stores.map((store) => (
          <Grid item xs={12} sm={6} md={4} key={store.id}>
            <Paper sx={{ p: 2 }}>
              <Box display="flex" alignItems="center" mb={2}>
                <StoreIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">{store.name}</Typography>
              </Box>
              
              <Typography variant="body2" color="textSecondary" gutterBottom>
                Store #{store.store_number}
              </Typography>
              
              {store.region && (
                <Chip label={store.region} size="small" color="primary" sx={{ mr: 1, mb: 1 }} />
              )}
              {store.format && (
                <Chip label={store.format} size="small" color="secondary" sx={{ mr: 1, mb: 1 }} />
              )}
              
              {store.district && (
                <Typography variant="body2" color="textSecondary">
                  District: {store.district}
                </Typography>
              )}

              {canManageStores && (
                <Box mt={2} display="flex" justifyContent="flex-end">
                  <IconButton onClick={() => handleEdit(store)} size="small">
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(store.id)} size="small">
                    <Delete />
                  </IconButton>
                </Box>
              )}
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Add/Edit Dialog */}
      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingStore ? "Edit Store" : "Add New Store"}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Store Number"
            fullWidth
            variant="outlined"
            value={formData.store_number}
            onChange={(e) => setFormData({ ...formData, store_number: e.target.value })}
            required
          />
          <TextField
            margin="dense"
            label="Store Name"
            fullWidth
            variant="outlined"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
          <TextField
            margin="dense"
            label="Region"
            fullWidth
            variant="outlined"
            value={formData.region}
            onChange={(e) => setFormData({ ...formData, region: e.target.value })}
          />
          <TextField
            margin="dense"
            label="District"
            fullWidth
            variant="outlined"
            value={formData.district}
            onChange={(e) => setFormData({ ...formData, district: e.target.value })}
          />
          <FormControl fullWidth margin="dense" variant="outlined">
            <InputLabel>Format</InputLabel>
            <Select
              value={formData.format}
              onChange={(e) => setFormData({ ...formData, format: e.target.value })}
              label="Format"
            >
              <MenuItem value="">Select Format</MenuItem>
              <MenuItem value="Supercenter">Supercenter</MenuItem>
              <MenuItem value="Neighborhood Market">Neighborhood Market</MenuItem>
              <MenuItem value="Express">Express</MenuItem>
              <MenuItem value="Sam's Club">Sam's Club</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editingStore ? "Update" : "Create"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}