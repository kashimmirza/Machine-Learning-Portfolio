import React, { useRef, useEffect, useState } from 'react';
import { Button } from '../../components/ui/button';
import { Loader2, Scan, Maximize2, Camera, RefreshCw, Upload, Image as ImageIcon, Volume2, Move, Lightbulb, Focus } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { toast } from 'sonner';

interface ScannerInterfaceProps {
    onScanComplete: (type: string) => void;
    isScanning: boolean;
    scanType: string;
    isAudioPlaying?: boolean;
}

export const ScannerInterface: React.FC<ScannerInterfaceProps> = ({ onScanComplete, isScanning, scanType, isAudioPlaying }) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [stream, setStream] = useState<MediaStream | null>(null);
    const [progress, setProgress] = useState(0);
    const [isDemoMode, setIsDemoMode] = useState(false);
    const [uploadedImage, setUploadedImage] = useState<string | null>(null);

    // Quality & Guidance State
    const [guidanceText, setGuidanceText] = useState("Initializing sensor...");
    const [qualityMetric, setQualityMetric] = useState(0); // 0-100
    const [isAligned, setIsAligned] = useState(false);

    useEffect(() => {
        if (!isDemoMode && !uploadedImage) {
            startCamera();
        } else {
            stopCamera();
        }
        return () => stopCamera();
    }, [isDemoMode, uploadedImage]);

    // Guidance Logic Loop
    useEffect(() => {
        if (!isScanning && !uploadedImage && !isDemoMode) {
            // Passive guidance when just looking at camera
            const instructions = getInstructionsForType(scanType);
            let i = 0;
            const interval = setInterval(() => {
                // Simulate fluctuating quality metrics (Focus, Light, Stability)
                setQualityMetric(Math.floor(Math.random() * (100 - 80) + 80)); // Random 80-100%
                setGuidanceText(instructions[i % instructions.length]);
                i++;

                // Simulate "Alignment" achieved occasionally
                setIsAligned(Math.random() > 0.3);
            }, 3000);
            return () => clearInterval(interval);
        } else if (isScanning) {
            setGuidanceText("Capturing high-resolution frames...");
            setQualityMetric(100);
            setIsAligned(true);
        }
    }, [scanType, isScanning, uploadedImage, isDemoMode]);

    useEffect(() => {
        if (isScanning) {
            setProgress(0);
            const interval = setInterval(() => {
                setProgress(prev => {
                    if (prev >= 100) {
                        clearInterval(interval);
                        onScanComplete(scanType);
                        return 100;
                    }
                    return prev + 1;
                });
            }, 50);
            return () => clearInterval(interval);
        } else {
            setProgress(0);
        }
    }, [isScanning, scanType]);

    const getInstructionsForType = (type: string) => {
        switch (type) {
            case 'eyes': return ["Position eyes within the box", "Remove glasses if possible", "Look straight ahead", "Hold steady for focus"];
            case 'skin': return ["Center the lesion", "Ensure even lighting", "Move closer to visible area", "Hold device steady"];
            case 'throat': return ["Open mouth wide", "Say 'Ahhh' to lower tongue", "Face a light source", "Keep camera steady"];
            case 'nails': return ["Place fingers flat", "Spread fingers slightly", "Avoid glare on nails", "Hold steady"];
            default: return ["Align target"];
        }
    };

    const startCamera = async () => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
            setStream(mediaStream);
            if (videoRef.current) {
                videoRef.current.srcObject = mediaStream;
            }
        } catch (err) {
            console.error("Error accessing camera:", err);
            toast.error("Camera access denied. Please check permissions.");
        }
    };

    const stopCamera = () => {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            setStream(null);
        }
    };

    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setUploadedImage(reader.result as string);
                setIsDemoMode(false);
                toast.success("Image uploaded successfully");
                setGuidanceText("Image loaded. Ready to analyze.");
                setQualityMetric(100);
                setIsAligned(true);
            };
            reader.readAsDataURL(file);
        }
    };

    const clearUpload = () => {
        setUploadedImage(null);
        if (fileInputRef.current) fileInputRef.current.value = '';
    };

    const getActiveImage = () => {
        if (uploadedImage) return uploadedImage;
        if (isDemoMode) {
            switch (scanType) {
                case 'eyes': return '/demo/retina_scan.png';
                case 'skin': return '/demo/skin_scan.png';
                case 'throat': return '/demo/throat_scan.png';
                case 'nails': return '/demo/nail_scan.png';
                default: return '';
            }
        }
        return null;
    };

    return (
        <Card className={`relative w-full h-[600px] overflow-hidden bg-black rounded-xl border-t-4 shadow-2xl group transition-all duration-300 ${isAudioPlaying ? 'border-t-red-500 shadow-red-500/20' : isScanning ? 'border-t-cyan-500 shadow-cyan-500/50' : 'border-t-slate-500'}`}>

            {/* Video Feed / Image */}
            <div className={`relative w-full h-full ${isAudioPlaying ? 'scale-105 transition-transform duration-[2000ms]' : 'scale-100'}`}>
                {getActiveImage() ? (
                    <img
                        src={getActiveImage()!}
                        alt="Scan Target"
                        className="w-full h-full object-cover opacity-80 animate-in fade-in duration-700"
                    />
                ) : (
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className="w-full h-full object-cover opacity-80"
                    />
                )}

                {/* Dynamic Bounding Box / Reticle */}
                {!uploadedImage && !isDemoMode && (
                    <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 transition-all duration-500 
                   ${isScanning ? 'w-full h-full border-4 border-cyan-500/50 rounded-none' : 'w-64 h-64 border-2 rounded-lg'}
                   ${isAligned ? 'border-green-500 shadow-[0_0_20px_rgba(34,197,94,0.3)]' : 'border-white/50'}
               `}>
                        {/* Corner markers */}
                        {!isScanning && (
                            <>
                                <div className={`absolute top-0 left-0 w-6 h-6 border-t-4 border-l-4 transition-colors ${isAligned ? 'border-green-500' : 'border-white'}`}></div>
                                <div className={`absolute top-0 right-0 w-6 h-6 border-t-4 border-r-4 transition-colors ${isAligned ? 'border-green-500' : 'border-white'}`}></div>
                                <div className={`absolute bottom-0 left-0 w-6 h-6 border-b-4 border-l-4 transition-colors ${isAligned ? 'border-green-500' : 'border-white'}`}></div>
                                <div className={`absolute bottom-0 right-0 w-6 h-6 border-b-4 border-r-4 transition-colors ${isAligned ? 'border-green-500' : 'border-white'}`}></div>
                            </>
                        )}

                        {/* Scanning Beam */}
                        {(isScanning || isAudioPlaying) && (
                            <div className={`w-full h-2 shadow-[0_0_20px_rgba(34,211,238,0.8)] animate-[scan-y_2s_ease-in-out_infinite] absolute top-0 ${isAudioPlaying ? 'bg-red-500' : 'bg-cyan-400'}`}></div>
                        )}
                    </div>
                )}
            </div>

            {/* Hidden File Input */}
            <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                accept="image/*"
                onChange={handleFileUpload}
            />

            {/* Overlay UI Layer */}
            <div className="absolute inset-0 pointer-events-none p-6 flex flex-col justify-between">

                {/* Top Bar */}
                <div className="flex justify-between items-start pointer-events-auto">
                    <div className="space-y-2">
                        <div className={`backdrop-blur-md p-3 rounded-lg border flex items-center gap-3 transition-colors ${isAligned ? 'bg-green-900/30 border-green-500/50' : 'bg-black/50 border-white/20'}`}>
                            <div className={`p-1.5 rounded-full ${isAligned ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'}`}>
                                <Camera className="h-4 w-4 text-white" />
                            </div>
                            <div>
                                <p className="text-xs text-white/70 font-mono tracking-wider">GUIDANCE SYSTEM</p>
                                <p className="text-white font-bold text-sm shadow-black drop-shadow-md">
                                    {guidanceText}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-2 text-cyan-500 bg-black/40 backdrop-blur rounded-lg p-1">
                        {uploadedImage && (
                            <Button variant="ghost" size="icon" onClick={clearUpload} title="Clear Upload" className="text-red-400 hover:text-red-300">
                                <RefreshCw className="h-5 w-5" />
                            </Button>
                        )}
                        <Button variant="ghost" size="icon" onClick={() => fileInputRef.current?.click()} title="Upload Image">
                            <Upload className="h-5 w-5" />
                        </Button>
                        <Button variant="ghost" size="icon" onClick={() => { setIsDemoMode(!isDemoMode); setUploadedImage(null); }} title="Toggle Demo">
                            {isDemoMode ? <Camera className="h-5 w-5" /> : <Scan className="h-5 w-5" />}
                        </Button>
                    </div>
                </div>

                {/* Bottom Status Bar */}
                <div className="space-y-3 pointer-events-auto">
                    {/* Quality Indicators */}
                    {!isDemoMode && !uploadedImage && (
                        <div className="flex gap-4 justify-center mb-4">
                            <div className={`flex items-center gap-2 px-3 py-1 rounded-full backdrop-blur-sm border ${qualityMetric > 90 ? 'bg-green-500/20 border-green-500 text-green-400' : 'bg-yellow-500/20 border-yellow-500 text-yellow-400'}`}>
                                <Focus className="h-3 w-3" />
                                <span className="text-xs font-bold">FOCUS: {qualityMetric}%</span>
                            </div>
                            <div className="flex items-center gap-2 px-3 py-1 rounded-full backdrop-blur-sm border bg-blue-500/20 border-blue-500 text-blue-400">
                                <Lightbulb className="h-3 w-3" />
                                <span className="text-xs font-bold">LIGHT: OK</span>
                            </div>
                            <div className="flex items-center gap-2 px-3 py-1 rounded-full backdrop-blur-sm border bg-purple-500/20 border-purple-500 text-purple-400">
                                <Move className="h-3 w-3" />
                                <span className="text-xs font-bold">STABILITY: HIGH</span>
                            </div>
                        </div>
                    )}

                    {isScanning ? (
                        <div className="bg-black/80 backdrop-blur-lg p-4 rounded-xl border border-cyan-500/50 shadow-[0_0_30px_rgba(6,182,212,0.3)]">
                            <div className="flex justify-between text-xs text-cyan-300 font-mono mb-2">
                                <div className="flex items-center gap-2">
                                    <span className="relative flex h-2 w-2">
                                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                                        <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
                                    </span>
                                    <span>AI NEURAL NET PROCESSING...</span>
                                </div>
                                <span>{progress}%</span>
                            </div>
                            <div className="h-3 bg-gray-900 rounded-full overflow-hidden border border-gray-700">
                                <div
                                    className="h-full bg-gradient-to-r from-cyan-600 via-cyan-400 to-white shadow-[0_0_20px_#22d3ee] transition-all duration-100 ease-linear"
                                    style={{ width: `${progress}%` }}
                                />
                            </div>
                        </div>
                    ) : (
                        <div className="text-center">
                            {!isDemoMode && !uploadedImage && (
                                <p className={`text-sm inline-block px-4 py-2 rounded-full backdrop-blur-md border ${isAligned ? 'bg-green-500/20 border-green-500 text-white' : 'bg-red-500/20 border-red-500 text-white animate-pulse'}`}>
                                    {isAligned ? "✓ TARGET LOCKED: READY TO SCAN" : "⚠ ALIGN SUBJECT IN FRAME"}
                                </p>
                            )}
                        </div>
                    )}
                </div>
            </div>

            {/* Grid Overlay */}
            <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(6,182,212,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(6,182,212,0.03)_1px,transparent_1px)] bg-[size:40px_40px]"></div>
        </Card>
    );
};
