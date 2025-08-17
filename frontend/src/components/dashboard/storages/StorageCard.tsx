"use client"

import {FC, useMemo} from "react";
import {StoraSenseStorge} from "@/redux/api/storaSenseApiSchemas";
import {Card, CardHeader, CardTitle} from "@/components/ui/card";
import {useDispatch, useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {setActiveStorage} from "@/redux/slices/storageSlice";


interface StorageCardProps {
    storage: StoraSenseStorge;
}

const StorageCard: FC<StorageCardProps> = ({ storage }) => {
    const dispatch = useDispatch();
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage);

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

    return (
        <Card
            data-active={isActive || undefined}
            onClick={toggleActive}
            className="cursor-pointer data-active:bg-blue-whale data-active:text-white duration-300">
            <CardHeader>
                <CardTitle>
                    {storage.name || '[Unnamed Storage]'}
                </CardTitle>
            </CardHeader>
        </Card>
    );
}

export default StorageCard;
