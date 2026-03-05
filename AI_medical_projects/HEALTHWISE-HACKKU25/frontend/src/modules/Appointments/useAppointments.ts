import { useState, useCallback } from 'react';

export interface Appointment {
    id: string;
    patientName: string;
    doctorName: string;
    date: Date;
    time: string;
    type: 'Check-up' | 'Consultation' | 'Follow-up' | 'Emergency';
    status: 'Scheduled' | 'Completed' | 'Cancelled';
}

const MOCK_APPOINTMENTS: Appointment[] = [
    {
        id: '1',
        patientName: 'John Doe',
        doctorName: 'Dr. Sarah Chen',
        date: new Date(),
        time: '14:00',
        type: 'Check-up',
        status: 'Scheduled',
    },
    {
        id: '2',
        patientName: 'Jane Smith',
        doctorName: 'Dr. Michael Ross',
        date: new Date(new Date().setDate(new Date().getDate() + 1)),
        time: '10:00',
        type: 'Consultation',
        status: 'Scheduled',
    },
];

export function useAppointments() {
    const [appointments, setAppointments] = useState<Appointment[]>(MOCK_APPOINTMENTS);
    const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date());

    const addAppointment = useCallback((appointment: Omit<Appointment, 'id'>) => {
        const newAppointment = {
            ...appointment,
            id: Math.random().toString(36).substr(2, 9),
        };
        setAppointments((prev) => [...prev, newAppointment]);
    }, []);

    const filteredAppointments = appointments.filter((apt) => {
        if (!selectedDate) return true;
        return (
            apt.date.getDate() === selectedDate.getDate() &&
            apt.date.getMonth() === selectedDate.getMonth() &&
            apt.date.getFullYear() === selectedDate.getFullYear()
        );
    });

    return {
        appointments: filteredAppointments,
        allAppointments: appointments,
        selectedDate,
        setSelectedDate,
        addAppointment,
    };
}
