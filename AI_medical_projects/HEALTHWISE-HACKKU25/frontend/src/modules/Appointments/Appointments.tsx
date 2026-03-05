import React, { useState } from 'react';
import { useAppointments } from './useAppointments';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "../../components/ui/table";
import { Button } from "../../components/ui/button";
import { Calendar } from "../../components/ui/calendar";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import { Plus, Calendar as CalendarIcon, Clock, User } from 'lucide-react';
import { BookAppointmentModal } from './BookAppointmentModal';

export const Appointments = () => {
    const { appointments, selectedDate, setSelectedDate, addAppointment } =
        useAppointments();
    const [isBookModalOpen, setIsBookModalOpen] = useState(false);

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Appointments</h2>
                    <p className="text-muted-foreground">
                        Manage your schedule and consultations.
                    </p>
                </div>
                <Button onClick={() => setIsBookModalOpen(true)}>
                    <Plus className="mr-2 h-4 w-4" /> Book Appointment
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-1">
                    <Card>
                        <CardHeader>
                            <CardTitle>Calendar</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <Calendar
                                mode="single"
                                selected={selectedDate}
                                onSelect={setSelectedDate}
                                className="rounded-md border"
                            />
                        </CardContent>
                    </Card>
                </div>

                <div className="md:col-span-2">
                    <Card className="h-full">
                        <CardHeader>
                            <CardTitle>
                                {selectedDate
                                    ? `Appointments for ${selectedDate.toDateString()}`
                                    : 'All Upcoming Appointments'}
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Time</TableHead>
                                        <TableHead>Patient</TableHead>
                                        <TableHead>Doctor</TableHead>
                                        <TableHead>Type</TableHead>
                                        <TableHead>Status</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {appointments.length === 0 ? (
                                        <TableRow>
                                            <TableCell colSpan={5} className="text-center py-8">
                                                No appointments for this date.
                                            </TableCell>
                                        </TableRow>
                                    ) : (
                                        appointments.map((apt) => (
                                            <TableRow key={apt.id} className="hover:bg-muted/50">
                                                <TableCell className="font-medium flex items-center gap-2">
                                                    <Clock className="h-4 w-4 text-muted-foreground" />
                                                    {apt.time}
                                                </TableCell>
                                                <TableCell>
                                                    <div className="flex items-center gap-2">
                                                        <User className="h-4 w-4 text-muted-foreground" />
                                                        {apt.patientName}
                                                    </div>
                                                </TableCell>
                                                <TableCell>{apt.doctorName}</TableCell>
                                                <TableCell>{apt.type}</TableCell>
                                                <TableCell>
                                                    <span
                                                        className={`px-2 py-1 rounded-full text-xs font-medium ${apt.status === 'Scheduled'
                                                            ? 'bg-blue-100 text-blue-700'
                                                            : apt.status === 'Completed'
                                                                ? 'bg-green-100 text-green-700'
                                                                : 'bg-red-100 text-red-700'
                                                            }`}
                                                    >
                                                        {apt.status}
                                                    </span>
                                                </TableCell>
                                            </TableRow>
                                        ))
                                    )}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                </div>
            </div>

            <BookAppointmentModal
                isOpen={isBookModalOpen}
                onClose={() => setIsBookModalOpen(false)}
                onBook={addAppointment}
                selectedDate={selectedDate}
            />
        </div>
    );
};
