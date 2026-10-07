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
            cycleDay: checkin.cycle_day!,
            bbt: checkin.bbt!,
        }))
        .sort((a, b) => a.cycleDay - b.cycleDay);

    if (bbtData.length === 0) {
        return <p>No BBT data available yet.</p>;
    }

    const minBBT = Math.min(...bbtData.map((item) => item.bbt));
    const maxBBT = Math.max(...bbtData.map((item) => item.bbt));

    const yAxisMin = Math.floor((minBBT - 0.2) * 10) / 10;
    const yAxisMax = Math.ceil((maxBBT + 0.2) * 10) / 10;

    const cycleDays = [
        ...new Set(bbtData.map((item) => item.cycleDay)),
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
                data={bbtData}
                margin={{
                    top: 10,
                    right: 20,
                    left: 10,
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
                    domain={[yAxisMin, yAxisMax]}
                    tickFormatter={(value) => value.toFixed(1)}
                />

                <Tooltip
                    formatter={(value) =>
                        typeof value === "number"
                            ? value.toFixed(2)
                            : value
                    }
                    labelFormatter={(cycleDay) =>
                        `Cycle Day ${cycleDay}`
                    }
                />

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