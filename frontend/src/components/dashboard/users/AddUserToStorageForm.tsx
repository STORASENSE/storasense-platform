import { Button } from "@/components/ui/button";
import { DialogFooter, DialogClose } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAddUserToStorageMutation } from "@/redux/api/storaSenseApi";
import { FastApiError } from "@/redux/api/storaSenseApiErrors";
import { RootState } from "@/redux/store";
import { Formik, FormikConfig, FormikErrors } from "formik";
import { AlertCircle } from "lucide-react";
import { FC } from "react";
import { useSelector } from "react-redux";


interface FormState {
    username: string;
}


interface AddUserToStorageFormProps {
    onSuccess?: () => void;
}

const AddUserToStorageForm: FC<AddUserToStorageFormProps> = ({ onSuccess }) => {
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage)!;
    const [addUserToStorage] = useAddUserToStorageMutation();

    const formikConfig: FormikConfig<FormState> = {
        initialValues: {
            username: ''
        },
        validate: (values) => {
            const errors: FormikErrors<FormState> = {};
            if (!values.username.trim()) {
                errors.username = "Username is required."
            }
            return errors;
        },
        onSubmit: async (values, { setSubmitting, resetForm, setStatus }) => {
            try {
                setStatus(null);
                await addUserToStorage({
                    username: values.username.trim().toLowerCase(),
                    storage_id: activeStorage.id
                }).unwrap();
                resetForm();
                if (onSuccess) {
                    onSuccess();
                }
            } catch (error: any) {
                console.error('Failed to create storage:', error);
                if ('status' in error) {
                    setStatus('Failed to create storage. Please try again.');
                }
                switch ((error as FastApiError).status) {
                    case 401:
                        setStatus("You aren't authorized to add new users.");
                        break;
                    case 409:
                        setStatus("The given username does not exist.");
                        break;
                    default:
                        setStatus("An unknown error occurred. Please try again later.");
                        break;
                }
            } finally {
                setSubmitting(false);
            }
        }
    }

    return (
        <Formik {...formikConfig}>
            {(formik) => (
                <form className="space-y-6" onSubmit={formik.handleSubmit}>
                        {formik.status && (
                            <div className="flex items-center gap-2 text-sm text-destructive bg-destructive/10 p-3 rounded-md">
                                <AlertCircle className="w-4 h-4" />
                                {formik.status}
                            </div>
                        )}

                        <div className="space-y-2">
                            <Label htmlFor="storageName" className="text-sm font-medium">
                                User Name
                            </Label>
                            <Input
                                id="username"
                                name="username"
                                placeholder="Enter username"
                                value={formik.values.username}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                className={`transition-colors ${
                                    formik.errors.username && formik.touched.username
                                        ? 'border-destructive focus-visible:ring-destructive'
                                        : ''
                                }`}
                                aria-invalid={!!(formik.errors.username && formik.touched.username)}
                                disabled={formik.isSubmitting}
                            />
                            {formik.errors.username && formik.touched.username && (
                                <div className="flex items-center gap-2 text-sm text-destructive">
                                    <AlertCircle className="w-4 h-4" />
                                    {formik.errors.username}
                                </div>
                            )}
                        </div>

                        <DialogFooter className="flex gap-3 pt-4">
                            <DialogClose asChild>
                                <Button
                                    type="button"
                                    variant="outline"
                                    className="flex-1"
                                    disabled={formik.isSubmitting}>
                                    Cancel
                                </Button>
                            </DialogClose>
                            <Button
                                type="submit"
                                className="flex-1 bg-blue-whale hover:bg-blue-whale/90"
                                disabled={formik.isSubmitting || !formik.isValid || !formik.dirty}
                            >
                                {formik.isSubmitting ? 'Working...' : 'Add User'}
                            </Button>
                        </DialogFooter>
                    </form>
            )}
        </Formik>
    );
}

export default AddUserToStorageForm;
