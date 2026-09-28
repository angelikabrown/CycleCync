import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

type DailyCheckIn = {
    id: number;
    date: string;
    cycle_day: number | null;
    bbt: number | null;
};

type BBTChartProps = {
    checkins: DailyCheckIn[];
};

function BBTChart({ checkins }: BBTChartProps) {
    const bbtData = checkins
        .filter(
            (checkin) =>
                checkin.bbt !== null &&
                checkin.cycle_day !== null
        )
        .map((checkin) => ({
            cycleDay: checkin.cycle_day,
            bbt: checkin.bbt,
        })).sort((a, b) => a.cycleDay - b.cycleDay);

    if (bbtData.length === 0) {
        return <p>No BBT data available yet.</p>;
    }

    return (
        <ResponsiveContainer width="100%" height={300}>
            <LineChart data={bbtData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="cycleDay" />

                <YAxis
                    domain={["dataMin - 0.2", "dataMax + 0.2"]}
                />

                <Tooltip />

                <Line
                    type="monotone"
                    dataKey="bbt"
                    stroke="#8884d8"
                    strokeWidth={2}
                    dot
                />
            </LineChart>
        </ResponsiveContainer>
    );
}

export default BBTChart;