import { useGetMeQuery, useGetStoragesByUserIdQuery } from "@/redux/api/storaSenseApi";
import { FC } from "react";

const ActiveStorageUsers: FC = () => {
    const {data: user, isLoading: isUserLoading, isError: isUserError, error: userError} = useGetMeQuery();

    const {data: storages, isLoading: isStoragesLoading, isError: isStoragesError, error: storageError} = useGetStoragesByUserIdQuery({
        user_id: user?.id || ''
    }, {
        skip: !user
    });

    return (
        <></>
    );
}

export default ActiveStorageUsers;
