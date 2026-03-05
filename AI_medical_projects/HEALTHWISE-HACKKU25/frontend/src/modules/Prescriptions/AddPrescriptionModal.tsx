import React, { useState } from 'react';
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
import { Prescription } from './usePrescriptions';

interface AddPrescriptionModalProps {
    isOpen: boolean;
    onClose: () => void;
    onAdd: (prescription: Omit<Prescription, 'id'>) => void;
}

export const AddPrescriptionModal: React.FC<AddPrescriptionModalProps> = ({
    isOpen,
    onClose,
    onAdd,
}) => {
    const [formData, setFormData] = useState({
        medication: '',
        dosage: '',
        frequency: '',
        startDate: '',
        endDate: '',
        doctorName: '',
        status: 'Active',
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onAdd({
            medication: formData.medication,
            dosage: formData.dosage,
            frequency: formData.frequency,
            startDate: formData.startDate,
            endDate: formData.endDate,
            doctorName: formData.doctorName,
            status: formData.status as any,
        });
        onClose();
        setFormData({
            medication: '',
            dosage: '',
            frequency: '',
            startDate: '',
            endDate: '',
            doctorName: '',
            status: 'Active',
        });
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Add Prescription</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="medication" className="text-right">
                            Medication
                        </Label>
                        <Input
                            id="medication"
                            value={formData.medication}
                            onChange={(e) =>
                                setFormData({ ...formData, medication: e.target.value })
                            }
                            className="col-span-3"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="dosage" className="text-right">
                            Dosage
                        </Label>
                        <Input
                            id="dosage"
                            value={formData.dosage}
                            onChange={(e) =>
                                setFormData({ ...formData, dosage: e.target.value })
                            }
                            className="col-span-3"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="frequency" className="text-right">
                            Frequency
                        </Label>
                        <Input
                            id="frequency"
                            value={formData.frequency}
                            onChange={(e) =>
                                setFormData({ ...formData, frequency: e.target.value })
                            }
                            className="col-span-3"
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
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="startDate" className="text-right">
                            Start Date
                        </Label>
                        <Input
                            id="startDate"
                            type="date"
                            value={formData.startDate}
                            onChange={(e) =>
                                setFormData({ ...formData, startDate: e.target.value })
                            }
                            className="col-span-3"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="endDate" className="text-right">
                            End Date
                        </Label>
                        <Input
                            id="endDate"
                            type="date"
                            value={formData.endDate}
                            onChange={(e) =>
                                setFormData({ ...formData, endDate: e.target.value })
                            }
                            className="col-span-3"
                            required
                        />
                    </div>
                    <DialogFooter>
                        <Button type="submit">Save Prescription</Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
};
