"use client"

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label"
import { useCreateStorageMutation } from "@/redux/api/storaSenseApi";
import { CreateStorageRequest } from "@/redux/api/storaSenseApiSchemas";
import { Formik, FormikConfig, FormikErrors } from "formik";
import { useRouter } from "next/navigation";
import { FC } from "react";


interface FormState {
    storageName: string;
}


const StorageCreationForm: FC = () => {
    const router = useRouter();
    const [createStorage] = useCreateStorageMutation();

    const formConfig: FormikConfig<FormState> = {
        initialValues: {
            storageName: ''
        },
        validate: (values) => {
            console.log('hello')
            const errors: FormikErrors<FormState> = {};
            const storageNameRegex = /^[a-zA-Z]+[a-zA-Z0-9]*/;

            if (!values.storageName) {
                errors.storageName = "This field is required";
            } else if (values.storageName.length < 5) {
                errors.storageName = "Name must be at least 5 characters long";
            } else if (!storageNameRegex.test(values.storageName)) {
                errors.storageName = ""
            }
            return errors;
        },
        onSubmit: (values, { setSubmitting }) => {
            console.log('world')
            const request: CreateStorageRequest = {
                name: values.storageName
            }
            createStorage(request)
                .unwrap()
                .then(() => {
                    setSubmitting(false);
                    router.push('/dashboard/storages');
                })
                .catch(reason => {
                    setSubmitting(false);
                    console.error(reason);
                })
        }
    }

    return (
        <Formik {...formConfig}>
            {(props) => (
                <form className="w-full max-w-[600px] flex flex-col gap-3" onSubmit={props.handleSubmit}>
                    <div>
                        <Label htmlFor="storageName" className="mb-1">
                            Storage Name
                        </Label>
                        <Input
                            id="storageName"
                            name="storageName"
                            value={props.values.storageName}
                            onChange={props.handleChange}
                            onBlur={props.handleBlur}
                            aria-invalid={(props.errors.storageName && props.touched.storageName) ? true : false}
                        />
                        <div className="text-sm text-destructive">
                            {props.errors.storageName && props.touched.storageName && props.errors.storageName}
                        </div>
                    </div>
                    <Button type="submit">
                        Submit Purchase Request
                    </Button>
                </form>
            )}
        </Formik>
    );
}

export default StorageCreationForm;
