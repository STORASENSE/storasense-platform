"use client"

import { FC } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useGetMyStoragesQuery } from "@/redux/api/storaSenseApi";
import { Skeleton } from "@/components/ui/skeleton";
import { useDispatch, useSelector } from "react-redux";
import { StoraSenseStorge } from "@/redux/api/storaSenseApiSchemas";
import { setActiveStorage } from "@/redux/slices/storageSlice";
import { RootState } from "@/redux/store";

const ActiveStorageSelection: FC = () => {
    const dispatch = useDispatch();
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage);
    const {data: storages, isLoading, isError, error} = useGetMyStoragesQuery();

    if (isLoading) {
        return (
            <Skeleton className="h-[40px] w-[170px]"/>
        )
    }

    if (isError) {
        console.error("Error while loading storages", error);
        return <></>;
    }

    function handleValueChange(storageJson: string) {
        const storage: StoraSenseStorge = JSON.parse(storageJson);
        dispatch(setActiveStorage(storage));
    }

    return (
        <Select
            value={activeStorage? JSON.stringify(activeStorage) : undefined}
            onValueChange={handleValueChange}
        >
            <SelectTrigger>
                <SelectValue placeholder="Storage" />
            </SelectTrigger>
            <SelectContent>
                {storages?.map(storage => (
                    <SelectItem key={storage.id} value={JSON.stringify(storage)}>
                        {storage.name}
                    </SelectItem>
                ))}
            </SelectContent>
        </Select>
    )
}

export default ActiveStorageSelection;
