import {FC, ReactNode} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {FaCircleInfo as InfoIcon} from "react-icons/fa6";
import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert";


interface ActiveStorageRequiredProps {
    children: ReactNode;
}

const ActiveStorageRequired: FC<ActiveStorageRequiredProps> = ({ children }) => {
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage);

    if (!activeStorage) {
        return (
            <Alert className="mt-2 p-2">
                <InfoIcon />
                <AlertTitle>
                    You cannot view this content.
                </AlertTitle>
                <AlertDescription>
                    No storage is currently selected!
                </AlertDescription>
            </Alert>
        );
    }

    return children;
}

export default ActiveStorageRequired;
