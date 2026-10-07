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
        "Very Bad": 1,
        Bad: 2,
        OK: 3,
        Good: 4,
        Excellent: 5,
    };

    const chartData = checkins
        .filter(
            (checkin) =>
                checkin.cycle_day !== null &&
                checkin.mood !== null
        )
        .map((checkin) => ({
            cycleDay: checkin.cycle_day!,
            mood: moodValues[checkin.mood!],
        }))
        .filter((item) => item.mood !== undefined)
        .sort((a, b) => a.cycleDay - b.cycleDay);

    if (chartData.length === 0) {
        return <p>No mood data available yet.</p>;
    }

    const cycleDays = [
        ...new Set(chartData.map((item) => item.cycleDay)),
    ];

    let xAxisTicks: number[];

    if (cycleDays.length <= 15) {
        xAxisTicks = cycleDays;
    } else {
        const step = Math.ceil(cycleDays.length / 8);

        xAxisTicks = cycleDays.filter(
            (_, index) => index % step === 0
        );

        const lastDay = cycleDays[cycleDays.length - 1];

        if (xAxisTicks[xAxisTicks.length - 1] !== lastDay) {
            xAxisTicks.push(lastDay);
        }
    }

    return (
        <ResponsiveContainer width="100%" height={200}>
            <LineChart
                data={chartData}
                margin={{
                    top: 10,
                    right: 20,
                    left: 55,
                    bottom: 10,
                }}
            >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis
                    dataKey="cycleDay"
                    type="number"
                    domain={["dataMin", "dataMax"]}
                    ticks={xAxisTicks}
                    allowDecimals={false}
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
                            1: "Very Bad",
                            2: "Bad",
                            3: "OK",
                            4: "Good",
                            5: "Excellent",
                        };

                        return labels[value] ?? "";
                    }}
                />

                <Tooltip
                    formatter={(value) => {
                        const labels: Record<number, string> = {
                            1: "Very Bad",
                            2: "Bad",
                            3: "OK",
                            4: "Good",
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
                    dataKey="mood"
                    strokeWidth={2}
                    dot
                />
            </LineChart>
        </ResponsiveContainer>
    );
}

export default MoodChart;