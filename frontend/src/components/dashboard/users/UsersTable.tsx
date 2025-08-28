"use client"

import {FC, useMemo} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetMeQuery, useGetUsersByStorageIdQuery} from "@/redux/api/storaSenseApi";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import {Skeleton} from "@/components/ui/skeleton";
import {Card} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {UserRole} from "@/redux/api/storaSenseApiSchemas";


const UsersTable: FC = () => {
    // never undefined because wrapped in <RequiresActiveStorage>
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage)!;

    const {data: me, isLoading: isMeLoading, isError: isMeError, error: meError} = useGetMeQuery();

    const {data: users, isLoading, isError, error} = useGetUsersByStorageIdQuery({
        storage_id: activeStorage.id
    });

    const myRole = useMemo(() => {
        if (!users || !me) {
            return undefined;
        }
        return users.find(user => user.id === me.id)?.role;
    }, [users, me]);

    if (isLoading || isMeLoading) {
        return (
            <div className="w-full flex flex-col gap-2">
                <Skeleton className="h-[100px]"/>
                <Skeleton className="h-[100px]"/>
                <Skeleton className="h-[100px]"/>
            </div>
        );
    }

    if (isError || isMeError) {
        console.error(`Error while loading users in storage '${activeStorage.name}'`, error || meError);
        return <>Error!</>
    }

    return (
        <Card className="p-3">
            {(myRole === UserRole.ADMIN) && (
                <nav>
                    <Button>
                        Add User
                    </Button>
                </nav>
            )}

            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>
                            Username
                        </TableHead>
                        <TableHead>
                            Role
                        </TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {users!.map(user => (
                        <TableRow key={user.id}>
                            <TableCell>
                                {user.username}
                            </TableCell>
                            <TableCell>
                                {user.role || <span>None</span>}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </Card>
    );
}

export default UsersTable;
