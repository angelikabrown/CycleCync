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
        Low: 1,
        Moderate: 2,
        Good: 3,
        High: 4,
    };

    const energyLabels: Record<number, string> = {
        1: "Low",
        2: "Moderate",
        3: "Good",
        4: "High",
    };

    const chartData = checkins
        .filter(
            (checkin) =>
                checkin.cycle_day !== null &&
                checkin.energy_level !== null
        )
        .map((checkin) => ({
            cycleDay: checkin.cycle_day,
            energy: energyValues[checkin.energy_level!],
        }))
        .filter((checkin) => checkin.energy !== undefined)
        .sort((a, b) => a.cycleDay! - b.cycleDay!);

    if (chartData.length === 0) {
        return <p>No energy data available yet.</p>;
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
                    tickFormatter={(value) => energyLabels[value]}
                />

                <Tooltip
                    formatter={(value) => [
                        energyLabels[value as number],
                        "Energy",
                    ]}
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