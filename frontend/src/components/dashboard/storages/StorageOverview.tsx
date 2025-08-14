"use client"

import {FC, JSX} from "react";
import {useGetMeQuery, useGetStoragesByUserIdQuery} from "@/redux/api/storaSenseApi";
import StorageCard from "@/components/dashboard/storages/StorageCard";
import {Skeleton} from "@/components/ui/skeleton";
import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert";
import {AlertCircleIcon} from "lucide-react";


const StorageOverview: FC = () => {
    const {data: user, isLoading: isUserLoading, isError: isUserError, error: userError} = useGetMeQuery();

    const {data: storages, isLoading: isStoragesLoading, isError: isStoragesError, error: storageError} = useGetStoragesByUserIdQuery({
        user_id: user?.id || ''
    }, {
        skip: !user
    });

    if (isUserLoading || isStoragesLoading) {
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

    if (isUserError) {
        console.log(userError);
        return (
            <Alert variant="destructive" className="mt-2 p-2">
                <AlertCircleIcon />
                <AlertTitle>
                    Error while fetching user data.
                </AlertTitle>
                <AlertDescription>
                    An error occurred while attempting to fetch user data from the server.
                </AlertDescription>
            </Alert>
        );
    }

    if (isStoragesError || !storages) {
        console.log(storageError);
        return (
            <Alert variant="destructive" className="mt-2 p-2">
                <AlertCircleIcon />
                <AlertTitle>
                    Error while fetching storage data.
                </AlertTitle>
                <AlertDescription>
                    An error occurred while attempting to fetch storage data from the server.
                </AlertDescription>
            </Alert>
        );
    }

    if (storages.length === 0) {
        return (
            <div className="flex items-center">
                <span>You seem to have no storages!</span>
            </div>
        );
    }

    return (
        <ul className="w-full grid grid-cols-5 gap-3">
            {storages.map(s => (
                <li key={s.id}>
                    <StorageCard storage={s} />
                </li>
            ))}
        </ul>
    );
}

export default StorageOverview;
