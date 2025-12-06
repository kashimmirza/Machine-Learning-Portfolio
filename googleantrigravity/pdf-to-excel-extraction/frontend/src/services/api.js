/**
 * API client for backend communication
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Upload PDF files
 * @param {File[]} files - Array of PDF files
 * @returns {Promise} Upload response with file IDs
 */
export const uploadFiles = async (files) => {
    const formData = new FormData();
    files.forEach((file) => {
        formData.append('files', file);
    });

    const response = await api.post('/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

/**
 * Start extraction process
 * @param {Object} params - Extraction parameters
 * @returns {Promise} Extraction job status
 */
export const startExtraction = async (params) => {
    const response = await api.post('/extract/start', params);
    return response.data;
};

/**
 * Get extraction status
 * @param {string} jobId - Job ID
 * @returns {Promise} Current job status
 */
export const getExtractionStatus = async (jobId) => {
    const response = await api.get(`/extract/status/${jobId}`);
    return response.data;
};

/**
 * Get extraction results
 * @param {string} jobId - Job ID
 * @returns {Promise} Extraction results
 */
export const getExtractionResult = async (jobId) => {
    const response = await api.get(`/extract/result/${jobId}`);
    return response.data;
};

/**
 * Get export file info
 * @param {string} jobId - Job ID
 * @returns {Promise} Export file information
 */
export const getExportInfo = async (jobId) => {
    const response = await api.get(`/export/info/${jobId}`);
    return response.data;
};

/**
 * Get download URL
 * @param {string} jobId - Job ID
 * @param {string} format - File format (xlsx or csv)
 * @returns {string} Download URL
 */
export const getDownloadUrl = (jobId, format = 'xlsx') => {
    if (format === 'csv') {
        return `${API_BASE_URL}/export/download/${jobId}/csv`;
    }
    return `${API_BASE_URL}/export/download/${jobId}`;
};

/**
 * Delete uploaded file
 * @param {string} fileId - File ID
 * @returns {Promise} Delete response
 */
export const deleteFile = async (fileId) => {
    const response = await api.delete(`/upload/${fileId}`);
    return response.data;
};

/**
 * Delete extraction job
 * @param {string} jobId - Job ID
 * @returns {Promise} Delete response
 */
export const deleteJob = async (jobId) => {
    const response = await api.delete(`/extract/${jobId}`);
    return response.data;
};

/**
 * List uploaded files
 * @returns {Promise} List of uploaded files
 */
export const listUploadedFiles = async () => {
    const response = await api.get('/upload/list');
    return response.data;
};

/**
 * Health check
 * @returns {Promise} API health status
 */
export const healthCheck = async () => {
    const response = await api.get('/health');
    return response.data;
};

export default api;
