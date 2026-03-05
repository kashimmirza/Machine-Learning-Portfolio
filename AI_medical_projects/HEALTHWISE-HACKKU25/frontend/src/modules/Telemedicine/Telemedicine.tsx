import React, { useState } from 'react';
import { Button } from '../../components/ui/button';
import { Card, CardContent } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Mic, MicOff, Video, VideoOff, PhoneOff, MessageSquare, Send } from 'lucide-react';
import { ScribePanel } from './ScribePanel';

export const Telemedicine = () => {
    const [isMuted, setIsMuted] = useState(false);
    const [isVideoOff, setIsVideoOff] = useState(false);
    const [messages, setMessages] = useState<{ sender: 'user' | 'doctor'; text: string }[]>([
        { sender: 'doctor', text: 'Hello! How are you feeling today?' },
    ]);
    const [newMessage, setNewMessage] = useState('');

    const handleSendMessage = (e: React.FormEvent) => {
        e.preventDefault();
        if (!newMessage.trim()) return;
        setMessages([...messages, { sender: 'user', text: newMessage }]);
        setNewMessage('');
        setTimeout(() => {
            setMessages((prev) => [
                ...prev,
                { sender: 'doctor', text: 'I see. Let me check your vitals.' },
            ]);
        }, 1000);
    };

    return (
        <div className="h-[calc(100vh-8rem)] flex flex-col gap-4 animate-in fade-in duration-500">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Telemedicine</h2>
                    <p className="text-muted-foreground">Virtual consultation room.</p>
                </div>
                <div className="flex items-center gap-2">
                    <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-green-500 text-white shadow hover:bg-green-600">Live</span>
                    <span className="text-sm font-medium">Dr. Sarah Chen</span>
                </div>
            </div>

            <div className="flex-1 grid grid-cols-1 md:grid-cols-4 gap-4 min-h-0">
                <div className="md:col-span-2 flex flex-col gap-4">
                    <Card className="flex-1 bg-black/90 relative overflow-hidden flex items-center justify-center">
                        {isVideoOff ? (
                            <div className="text-white flex flex-col items-center">
                                <div className="h-20 w-20 rounded-full bg-gray-700 flex items-center justify-center mb-4">
                                    <VideoOff className="h-8 w-8 text-gray-400" />
                                </div>
                                <p>Camera is off</p>
                            </div>
                        ) : (
                            <div className="text-white text-center">
                                <p className="mb-4 text-lg">Dr. Sarah Chen</p>
                                <div className="h-48 w-48 bg-gray-800 rounded-full mx-auto flex items-center justify-center animate-pulse">
                                    <span className="text-4xl">👨‍⚕️</span>
                                </div>
                            </div>
                        )}

                        {/* Self view */}
                        <div className="absolute bottom-4 right-4 w-32 h-24 bg-gray-800 rounded-lg border border-gray-700 flex items-center justify-center overflow-hidden">
                            <span className="text-xs text-gray-400">You</span>
                        </div>
                    </Card>

                    <div className="flex justify-center gap-4">
                        <Button
                            variant={isMuted ? "destructive" : "secondary"}
                            size="icon"
                            className="rounded-full h-12 w-12"
                            onClick={() => setIsMuted(!isMuted)}
                        >
                            {isMuted ? <MicOff /> : <Mic />}
                        </Button>
                        <Button
                            variant={isVideoOff ? "destructive" : "secondary"}
                            size="icon"
                            className="rounded-full h-12 w-12"
                            onClick={() => setIsVideoOff(!isVideoOff)}
                        >
                            {isVideoOff ? <VideoOff /> : <Video />}
                        </Button>
                        <Button
                            variant="destructive"
                            size="icon"
                            className="rounded-full h-12 w-12"
                        >
                            <PhoneOff />
                        </Button>
                    </div>
                </div>

                <div className="md:col-span-1 flex flex-col min-h-0">
                    <ScribePanel patientName="Active Patient" />
                </div>

                <Card className="md:col-span-1 flex flex-col min-h-0">
                    <CardContent className="flex-1 flex flex-col p-4 h-full">
                        <div className="flex items-center gap-2 mb-4 pb-4 border-b">
                            <MessageSquare className="h-4 w-4" />
                            <h3 className="font-semibold">Chat</h3>
                        </div>

                        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                            {messages.map((msg, i) => (
                                <div
                                    key={i}
                                    className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'
                                        }`}
                                >
                                    <div
                                        className={`max-w-[80%] rounded-lg px-4 py-2 text-sm ${msg.sender === 'user'
                                            ? 'bg-primary text-primary-foreground'
                                            : 'bg-muted'
                                            }`}
                                    >
                                        {msg.text}
                                    </div>
                                </div>
                            ))}
                        </div>

                        <form onSubmit={handleSendMessage} className="flex gap-2">
                            <Input
                                value={newMessage}
                                onChange={(e) => setNewMessage(e.target.value)}
                                placeholder="Type a message..."
                            />
                            <Button type="submit" size="icon">
                                <Send className="h-4 w-4" />
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};
