/**
 * Main application component
 */

import { useState } from 'react';
import FileUploader from './components/FileUploader';
import ProcessingStatus from './components/ProcessingStatus';
import ResultsViewer from './components/ResultsViewer';
import { uploadFiles, startExtraction } from './services/api';
import './App.css';

function App() {
    const [step, setStep] = useState('upload'); // upload, configure, processing, results
    const [files, setFiles] = useState([]);
    const [uploadedFileIds, setUploadedFileIds] = useState([]);
    const [jobId, setJobId] = useState(null);
    const [documentType, setDocumentType] = useState('unknown');
    const [consolidate, setConsolidate] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);

    const handleFilesSelected = (selectedFiles) => {
        setFiles(selectedFiles);
        setError(null);
    };

    const handleUpload = async () => {
        if (files.length === 0) {
            setError('Please select at least one PDF file');
            return;
        }

        try {
            setUploading(true);
            setError(null);

            const response = await uploadFiles(files);

            if (response.success) {
                const fileIds = response.files.map(f => f.file_id);
                setUploadedFileIds(fileIds);
                setStep('configure');
            } else {
                setError('Upload failed');
            }
        } catch (err) {
            console.error('Upload error:', err);
            setError(err.response?.data?.detail || err.message || 'Upload failed');
        } finally {
            setUploading(false);
        }
    };

    const handleStartExtraction = async () => {
        try {
            setError(null);

            const response = await startExtraction({
                file_ids: uploadedFileIds,
                document_type: documentType,
                custom_fields: null,
                consolidate: consolidate,
            });

            setJobId(response.job_id);
            setStep('processing');
        } catch (err) {
            console.error('Extraction error:', err);
            setError(err.response?.data?.detail || err.message || 'Failed to start extraction');
        }
    };

    const handleComplete = () => {
        setStep('results');
    };

    const handleError = (errorMessage) => {
        setError(errorMessage);
        setStep('results');
    };

    const handleReset = () => {
        setStep('upload');
        setFiles([]);
        setUploadedFileIds([]);
        setJobId(null);
        setDocumentType('unknown');
        setConsolidate(true);
        setError(null);
    };

    return (
        <div className="app">
            <header className="app-header">
                <h1>PDF to Excel Extraction</h1>
                <p className="tagline">
                    AI-powered document extraction for invoices and utility bills
                </p>
            </header>

            <main className="app-main">
                {/* Progress Steps */}
                <div className="steps-indicator">
                    <div className={`step ${step === 'upload' ? 'active' : step !== 'upload' ? 'completed' : ''}`}>
                        <div className="step-number">1</div>
                        <div className="step-label">Upload</div>
                    </div>
                    <div className="step-line"></div>
                    <div className={`step ${step === 'configure' ? 'active' : step === 'processing' || step === 'results' ? 'completed' : ''}`}>
                        <div className="step-number">2</div>
                        <div className="step-label">Configure</div>
                    </div>
                    <div className="step-line"></div>
                    <div className={`step ${step === 'processing' ? 'active' : step === 'results' ? 'completed' : ''}`}>
                        <div className="step-number">3</div>
                        <div className="step-label">Process</div>
                    </div>
                    <div className="step-line"></div>
                    <div className={`step ${step === 'results' ? 'active' : ''}`}>
                        <div className="step-number">4</div>
                        <div className="step-label">Results</div>
                    </div>
                </div>

                {/* Error Display */}
                {error && (
                    <div className="error-banner">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span>{error}</span>
                        <button onClick={() => setError(null)} className="close-btn">×</button>
                    </div>
                )}

                {/* Upload Step */}
                {step === 'upload' && (
                    <div className="step-content">
                        <FileUploader
                            onFilesSelected={handleFilesSelected}
                            disabled={uploading}
                        />
                        <div className="step-actions">
                            <button
                                onClick={handleUpload}
                                disabled={files.length === 0 || uploading}
                                className="btn btn-primary"
                            >
                                {uploading ? 'Uploading...' : `Upload ${files.length} File(s)`}
                            </button>
                        </div>
                    </div>
                )}

                {/* Configuration Step */}
                {step === 'configure' && (
                    <div className="step-content">
                        <div className="config-panel">
                            <h2>Extraction Configuration</h2>
                            <p className="upload-success">
                                ✓ Successfully uploaded {uploadedFileIds.length} file(s)
                            </p>

                            <div className="config-option">
                                <label htmlFor="documentType">Document Type:</label>
                                <select
                                    id="documentType"
                                    value={documentType}
                                    onChange={(e) => setDocumentType(e.target.value)}
                                >
                                    <option value="unknown">Auto-detect</option>
                                    <option value="invoice">Invoice</option>
                                    <option value="utility_bill">Utility Bill</option>
                                </select>
                                <p className="hint">
                                    Select the type of documents you're uploading, or let the system auto-detect.
                                </p>
                            </div>

                            <div className="config-option">
                                <label className="checkbox-label">
                                    <input
                                        type="checkbox"
                                        checked={consolidate}
                                        onChange={(e) => setConsolidate(e.target.checked)}
                                    />
                                    <span>Consolidate results into single Excel file</span>
                                </label>
                                <p className="hint">
                                    Combine all extracted data into one spreadsheet for easy analysis.
                                </p>
                            </div>
                        </div>

                        <div className="step-actions">
                            <button onClick={handleReset} className="btn btn-secondary">
                                Back
                            </button>
                            <button onClick={handleStartExtraction} className="btn btn-primary">
                                Start Extraction
                            </button>
                        </div>
                    </div>
                )}

                {/* Processing Step */}
                {step === 'processing' && jobId && (
                    <div className="step-content">
                        <ProcessingStatus
                            jobId={jobId}
                            onComplete={handleComplete}
                            onError={handleError}
                        />
                    </div>
                )}

                {/* Results Step */}
                {step === 'results' && jobId && (
                    <div className="step-content">
                        <ResultsViewer jobId={jobId} />
                        <div className="step-actions">
                            <button onClick={handleReset} className="btn btn-primary">
                                Process More Files
                            </button>
                        </div>
                    </div>
                )}
            </main>

            <footer className="app-footer">
                <p>Built with AI-powered extraction technology</p>
            </footer>
        </div>
    );
}

export default App;
