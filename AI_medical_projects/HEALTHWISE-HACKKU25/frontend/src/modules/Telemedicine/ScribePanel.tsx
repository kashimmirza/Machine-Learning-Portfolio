import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { ScrollArea } from '../../components/ui/scroll-area';
import { Bot, Save, FileText, Loader2, Play, Square } from 'lucide-react';
import { useMedicalRecords } from '../MedicalRecords/useMedicalRecords';
import { toast } from 'sonner';

interface ScribePanelProps {
    patientName: string;
}

const MOCK_TRANSCRIPT = [
    "Doctor: Good morning, how are you feeling today?",
    "Patient: I've been having this persistent cough for the last 3 days.",
    "Doctor: Is it a dry cough or are you coughing up anything?",
    "Patient: It's mostly dry, but my throat feels very sore.",
    "Doctor: Have you had any fever or chills?",
    "Patient: Yes, I had a mild fever last night, about 38 degrees.",
    "Doctor: Any difficulty breathing or chest pain?",
    "Patient: No chest pain, but I feel a bit short of breath when I walk up stairs.",
    "Doctor: I see. I'm going to prescribe you an inhaler and some antibiotics.",
];

export const ScribePanel: React.FC<ScribePanelProps> = ({ patientName }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [transcription, setTranscription] = useState<string[]>([]);
    const [soapNote, setSoapNote] = useState({
        subjective: '',
        objective: '',
        assessment: '',
        plan: '',
    });
    const [currentLine, setCurrentLine] = useState(0);
    const { addRecord } = useMedicalRecords();
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        let interval: NodeJS.Timeout;

        if (isRecording && currentLine < MOCK_TRANSCRIPT.length) {
            interval = setInterval(() => {
                setTranscription((prev) => [...prev, MOCK_TRANSCRIPT[currentLine]]);

                // Simulate progressive SOAP note generation
                if (currentLine === 1) {
                    setSoapNote(prev => ({ ...prev, subjective: "Patient reports persistent dry cough for 3 days. Sore throat." }));
                }
                if (currentLine === 5) {
                    setSoapNote(prev => ({ ...prev, subjective: prev.subjective + " Mild fever (38C) last night.", objective: "Patient appears flushed." }));
                }
                if (currentLine === 7) {
                    setSoapNote(prev => ({ ...prev, subjective: prev.subjective + " Mild dyspnea on exertion.", assessment: "Likely upper respiratory tract infection or acute bronchitis." }));
                }
                if (currentLine === 8) {
                    setSoapNote(prev => ({ ...prev, plan: "Prescribe inhaler for symptomatic relief. Start course of antibiotics. Follow up in 5 days if no improvement." }));
                }

                setCurrentLine((prev) => prev + 1);

                // Auto-scroll
                if (scrollRef.current) {
                    scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
                }

            }, 2000);
        } else if (currentLine >= MOCK_TRANSCRIPT.length) {
            setIsRecording(false);
        }

        return () => clearInterval(interval);
    }, [isRecording, currentLine]);

    const handleSave = () => {
        const fullNote = `SOAP NOTE\n\nSUBJECTIVE:\n${soapNote.subjective}\n\nOBJECTIVE:\n${soapNote.objective}\n\nASSESSMENT:\n${soapNote.assessment}\n\nPLAN:\n${soapNote.plan}`;

        addRecord({
            date: new Date().toISOString().split('T')[0],
            type: 'Diagnosis', // Or 'Consultation' if available
            title: `Consultation Note - ${patientName}`,
            description: fullNote,
            doctorName: 'Dr. Sarah Chen', // Assuming current user
        });

        toast.success("SOAP Note saved to Medical Records");
    };

    return (
        <div className="flex flex-col h-full gap-4">
            <Card className="flex-1 flex flex-col min-h-0 bg-slate-50 dark:bg-slate-900 border-l-4 border-l-primary">
                <CardHeader className="py-3 px-4 border-b bg-white dark:bg-slate-950 flex flex-row items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Bot className="h-5 w-5 text-primary" />
                        <CardTitle className="text-base">AI Medical Scribe</CardTitle>
                    </div>
                    <Button
                        variant={isRecording ? "destructive" : "default"}
                        size="sm"
                        onClick={() => setIsRecording(!isRecording)}
                        className="w-24"
                    >
                        {isRecording ? (
                            <>
                                <Square className="h-3 w-3 mr-2" /> Stop
                            </>
                        ) : (
                            <>
                                <Play className="h-3 w-3 mr-2" /> Start
                            </>
                        )}
                    </Button>
                </CardHeader>
                <CardContent className="flex-1 p-0 grid grid-rows-2">
                    {/* Real-time Transcription */}
                    <div className="border-b p-4 overflow-hidden flex flex-col">
                        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Live Transcription</p>
                        <ScrollArea className="flex-1" ref={scrollRef}>
                            <div className="space-y-2">
                                {transcription.length === 0 ? (
                                    <p className="text-sm text-muted-foreground italic">
                                        Press Start to begin listening...
                                    </p>
                                ) : (
                                    transcription.map((line, i) => (
                                        <div key={i} className="text-sm">
                                            <span className="font-semibold text-primary">{line.split(':')[0]}:</span>
                                            <span className="text-foreground">{line.split(':')[1]}</span>
                                        </div>
                                    ))
                                )}
                                {isRecording && (
                                    <div className="flex items-center gap-2 text-xs text-primary animate-pulse">
                                        <Loader2 className="h-3 w-3 animate-spin" />
                                        Listening...
                                    </div>
                                )}
                            </div>
                        </ScrollArea>
                    </div>

                    {/* SOAP Note Generation */}
                    <div className="p-4 overflow-hidden flex flex-col bg-white dark:bg-black/20">
                        <div className="flex items-center justify-between mb-2">
                            <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Generated SOAP Note</p>
                            {soapNote.plan && (
                                <Button variant="outline" size="sm" className="h-6 text-xs gap-1" onClick={handleSave}>
                                    <Save className="h-3 w-3" /> Save to Record
                                </Button>
                            )}
                        </div>
                        <ScrollArea className="flex-1">
                            <div className="space-y-3 text-sm">
                                <div>
                                    <span className="font-bold text-blue-600 block text-xs">SUBJECTIVE</span>
                                    <p className="text-muted-foreground">{soapNote.subjective || "..."}</p>
                                </div>
                                <div>
                                    <span className="font-bold text-blue-600 block text-xs">OBJECTIVE</span>
                                    <p className="text-muted-foreground">{soapNote.objective || "..."}</p>
                                </div>
                                <div>
                                    <span className="font-bold text-blue-600 block text-xs">ASSESSMENT</span>
                                    <p className="text-muted-foreground">{soapNote.assessment || "..."}</p>
                                </div>
                                <div>
                                    <span className="font-bold text-blue-600 block text-xs">PLAN</span>
                                    <p className="text-muted-foreground">{soapNote.plan || "..."}</p>
                                </div>
                            </div>
                        </ScrollArea>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};
