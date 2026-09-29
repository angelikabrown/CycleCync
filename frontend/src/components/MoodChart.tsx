import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

import type { DailyCheckIn } from "../types/DailyCheckin";

type MoodChartProps = {
    checkins: DailyCheckIn[];
};

function MoodChart({ checkins }: MoodChartProps) {
    const moodValues: Record<string, number> = {
        Poor: 1,
        Average: 2,
        Good: 3,
        Excellent: 4,
    };

    const chartData = checkins
        .filter(
            (checkin) =>
                checkin.cycle_day !== null &&
                checkin.mood !== null
        )
        .map((checkin) => ({
            cycleDay: checkin.cycle_day,
            mood: moodValues[checkin.mood!],
        }))
        .sort((a, b) => a.cycleDay! - b.cycleDay!);


    if (chartData.length === 0) {
        return <p>No mood data available yet.</p>;
    }

    return (
        <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                    dataKey="cycleDay"
                    label={{
                        value: "Cycle Day",
                        position: "insideBottom",
                        offset: -5,
                    }}
                />

                <YAxis
                    domain={[1, 4]}
                    ticks={[1, 2, 3, 4]}
                    tickFormatter={(value) => {
                        const labels: Record<number, string> = {
                            1: "Poor",
                            2: "Average",
                            3: "Good",
                            4: "Excellent",
                        };

                        return labels[value];
                    }}
                />

                <Tooltip />

                <Line
                    type="monotone"
                    dataKey="mood"
                    strokeWidth={2}
                    dot
                />
            </LineChart>
        </ResponsiveContainer>
    );
}

export default MoodChart;