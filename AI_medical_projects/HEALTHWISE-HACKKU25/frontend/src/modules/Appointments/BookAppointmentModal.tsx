import React, { useState, useEffect } from 'react';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from '../../components/ui/dialog';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '../../components/ui/select';
import { Appointment } from './useAppointments';
import { format } from 'date-fns';

interface BookAppointmentModalProps {
    isOpen: boolean;
    onClose: () => void;
    onBook: (appointment: Omit<Appointment, 'id'>) => void;
    selectedDate?: Date;
}

export const BookAppointmentModal: React.FC<BookAppointmentModalProps> = ({
    isOpen,
    onClose,
    onBook,
    selectedDate,
}) => {
    const [formData, setFormData] = useState({
        patientName: '',
        doctorName: '',
        time: '09:00',
        type: 'Check-up',
    });

    useEffect(() => {
        if (!isOpen) {
            setFormData({
                patientName: '',
                doctorName: '',
                time: '09:00',
                type: 'Check-up',
            });
        }
    }, [isOpen]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onBook({
            patientName: formData.patientName,
            doctorName: formData.doctorName,
            date: selectedDate || new Date(),
            time: formData.time,
            type: formData.type as any,
            status: 'Scheduled',
        });
        onClose();
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Book Appointment</DialogTitle>
                    <p className="text-sm text-muted-foreground">
                        {selectedDate
                            ? `Scheduling for ${format(selectedDate, 'PPP')}`
                            : 'Select a date from the calendar first'}
                    </p>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="patientName" className="text-right">
                            Patient
                        </Label>
                        <Input
                            id="patientName"
                            value={formData.patientName}
                            onChange={(e) =>
                                setFormData({ ...formData, patientName: e.target.value })
                            }
                            className="col-span-3"
                            placeholder="Enter patient name"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="doctorName" className="text-right">
                            Doctor
                        </Label>
                        <Input
                            id="doctorName"
                            value={formData.doctorName}
                            onChange={(e) =>
                                setFormData({ ...formData, doctorName: e.target.value })
                            }
                            className="col-span-3"
                            placeholder="Dr. Name"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="time" className="text-right">
                            Time
                        </Label>
                        <Input
                            id="time"
                            type="time"
                            value={formData.time}
                            onChange={(e) =>
                                setFormData({ ...formData, time: e.target.value })
                            }
                            className="col-span-3"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="type" className="text-right">
                            Type
                        </Label>
                        <Select
                            value={formData.type}
                            onValueChange={(value) =>
                                setFormData({ ...formData, type: value })
                            }
                        >
                            <SelectTrigger className="col-span-3">
                                <SelectValue placeholder="Select type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="Check-up">Check-up</SelectItem>
                                <SelectItem value="Consultation">Consultation</SelectItem>
                                <SelectItem value="Follow-up">Follow-up</SelectItem>
                                <SelectItem value="Emergency">Emergency</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <DialogFooter>
                        <Button type="submit">Confirm Booking</Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
};
