"use client"

import {FC, useMemo} from "react";
import {StoraSenseStorge} from "@/redux/api/storaSenseApiSchemas";
import {Card} from "@/components/ui/card";
import {useDispatch, useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {setActiveStorage} from "@/redux/slices/storageSlice";
import { Button } from "@/components/ui/button";
import { FaTrash as TrashIcon } from "react-icons/fa6";
import { useDeleteStorageMutation } from "@/redux/api/storaSenseApi";


interface StorageCardProps {
    storage: StoraSenseStorge;
}

const StorageCard: FC<StorageCardProps> = ({ storage }) => {
    const dispatch = useDispatch();
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage);

    const [deleteStorage] = useDeleteStorageMutation();

    const isActive = useMemo<boolean>(() => {
        if (!activeStorage)
            return false;
        return activeStorage.id === storage.id;
    }, [storage, activeStorage]);

    function toggleActive() {
        if (isActive)
            dispatch(setActiveStorage(undefined));
        else
            dispatch(setActiveStorage(storage));
    }

    function handleDelete() {
        deleteStorage(storage.id)
        .unwrap()
        .then(() => {
            if (isActive) {
                dispatch(setActiveStorage(undefined));
            }
        })
        .catch((error: any) => {
            let message = 'An error occurred while deleting storage';
            if ('status' in error) {
                switch(error.status) {
                    case 404:
                        message = 'Error: storage does not exist';
                        break;
                    case 409:
                        message = 'Error: only admins can delete storages';
                        break;
                }
            }
            console.error(message, error);
        });
    }

    return (
        <Card
            data-active={isActive || undefined}
            className="
                p-0 hover:shadow-md select-none
                flex flex-row justify-between items-center gap-3
                data-active:border-l-4 data-active:border-l-blue-whale
                duration-300
            ">
            <div onClick={toggleActive} className="w-full h-full flex items-center cursor-pointer">
                <h3 className="ml-5 my-5 text-xl font-semibold text-blue-whale">
                    {storage.name || '[Unnamed Storage]'}
                </h3>
            </div>
            <div className="mr-5 my-5">
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleDelete}
                    className="text-cerise-red hover:text-cerise-red-700 hover:bg-cerise-red/5">
                    <TrashIcon />
                </Button>
            </div>
        </Card>
    );
}

export default StorageCard;
