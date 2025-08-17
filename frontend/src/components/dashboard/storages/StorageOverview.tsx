"use client"

import {FC, JSX, useState, Fragment} from "react";
import {useGetMyStoragesQuery} from "@/redux/api/storaSenseApi";
import StorageCard from "@/components/dashboard/storages/StorageCard";
import StorageCreationForm from "@/components/dashboard/storages/purchase/StorageCreationForm";
import {Skeleton} from "@/components/ui/skeleton";
import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert";
import {AlertCircleIcon, Plus} from "lucide-react";
import {Button} from "@/components/ui/button";
import {Dialog, Transition} from '@headlessui/react';

const StorageOverview: FC = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const {data: storages, isLoading, isError, error, refetch} = useGetMyStoragesQuery();

    const handleModalClose = () => {
        setIsModalOpen(false);
        refetch();
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

    if (storages?.length === 0) {
        return (
            <div className="space-y-6">
                <header className="flex justify-between items-center">
                    <div className="text-sm text-gray-600">0 Storages</div>
                    <Button
                        onClick={() => setIsModalOpen(true)}
                        className="bg-blue-whale text-white border-blue-whale"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        Add Storage
                    </Button>
                </header>

                <section className="text-center py-12">
                    <p className="text-gray-500 mb-4">
                        You seem to have no storages!
                    </p>
                </section>
                <Transition appear show={isModalOpen} as={Fragment}>
                    <Dialog as="div" className="relative z-10" onClose={setIsModalOpen}>
                        <div className="fixed inset-0 overflow-y-auto">
                            <div className="flex min-h-full items-center justify-center p-4">
                                <Transition.Child
                                    as={Fragment}
                                    enter="ease-out duration-300"
                                    enterFrom="opacity-0 scale-95"
                                    enterTo="opacity-100 scale-100"
                                    leave="ease-in duration-200"
                                    leaveFrom="opacity-100 scale-100"
                                    leaveTo="opacity-0 scale-95"
                                >
                                    <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                                        <Dialog.Title className="text-lg font-medium leading-6 text-gray-900 mb-4">
                                            Add New Storage
                                        </Dialog.Title>
                                        <StorageCreationForm onSuccess={handleModalClose} />
                                    </Dialog.Panel>
                                </Transition.Child>
                            </div>
                        </div>
                    </Dialog>
                </Transition>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <header className="flex justify-between items-center">
                <div className="text-sm text-gray-600">
                    {storages?.length || 0} Storages
                </div>
                <Button
                    onClick={() => setIsModalOpen(true)}
                    className="bg-blue-whale text-white border-blue-whale"
                >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Storage
                </Button>
            </header>

                <ul className="w-full grid grid-cols-5 gap-3">
                    {storages?.map(s => (
                        <li key={s.id}>
                            <StorageCard storage={s} />
                        </li>
                    ))}
                </ul>
                <Transition appear show={isModalOpen} as={Fragment}>
                        <Dialog as="div" className="relative z-10" onClose={setIsModalOpen}>
                    <div className="fixed inset-0 overflow-y-auto">
                        <div className="flex min-h-full items-center justify-center p-4">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-out duration-300"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                            >
                                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                                    <Dialog.Title className="text-lg font-medium leading-6 text-gray-900 mb-4">
                                        Add New Storage
                                    </Dialog.Title>
                                    <StorageCreationForm onSuccess={handleModalClose} />
                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </div>
                </Dialog>
            </Transition>
        </div>
    );
}

export default StorageOverview;
