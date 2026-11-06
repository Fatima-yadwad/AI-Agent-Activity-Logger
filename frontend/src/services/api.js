
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getExecutions = async () => {
  const response = await api.get("/executions");
  return response.data;
};

export const getStatistics = async () => {
  const response = await api.get("/statistics");
  return response.data;
};

export const getExecutionDetails = async (executionId) => {
  const response = await api.get(`/executions/${executionId}`);
  return response.data;
};

export const getExecutionLogs = async (executionId) => {
  const response = await api.get(`/executions/${executionId}/logs`);
  return response.data;
};

export default api;
