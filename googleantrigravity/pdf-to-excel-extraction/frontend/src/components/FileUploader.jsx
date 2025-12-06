/**
 * File uploader component with drag-and-drop support
 */

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

const FileUploader = ({ onFilesSelected, disabled }) => {
    const [selectedFiles, setSelectedFiles] = useState([]);

    const onDrop = useCallback((acceptedFiles) => {
        const pdfFiles = acceptedFiles.filter(file =>
            file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
        );

        setSelectedFiles(prev => [...prev, ...pdfFiles]);

        if (onFilesSelected) {
            onFilesSelected([...selectedFiles, ...pdfFiles]);
        }
    }, [selectedFiles, onFilesSelected]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf']
        },
        disabled,
        multiple: true,
    });

    const removeFile = (index) => {
        const newFiles = selectedFiles.filter((_, i) => i !== index);
        setSelectedFiles(newFiles);
        if (onFilesSelected) {
            onFilesSelected(newFiles);
        }
    };

    const clearAll = () => {
        setSelectedFiles([]);
        if (onFilesSelected) {
            onFilesSelected([]);
        }
    };

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    };

    return (
        <div className="file-uploader">
            <div
                {...getRootProps()}
                className={`dropzone ${isDragActive ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
            >
                <input {...getInputProps()} />
                <div className="dropzone-content">
                    <svg
                        className="upload-icon"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                        />
                    </svg>
                    {isDragActive ? (
                        <p className="dropzone-text">Drop the PDF files here...</p>
                    ) : (
                        <div>
                            <p className="dropzone-text">
                                Drag & drop PDF files here, or click to select files
                            </p>
                            <p className="dropzone-hint">
                                Supports invoices, utility bills, and other PDF documents
                            </p>
                        </div>
                    )}
                </div>
            </div>

            {selectedFiles.length > 0 && (
                <div className="file-list">
                    <div className="file-list-header">
                        <h3>Selected Files ({selectedFiles.length})</h3>
                        <button onClick={clearAll} className="btn-link">
                            Clear All
                        </button>
                    </div>

                    <div className="file-items">
                        {selectedFiles.map((file, index) => (
                            <div key={index} className="file-item">
                                <div className="file-icon">
                                    <svg fill="currentColor" viewBox="0 0 20 20">
                                        <path
                                            fillRule="evenodd"
                                            d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                </div>
                                <div className="file-info">
                                    <div className="file-name">{file.name}</div>
                                    <div className="file-size">{formatFileSize(file.size)}</div>
                                </div>
                                <button
                                    onClick={() => removeFile(index)}
                                    className="btn-remove"
                                    aria-label="Remove file"
                                >
                                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth={2}
                                            d="M6 18L18 6M6 6l12 12"
                                        />
                                    </svg>
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default FileUploader;
