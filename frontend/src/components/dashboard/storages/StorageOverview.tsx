"use client"

import {FC, JSX, useState} from "react";
import {useGetMyStoragesQuery} from "@/redux/api/storaSenseApi";
import StorageCard from "@/components/dashboard/storages/StorageCard";
import StorageCreationForm from "@/components/dashboard/storages/StorageCreationForm";
import {Skeleton} from "@/components/ui/skeleton";
import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert";
import {AlertCircleIcon, Plus} from "lucide-react";
import {Button} from "@/components/ui/button";
import {Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle} from "@/components/ui/dialog";


const StorageOverview: FC = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const {data: storages, isLoading, isError, error} = useGetMyStoragesQuery();

    const handleModalClose = () => {
        setIsModalOpen(false);
    };

    if (isLoading) {
        const skeletons: JSX.Element[] = [];
        for (let i=0; i<8; i++) {
            skeletons.push(
                <Skeleton key={i} className="h-[100px]" />
            )
        }
        return (
            <div className="w-full grid grid-cols-4 gap-3">
                {skeletons}
            </div>
        );
    }

    if (isError) {
        console.error('An error occurred while fetching storages', error);
        let message = 'An unknown error occurred. Please try again later.';
        if ('status' in error) {
            switch (error.status) {
                case 401:
                    message = 'You do not have permission to view this content.';
                    break;
            }
        }
        return (
            <Alert variant="destructive" className="mt-2 p-2">
                <AlertCircleIcon />
                <AlertTitle>
                    Error while loading storages.
                </AlertTitle>
                <AlertDescription>
                    {message}
                </AlertDescription>
            </Alert>
        );
    }

    return (
        <>
            <nav className="mb-5 flex justify-start gap-3">
                <Button size="sm" onClick={() => setIsModalOpen(true)}>
                    <Plus className="w-4 h-4 mr-1" />
                    Add Storage
                </Button>
            </nav>

            <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>
                            Create Storage
                        </DialogTitle>
                        <DialogDescription>
                            You will become the admin of the storage you create.
                        </DialogDescription>
                    </DialogHeader>
                    <StorageCreationForm onSuccess={handleModalClose} />
                </DialogContent>
            </Dialog>

            <section>
                {
                    (storages?.length === 0) ? (
                        <Alert>
                            <AlertTitle>
                                You seem to have no storages.
                            </AlertTitle>
                            <AlertDescription>
                                Your storages will be shown here.
                            </AlertDescription>
                        </Alert>
                    ) : (
                        <ul className="w-full grid grid-cols-5 gap-3">
                            {storages?.map(s => (
                                <li key={s.id}>
                                    <StorageCard storage={s} />
                                </li>
                            ))}
                        </ul>
                    )
                }
            </section>
        </>
    );
}

export default StorageOverview;
