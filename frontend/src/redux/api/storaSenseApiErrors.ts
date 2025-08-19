export interface FastApiError {
    status: number;
    data: {
        detail?: string;
    }
}
