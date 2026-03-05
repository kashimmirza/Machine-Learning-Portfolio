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
import { Textarea } from '../../components/ui/textarea';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '../../components/ui/select';
import { MedicalRecord } from './useMedicalRecords';

interface AddRecordModalProps {
    isOpen: boolean;
    onClose: () => void;
    onAdd: (record: Omit<MedicalRecord, 'id'>) => void;
}

export const AddRecordModal: React.FC<AddRecordModalProps> = ({
    isOpen,
    onClose,
    onAdd,
}) => {
    const [formData, setFormData] = useState({
        title: '',
        type: 'Diagnosis',
        description: '',
        doctorName: '',
        date: new Date().toISOString().split('T')[0],
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onAdd({
            title: formData.title,
            type: formData.type as any,
            description: formData.description,
            doctorName: formData.doctorName,
            date: formData.date,
        });
        onClose();
        setFormData({
            title: '',
            type: 'Diagnosis',
            description: '',
            doctorName: '',
            date: new Date().toISOString().split('T')[0],
        });
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Add Medical Record</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="title" className="text-right">
                            Title
                        </Label>
                        <Input
                            id="title"
                            value={formData.title}
                            onChange={(e) =>
                                setFormData({ ...formData, title: e.target.value })
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
                                <SelectItem value="Diagnosis">Diagnosis</SelectItem>
                                <SelectItem value="Lab Result">Lab Result</SelectItem>
                                <SelectItem value="Procedure">Procedure</SelectItem>
                                <SelectItem value="Vaccination">Vaccination</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="date" className="text-right">
                            Date
                        </Label>
                        <Input
                            id="date"
                            type="date"
                            value={formData.date}
                            onChange={(e) =>
                                setFormData({ ...formData, date: e.target.value })
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
                        <Label htmlFor="description" className="text-right">
                            Description
                        </Label>
                        <Textarea
                            id="description"
                            value={formData.description}
                            onChange={(e) =>
                                setFormData({ ...formData, description: e.target.value })
                            }
                            className="col-span-3"
                            rows={3}
                        />
                    </div>
                    <DialogFooter>
                        <Button type="submit">Save Record</Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
};
