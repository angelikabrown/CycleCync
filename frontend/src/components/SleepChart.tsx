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

type SleepChartProps = {
    checkins: DailyCheckIn[];
};

function SleepChart({ checkins }: SleepChartProps) {
    const sleepValues: Record<string, number> = {
        Poor: 1,
        Fair: 2,
        Good: 3,
        "Very Good": 4,
        Excellent: 5,
    };

    const chartData = checkins
        .filter(
            (checkin) =>
                checkin.cycle_day !== null &&
                checkin.sleep_quality !== null
        )
        .map((checkin) => ({
            cycleDay: String(checkin.cycle_day),
            sleep: sleepValues[checkin.sleep_quality!],
        }))
        .filter((item) => item.sleep !== undefined)
        .sort((a, b) => Number(a.cycleDay) - Number(b.cycleDay));

    if (chartData.length === 0) {
        return <p>No sleep data available yet.</p>;
    }

    return (
        <ResponsiveContainer width="100%" height={300}>
            <LineChart
                data={chartData}
                margin={{
                    top: 10,
                    right: 20,
                    left: 65,
                    bottom: 10,
                }}
            >
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
                    domain={[1, 5]}
                    ticks={[1, 2, 3, 4, 5]}
                    allowDecimals={false}
                    tickFormatter={(value) => {
                        const labels: Record<number, string> = {
                            1: "Poor",
                            2: "Fair",
                            3: "Good",
                            4: "Very Good",
                            5: "Excellent",
                        };

                        return labels[value] ?? "";
                    }}
                />

                <Tooltip
                    formatter={(value) => {
                        const labels: Record<number, string> = {
                            1: "Poor",
                            2: "Fair",
                            3: "Good",
                            4: "Very Good",
                            5: "Excellent",
                        };

                        return labels[value as number] ?? value;
                    }}
                    labelFormatter={(cycleDay) =>
                        `Cycle Day ${cycleDay}`
                    }
                />

                <Line
                    type="monotone"
                    dataKey="sleep"
                    strokeWidth={2}
                    dot
                />
            </LineChart>
        </ResponsiveContainer>
    );
}

export default SleepChart;