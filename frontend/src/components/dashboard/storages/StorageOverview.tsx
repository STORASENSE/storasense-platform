"use client"

import {FC} from "react";
import {useGetMeQuery, useGetStoragesByUserIdQuery} from "@/redux/api/storaSenseApi";
import StorageCard from "@/components/dashboard/storages/StorageCard";


const StorageOverview: FC = () => {
    const {data: user, isLoading: isUserLoading, isError: isUserError} = useGetMeQuery();

    const {data: storages, isLoading: isStoragesLoading, isError: isStoragesError} = useGetStoragesByUserIdQuery({
        user_id: user!.id
    }, {
        skip: !user
    });

    if (isUserLoading || isStoragesLoading) {
        return 'Loading...';
    }

    if (isUserError) {
        return 'Error: Could not fetch user!';
    }

    if (isStoragesError) {
        return 'Error, could not fetch storages for user ' + user?.username;
    }

    return (
        <ul className="w-full grid grid-cols-5 gap-3">
            {storages!.map(s => (
                <li key={s.id}>
                    <StorageCard storage={s} />
                </li>
            ))}
        </ul>
    );
}

export default StorageOverview;
