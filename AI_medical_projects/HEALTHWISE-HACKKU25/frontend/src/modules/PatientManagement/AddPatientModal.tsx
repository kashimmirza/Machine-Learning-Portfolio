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
import { Patient } from './usePatients';

interface AddPatientModalProps {
    isOpen: boolean;
    onClose: () => void;
    onAdd: (patient: Omit<Patient, 'id'>) => void;
}

export const AddPatientModal: React.FC<AddPatientModalProps> = ({
    isOpen,
    onClose,
    onAdd,
}) => {
    const [formData, setFormData] = useState({
        name: '',
        age: '',
        gender: 'Male',
        contact: '',
        status: 'Stable',
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onAdd({
            name: formData.name,
            age: parseInt(formData.age),
            gender: formData.gender,
            contact: formData.contact,
            lastVisit: new Date().toISOString().split('T')[0],
            status: formData.status as any,
        });
        onClose();
        setFormData({
            name: '',
            age: '',
            gender: 'Male',
            contact: '',
            status: 'Stable',
        });
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Add New Patient</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="name" className="text-right">
                            Name
                        </Label>
                        <Input
                            id="name"
                            value={formData.name}
                            onChange={(e) =>
                                setFormData({ ...formData, name: e.target.value })
                            }
                            className="col-span-3"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="age" className="text-right">
                            Age
                        </Label>
                        <Input
                            id="age"
                            type="number"
                            value={formData.age}
                            onChange={(e) =>
                                setFormData({ ...formData, age: e.target.value })
                            }
                            className="col-span-3"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="gender" className="text-right">
                            Gender
                        </Label>
                        <Select
                            value={formData.gender}
                            onValueChange={(value) =>
                                setFormData({ ...formData, gender: value })
                            }
                        >
                            <SelectTrigger className="col-span-3">
                                <SelectValue placeholder="Select gender" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="Male">Male</SelectItem>
                                <SelectItem value="Female">Female</SelectItem>
                                <SelectItem value="Other">Other</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="contact" className="text-right">
                            Contact
                        </Label>
                        <Input
                            id="contact"
                            value={formData.contact}
                            onChange={(e) =>
                                setFormData({ ...formData, contact: e.target.value })
                            }
                            className="col-span-3"
                            required
                        />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="status" className="text-right">
                            Status
                        </Label>
                        <Select
                            value={formData.status}
                            onValueChange={(value) =>
                                setFormData({ ...formData, status: value })
                            }
                        >
                            <SelectTrigger className="col-span-3">
                                <SelectValue placeholder="Select status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="Stable">Stable</SelectItem>
                                <SelectItem value="Recovering">Recovering</SelectItem>
                                <SelectItem value="Critical">Critical</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <DialogFooter>
                        <Button type="submit">Save Patient</Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
};
