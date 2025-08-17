"use client"

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateStorageMutation } from "@/redux/api/storaSenseApi";
import { CreateStorageRequest } from "@/redux/api/storaSenseApiSchemas";
import { Formik, FormikConfig, FormikErrors } from "formik";
import { FC } from "react";
import { AlertCircle } from "lucide-react";
import { FastApiError } from "@/redux/api/storaSenseApiErrors";

interface FormState {
    storageName: string;
}

interface StorageCreationFormProps {
    onSuccess?: () => void;
    onClose?: () => void;
}

const StorageCreationForm: FC<StorageCreationFormProps> = ({ onSuccess, onClose }) => {
    const [createStorage] = useCreateStorageMutation();

    const handleCancel = () => {
        if (onClose) {
            onClose();
        } else if (onSuccess) {
            onSuccess();
        }
    };

    const formConfig: FormikConfig<FormState> = {
        initialValues: {
            storageName: ''
        },
        validate: (values) => {
            const errors: FormikErrors<FormState> = {};
            const storageNameRegex = /^[a-zA-Z][a-zA-Z0-9]*$/;

            if (!values.storageName.trim()) {
                errors.storageName = "This field is required";
            } else if (values.storageName.trim().length < 3) {
                errors.storageName = "Name must be at least 3 characters long";
            } else if (values.storageName.trim().length > 50) {
                errors.storageName = "Name must not exceed 50 characters";
            } else if (!storageNameRegex.test(values.storageName.trim())) {
                errors.storageName = "Name must start with a letter and can only contain letters and numbers";
            }
            return errors;
        },
        onSubmit: async (values, { setSubmitting, resetForm, setStatus }) => {
            try {
                setStatus(null);
                const request: CreateStorageRequest = {
                    name: values.storageName.trim()
                };

                await createStorage(request).unwrap();

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
                    case 400:
                        setStatus("The data you entered was empty or malformed.");
                        break;
                    case 401:
                        setStatus("You aren't authorized to access this resource.");
                        break;
                    case 409:
                        setStatus("A storage with this name already exists.");
                        break;
                    default:
                        setStatus("An unknown error occurred. Please try again later.");
                        break;
                }
            } finally {
                setSubmitting(false);
            }
        }
    };

    return (
        <div className="space-y-6">
            <Formik {...formConfig}>
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
                                Storage Name
                            </Label>
                            <Input
                                id="storageName"
                                name="storageName"
                                placeholder="Enter storage name"
                                value={formik.values.storageName}
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                className={`transition-colors ${
                                    formik.errors.storageName && formik.touched.storageName
                                        ? 'border-destructive focus-visible:ring-destructive'
                                        : ''
                                }`}
                                aria-invalid={!!(formik.errors.storageName && formik.touched.storageName)}
                                disabled={formik.isSubmitting}
                            />
                            {formik.errors.storageName && formik.touched.storageName && (
                                <div className="flex items-center gap-2 text-sm text-destructive">
                                    <AlertCircle className="w-4 h-4" />
                                    {formik.errors.storageName}
                                </div>
                            )}
                        </div>

                        <div className="flex gap-3 pt-4">
                            <Button
                                type="button"
                                variant="outline"
                                className="flex-1"
                                onClick={handleCancel}
                                disabled={formik.isSubmitting}
                            >
                                Cancel
                            </Button>
                            <Button
                                type="submit"
                                className="flex-1 bg-blue-whale hover:bg-blue-whale/90"
                                disabled={formik.isSubmitting || !formik.isValid || !formik.dirty}
                            >
                                {formik.isSubmitting ? 'Creating...' : 'Add Storage'}
                            </Button>
                        </div>
                    </form>
                )}
            </Formik>
        </div>
    );
};

export default StorageCreationForm;
