"use client"

import {FC, useMemo, useState} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetMeQuery, useGetUsersByStorageIdQuery, useRemoveUserFromStorageMutation} from "@/redux/api/storaSenseApi";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import {Skeleton} from "@/components/ui/skeleton";
import {Card} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {UserRole} from "@/redux/api/storaSenseApiSchemas";
import { Dialog, DialogHeader, DialogTitle, DialogDescription, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import AddUserToStorageForm from "./AddUserToStorageForm";
import { FaTrash as TrashIcon } from "react-icons/fa6";


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
        return users.find(user => user.username === me.username)?.role;
    }, [users, me]);

    //////////////////////////////////////////////////////////////////////////////////

    const [isAddUserDialogOpen, setIsAddUserDialogOpen] = useState<boolean>(false);

    //////////////////////////////////////////////////////////////////////////////////

    const [removeUserFromStorage] = useRemoveUserFromStorageMutation();

    function handleRemoveUserFromStorage(username: string) {
        removeUserFromStorage({
            username, storage_id: activeStorage.id
        })
        .unwrap()
        .catch((error: any) => {
            console.error(`Failed to remove user '${username}' from storage '${activeStorage.name}'`, error);
        });
    }

    //////////////////////////////////////////////////////////////////////////////////

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
                    <Dialog open={isAddUserDialogOpen} onOpenChange={setIsAddUserDialogOpen}>
                        <DialogTrigger asChild>
                            <Button>
                                Add User
                            </Button>
                        </DialogTrigger>
                        <DialogContent>
                            <DialogHeader>
                                <DialogTitle>
                                    Add User
                                </DialogTitle>
                                <DialogDescription>
                                    Add a new contributor to this storage.
                                </DialogDescription>
                            </DialogHeader>
                            <AddUserToStorageForm
                                onSuccess={() => setIsAddUserDialogOpen(false)}
                            />
                        </DialogContent>
                    </Dialog>
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
                        {(myRole === UserRole.ADMIN) && (
                            <TableHead>
                                Actions
                            </TableHead>
                        )}
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {users!.map(user => (
                        <TableRow key={user.id}>
                            <TableCell className="h-[50px]">
                                {user.username}
                            </TableCell>
                            <TableCell>
                                {user.role || <span>None</span>}
                            </TableCell>
                            {(myRole === UserRole.ADMIN) && (
                                <TableCell>
                                    {(user.username !== me!.username) && (
                                        <Button
                                            size="sm"
                                            variant="ghost"
                                            onClick={() => handleRemoveUserFromStorage(user.username)}
                                            className="text-cerise-red hover:text-cerise-red-700 hover:bg-cerise-red/5">
                                            <TrashIcon />
                                        </Button>
                                    )}
                                </TableCell>
                            )}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </Card>
    );
}

export default UsersTable;
