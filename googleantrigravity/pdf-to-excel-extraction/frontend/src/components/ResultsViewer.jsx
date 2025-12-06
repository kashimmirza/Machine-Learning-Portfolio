/**
 * Results viewer component for displaying extraction results and download options
 */

import { useState, useEffect } from 'react';
import { getExtractionResult, getDownloadUrl } from '../services/api';

const ResultsViewer = ({ jobId }) => {
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedDocument, setSelectedDocument] = useState(0);

    useEffect(() => {
        if (!jobId) return;

        const fetchResult = async () => {
            try {
                setLoading(true);
                const data = await getExtractionResult(jobId);
                setResult(data);
                setError(null);
            } catch (err) {
                console.error('Error fetching results:', err);
                setError(err.message || 'Failed to fetch results');
            } finally {
                setLoading(false);
            }
        };

        fetchResult();
    }, [jobId]);

    if (loading) {
        return (
            <div className="results-viewer loading">
                <div className="spinner"></div>
                <p>Loading results...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="results-viewer error">
                <p>Error: {error}</p>
            </div>
        );
    }

    if (!result || !result.documents || result.documents.length === 0) {
        return (
            <div className="results-viewer empty">
                <p>No results available</p>
            </div>
        );
    }

    const currentDoc = result.documents[selectedDocument];

    return (
        <div className="results-viewer">
            <div className="results-header">
                <h2>Extraction Results</h2>
                <div className="results-stats">
                    <div className="stat">
                        <span className="stat-label">Total:</span>
                        <span className="stat-value">{result.total_processed}</span>
                    </div>
                    <div className="stat success">
                        <span className="stat-label">Successful:</span>
                        <span className="stat-value">{result.successful}</span>
                    </div>
                    {result.failed > 0 && (
                        <div className="stat error">
                            <span className="stat-label">Failed:</span>
                            <span className="stat-value">{result.failed}</span>
                        </div>
                    )}
                </div>
            </div>

            {result.documents.length > 1 && (
                <div className="document-selector">
                    <label>Select Document:</label>
                    <select
                        value={selectedDocument}
                        onChange={(e) => setSelectedDocument(Number(e.target.value))}
                    >
                        {result.documents.map((doc, index) => (
                            <option key={index} value={index}>
                                {doc.filename} {!doc.success && '(Failed)'}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            <div className="document-details">
                <div className="detail-header">
                    <h3>{currentDoc.filename}</h3>
                    <span className={`status-badge ${currentDoc.success ? 'success' : 'error'}`}>
                        {currentDoc.success ? 'Success' : 'Failed'}
                    </span>
                </div>

                {currentDoc.error && (
                    <div className="error-alert">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span>{currentDoc.error}</span>
                    </div>
                )}

                {currentDoc.success && currentDoc.fields && currentDoc.fields.length > 0 && (
                    <div className="extracted-fields">
                        <h4>Extracted Data</h4>
                        <div className="fields-table">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Field</th>
                                        <th>Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {currentDoc.fields.map((field, index) => (
                                        <tr key={index}>
                                            <td className="field-name">{field.field_name}</td>
                                            <td className="field-value">
                                                {field.value !== null && field.value !== undefined
                                                    ? String(field.value)
                                                    : <span className="null-value">-</span>}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </div>

            <div className="download-section">
                <h3>Download Results</h3>
                <div className="download-buttons">
                    <a
                        href={getDownloadUrl(jobId, 'xlsx')}
                        className="btn btn-primary"
                        download
                    >
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Download Excel
                    </a>
                    <a
                        href={getDownloadUrl(jobId, 'csv')}
                        className="btn btn-secondary"
                        download
                    >
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Download CSV
                    </a>
                </div>
            </div>
        </div>
    );
};

export default ResultsViewer;
