import React, { useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { ScrollArea } from '../../components/ui/scroll-area';
import { AlertTriangle, CheckCircle, Pill, FileText, Download, PlayCircle, StopCircle, UserCheck } from 'lucide-react';
import { toast } from 'sonner';

interface AnalysisReportProps {
    results: Array<{
        part: string;
        condition: string;
        risk: 'High' | 'Medium' | 'Low';
        confidence: number;
        details: string;
        doctorAnalysis?: string;
        preventiveMeasures?: string[];
    }>;
    prescriptions: Array<{
        name: string;
        dosage: string;
        reason: string;
    }>;
    onAudioToggle: (isPlaying: boolean) => void;
    isExternalPlaying: boolean;
}

export const AnalysisReport: React.FC<AnalysisReportProps> = ({ results, prescriptions, onAudioToggle, isExternalPlaying }) => {
    const synth = window.speechSynthesis;

    useEffect(() => {
        // Cleanup audio on unmount
        return () => {
            if (synth.speaking) synth.cancel();
        };
    }, []);

    const handlePlayAudio = (text: string) => {
        if (isExternalPlaying) {
            synth.cancel();
            onAudioToggle(false);
            return;
        }

        if (text) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9; // Slightly slower, more authoritative
            utterance.pitch = 1.0;
            utterance.onend = () => onAudioToggle(false);
            synth.speak(utterance);
            onAudioToggle(true);
        }
    };

    const handleDownloadReport = () => {
        toast.success("Downloading Comprehensive PDF Report...");
        // Mock download - in real app, this would trigger a PDF generation
    };

    return (
        <div className="space-y-4 animate-in slide-in-from-right duration-500">

            {/* Findings Report */}
            <Card className={`border-t-4 border-t-amber-500 shadow-md transition-shadow ${isExternalPlaying ? 'shadow-red-500/20 ring-1 ring-red-500/50' : ''}`}>
                <CardHeader className="pb-2 bg-slate-50/50 dark:bg-slate-900/20">
                    <CardTitle className="text-lg flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <FileText className="h-5 w-5 text-amber-500" />
                            Diagnostic Report
                        </div>
                        {results.length > 0 && (
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handlePlayAudio(`Here is your diagnosis for ${results[0].part}. ${results[0].doctorAnalysis}`)}
                                className={`${isExternalPlaying ? 'text-red-500 animate-pulse' : 'text-blue-500'}`}
                            >
                                {isExternalPlaying ? <StopCircle className="h-5 w-5 mr-1" /> : <PlayCircle className="h-5 w-5 mr-1" />}
                                {isExternalPlaying ? 'Stop Audio' : 'Doctor Audio'}
                            </Button>
                        )}
                    </CardTitle>
                </CardHeader>
                <CardContent className="pt-4">
                    <ScrollArea className="h-[300px] w-full pr-4">
                        <div className="space-y-6">
                            {results.length === 0 && <p className="text-muted-foreground text-sm text-center py-8">No analysis data yet. Complete a scan.</p>}
                            {results.map((res, i) => (
                                <div key={i} className="space-y-3">
                                    {/* Header Status */}
                                    <div className="flex justify-between items-center border-b pb-2">
                                        <span className="font-bold text-sm uppercase text-slate-500">{res.part} Analysis</span>
                                        <span className={`text-xs px-3 py-1 rounded-full font-bold border ${res.risk === 'High' ? 'bg-red-50 text-red-600 border-red-200' :
                                                res.risk === 'Medium' ? 'bg-yellow-50 text-yellow-600 border-yellow-200' :
                                                    'bg-green-50 text-green-600 border-green-200'
                                            }`}>
                                            {res.risk} RISK ({res.confidence}%)
                                        </span>
                                    </div>

                                    {/* Condition */}
                                    <div>
                                        <h4 className="font-bold text-lg text-primary">{res.condition}</h4>
                                        <p className="text-sm text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">
                                            {res.details}
                                        </p>
                                    </div>

                                    {/* Expert Analysis */}
                                    {res.doctorAnalysis && (
                                        <div className={`bg-blue-50 dark:bg-blue-900/20 p-3 rounded-md border border-blue-100 dark:border-blue-800 transition-colors ${isExternalPlaying ? 'border-l-4 border-l-red-500 bg-red-50 dark:bg-red-900/10' : ''}`}>
                                            <div className="flex items-center gap-2 mb-1 text-blue-700 dark:text-blue-400 font-semibold text-xs uppercase tracking-wide">
                                                <UserCheck className="h-4 w-4" />
                                                Expert Analysis (Dr. AI - 20 Yrs Exp)
                                            </div>
                                            <p className="text-sm italic text-slate-700 dark:text-slate-300">
                                                "{res.doctorAnalysis}"
                                            </p>
                                        </div>
                                    )}

                                    {/* Preventive Measures */}
                                    {res.preventiveMeasures && res.preventiveMeasures.length > 0 && (
                                        <div className="space-y-1">
                                            <span className="text-xs font-bold uppercase text-slate-500">Recommended Actions:</span>
                                            <ul className="text-sm list-disc pl-5 space-y-1 text-slate-600 dark:text-slate-400">
                                                {res.preventiveMeasures.map((pm, idx) => (
                                                    <li key={idx}>{pm}</li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </ScrollArea>
                </CardContent>
                {results.length > 0 && (
                    <CardFooter className="bg-slate-50 dark:bg-slate-900/50 p-2 border-t">
                        <Button className="w-full" variant="outline" size="sm" onClick={handleDownloadReport}>
                            <Download className="mr-2 h-4 w-4" /> Download Detailed PDF Report
                        </Button>
                    </CardFooter>
                )}
            </Card>

            {/* AI Prescriptions */}
            <Card className="border-t-4 border-t-emerald-500 shadow-md">
                <CardHeader className="pb-2">
                    <CardTitle className="text-lg flex items-center gap-2">
                        <Pill className="h-5 w-5 text-emerald-500" />
                        Prescription & Dosage
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {prescriptions.length === 0 && <p className="text-muted-foreground text-sm text-center">No prescriptions required.</p>}
                        {prescriptions.map((rx, i) => (
                            <div key={i} className="flex gap-3 p-3 rounded-lg bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900 shadow-sm transition-all hover:shadow-md">
                                <div className="h-10 w-10 rounded-full bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center flex-shrink-0 border border-emerald-200">
                                    <span className="text-sm font-bold text-emerald-700 dark:text-emerald-400">Rx</span>
                                </div>
                                <div>
                                    <p className="font-bold text-base text-slate-800 dark:text-slate-200">{rx.name}</p>
                                    <div className="flex items-center gap-2 mt-1">
                                        <span className="px-2 py-0.5 rounded text-[10px] bg-slate-200 dark:bg-slate-800 font-mono">{rx.dosage}</span>
                                    </div>
                                    <p className="text-xs text-muted-foreground mt-2 italic">
                                        Reason: {rx.reason}
                                    </p>
                                </div>
                            </div>
                        ))}

                        {prescriptions.length > 0 && (
                            <Button className="w-full mt-2 bg-emerald-600 hover:bg-emerald-700 text-white" size="sm">
                                Print Prescription
                            </Button>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};
