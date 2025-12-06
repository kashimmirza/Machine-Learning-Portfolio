/**
 * Processing status component with real-time progress
 */

import { useEffect, useState } from 'react';
import { getExtractionStatus } from '../services/api';

const ProcessingStatus = ({ jobId, onComplete, onError }) => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!jobId) return;

        let intervalId;

        const checkStatus = async () => {
            try {
                const statusData = await getExtractionStatus(jobId);
                setStatus(statusData);
                setLoading(false);

                // Stop polling if completed or failed
                if (statusData.status === 'completed') {
                    clearInterval(intervalId);
                    if (onComplete) {
                        onComplete(statusData);
                    }
                } else if (statusData.status === 'failed') {
                    clearInterval(intervalId);
                    if (onError) {
                        onError(statusData.error_message || 'Extraction failed');
                    }
                }
            } catch (error) {
                console.error('Error checking status:', error);
                setLoading(false);
                if (onError) {
                    onError(error.message);
                }
            }
        };

        // Initial check
        checkStatus();

        // Poll every 2 seconds
        intervalId = setInterval(checkStatus, 2000);

        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    }, [jobId, onComplete, onError]);

    if (loading) {
        return (
            <div className="processing-status">
                <div className="spinner"></div>
                <p>Initializing extraction...</p>
            </div>
        );
    }

    if (!status) {
        return null;
    }

    const getStatusColor = () => {
        switch (status.status) {
            case 'completed':
                return 'success';
            case 'failed':
                return 'error';
            case 'processing':
                return 'processing';
            default:
                return 'pending';
        }
    };

    const getStatusIcon = () => {
        switch (status.status) {
            case 'completed':
                return (
                    <svg className="status-icon success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                );
            case 'failed':
                return (
                    <svg className="status-icon error" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                );
            case 'processing':
                return <div className="spinner small"></div>;
            default:
                return (
                    <svg className="status-icon pending" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                );
        }
    };

    return (
        <div className={`processing-status ${getStatusColor()}`}>
            <div className="status-header">
                {getStatusIcon()}
                <div className="status-info">
                    <h3 className="status-title">
                        {status.status === 'completed' && 'Extraction Complete'}
                        {status.status === 'failed' && 'Extraction Failed'}
                        {status.status === 'processing' && 'Processing Documents'}
                        {status.status === 'pending' && 'Pending'}
                    </h3>
                    <p className="status-subtitle">
                        {status.files_processed} of {status.total_files} files processed
                    </p>
                </div>
            </div>

            <div className="progress-bar">
                <div
                    className="progress-fill"
                    style={{ width: `${status.progress}%` }}
                ></div>
            </div>

            <div className="progress-text">
                {status.progress.toFixed(0)}% Complete
            </div>

            {status.current_file && (
                <div className="current-file">
                    <span className="label">Processing:</span>
                    <span className="filename">{status.current_file}</span>
                </div>
            )}

            {status.error_message && (
                <div className="error-message">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{status.error_message}</span>
                </div>
            )}

            {status.status === 'completed' && (
                <div className="success-message">
                    <p>✓ All files processed successfully!</p>
                </div>
            )}
        </div>
    );
};

export default ProcessingStatus;
