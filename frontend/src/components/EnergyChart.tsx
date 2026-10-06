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

type EnergyChartProps = {
    checkins: DailyCheckIn[];
};

function EnergyChart({ checkins }: EnergyChartProps) {
    const energyValues: Record<string, number> = {
        "Very Low": 1,
        Low: 2,
        Moderate: 3,
        High: 4,
        "Very High": 5,
    };

    const chartData = checkins
        .filter(
            (checkin) =>
                checkin.cycle_day !== null &&
                checkin.energy_level !== null
        )
        .map((checkin) => ({
            cycleDay: String(checkin.cycle_day),
            energy: energyValues[checkin.energy_level!],
        }))
        .filter((item) => item.energy !== undefined)
        .sort((a, b) => Number(a.cycleDay) - Number(b.cycleDay));

    if (chartData.length === 0) {
        return <p>No energy data available yet.</p>;
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
                            1: "Very Low",
                            2: "Low",
                            3: "Moderate",
                            4: "High",
                            5: "Very High",
                        };

                        return labels[value] ?? "";
                    }}
                />

                <Tooltip
                    formatter={(value) => {
                        const labels: Record<number, string> = {
                            1: "Very Low",
                            2: "Low",
                            3: "Moderate",
                            4: "High",
                            5: "Very High",
                        };

                        return labels[value as number] ?? value;
                    }}
                    labelFormatter={(cycleDay) =>
                        `Cycle Day ${cycleDay}`
                    }
                />

                <Line
                    type="monotone"
                    dataKey="energy"
                    strokeWidth={2}
                    dot
                />
            </LineChart>
        </ResponsiveContainer>
    );
}

export default EnergyChart;