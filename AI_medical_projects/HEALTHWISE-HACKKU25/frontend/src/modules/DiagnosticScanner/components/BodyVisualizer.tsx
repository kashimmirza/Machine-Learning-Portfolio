import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';

interface BodyVisualizerProps {
    scannedParts: string[];
    activePart?: string;
    isAnimating?: boolean;
}

export const BodyVisualizer: React.FC<BodyVisualizerProps> = ({ scannedParts, activePart, isAnimating }) => {
    const getFill = (part: string) => {
        // If expanding this part and it's the active one, make it pulse or highlight brighter
        if (isAnimating && activePart && part.toLowerCase() === activePart.toLowerCase()) return "#22d3ee";
        return scannedParts.includes(part) ? "#0e7490" : "#334155"; // Darker cyan for scanned, Slate for unscanned
    };

    const isTargeted = (part: string) => isAnimating && activePart && part.toLowerCase() === activePart.toLowerCase();

    return (
        <Card className="h-full bg-slate-900 border-none shadow-inner relative overflow-hidden">
            <CardHeader className="pb-2 relative z-10">
                <CardTitle className="text-sm text-cyan-400 uppercase tracking-widest text-center flex items-center justify-center gap-2">
                    Biometric Map
                    {isAnimating && <span className="flex h-2 w-2 rounded-full bg-red-500 animate-ping" />}
                </CardTitle>
            </CardHeader>
            <CardContent className="flex items-center justify-center p-6 relative z-10">
                <svg
                    viewBox="0 0 200 400"
                    className="h-full max-h-[400px] w-auto drop-shadow-[0_0_15px_rgba(6,182,212,0.1)]"
                    fill="none"
                    stroke="currentColor"
                >
                    {/* Abstract Body Shape */}

                    {/* Head */}
                    <g className={isTargeted('Eyes') || isTargeted('Tongue') || isTargeted('Throat') ? "animate-pulse" : ""}>
                        <circle cx="100" cy="50" r="30" stroke="#475569" strokeWidth="2" fill={getFill('Head') || getFill('Eyes')} className="transition-all duration-500" />
                        {/* Target Reticle for Head Area */}
                        {(isTargeted('Eyes') || isTargeted('Tongue') || isTargeted('Throat')) && (
                            <>
                                <circle cx="100" cy="50" r="40" stroke="#ef4444" strokeWidth="1" strokeDasharray="4 4" className="animate-[spin_3s_linear_infinite]" />
                                <circle cx="100" cy="50" r="35" stroke="#ef4444" strokeWidth="0.5" className="animate-ping opacity-50" />
                            </>
                        )}
                    </g>

                    {/* Neck */}
                    <rect x="90" y="80" width="20" height="20" stroke="#475569" strokeWidth="2" fill="#334155" />

                    {/* Torso - Skin/General */}
                    <g>
                        <path d="M70,100 Q100,100 130,100 L120,220 Q100,220 80,220 Z" stroke="#475569" strokeWidth="2" fill={getFill('Skin')} />
                        {isTargeted('Skin') && (
                            <>
                                <rect x="60" y="90" width="80" height="140" rx="10" stroke="#ef4444" strokeWidth="1" strokeDasharray="4 4" className="animate-pulse" fill="transparent" />
                                <line x1="100" y1="100" x2="100" y2="220" stroke="#ef4444" strokeWidth="0.5" className="animate-[scan-y_1s_ease-in-out_infinite]" />
                            </>
                        )}
                    </g>

                    {/* Arms - Nails */}
                    <path d="M70,100 L40,180" stroke="#475569" strokeWidth="2" />
                    <path d="M130,100 L160,180" stroke="#475569" strokeWidth="2" />
                    {isTargeted('Nails') && (
                        <>
                            <circle cx="40" cy="180" r="10" stroke="#ef4444" strokeWidth="1" className="animate-ping" />
                            <circle cx="160" cy="180" r="10" stroke="#ef4444" strokeWidth="1" className="animate-ping delay-100" />
                        </>
                    )}

                    {/* Legs */}
                    <path d="M80,220 L70,350" stroke="#475569" strokeWidth="2" />
                    <path d="M120,220 L130,350" stroke="#475569" strokeWidth="2" />

                    {/* Pointers/Segment Lines */}
                    {scannedParts.includes('Eyes') && (
                        <line x1="100" y1="50" x2="160" y2="30" stroke={isTargeted('Eyes') ? "#ef4444" : "#22d3ee"} strokeWidth={isTargeted('Eyes') ? "2" : "1"} />
                    )}
                    {scannedParts.includes('Skin') && (
                        <line x1="55" y1="140" x2="20" y2="120" stroke={isTargeted('Skin') ? "#ef4444" : "#22d3ee"} strokeWidth={isTargeted('Skin') ? "2" : "1"} />
                    )}

                </svg>
            </CardContent>

            {/* Scanning Grid Background when active */}
            {isAnimating && (
                <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(239,68,68,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(239,68,68,0.05)_1px,transparent_1px)] bg-[size:20px_20px] animate-in fade-in"></div>
            )}
        </Card>
    );
};
