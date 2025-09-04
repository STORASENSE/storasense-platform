import {FC} from "react";
import {useDispatch, useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {AnalyticsTimeWindow} from "@/redux/api/storaSenseApiSchemas";
import {setTimeWindow} from "@/redux/slices/analyticsSlice";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select";


const TimeWindowSelection: FC = () => {
    const dispatch = useDispatch();
    const timeWindow = useSelector((state: RootState) => state.analytics.timeWindow);

    function handleValueChange(value: string) {
        dispatch(setTimeWindow(value as AnalyticsTimeWindow));
    }

    return (
        <Select value={timeWindow} onValueChange={handleValueChange}>
            <SelectTrigger className="min-w-[120px]">
                <SelectValue placeholder="Time WiNdow"/>
            </SelectTrigger>
            <SelectContent>
                <SelectItem value={"7d" satisfies AnalyticsTimeWindow}>
                    7 days
                </SelectItem>
                <SelectItem value={"30d" satisfies AnalyticsTimeWindow}>
                    30 days
                </SelectItem>
                <SelectItem value={"365d" satisfies AnalyticsTimeWindow}>
                    365 days
                </SelectItem>
            </SelectContent>
        </Select>
    );
}

export default TimeWindowSelection;
