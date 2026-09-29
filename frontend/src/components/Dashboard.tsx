import { useEffect, useState } from "react";
import BBTChart from "./BBTChart";
import MoodChart from "./MoodChart";
import EnergyChart from "./EnergyChart";
import SleepChart from "./SleepChart";
import type { DailyCheckIn } from "../types/DailyCheckin";
import Calendar from "./Calendar";

function Dashboard() {
    const [checkins, setCheckins] = useState<DailyCheckIn[]>([]);

    useEffect(() => {
        const token = sessionStorage.getItem("token");

        fetch("http://localhost:8000/daily_checkins/", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                return response.json();
            })
            .then((data) => {
                setCheckins(data);
            })
            .catch((error) => {
                console.error("Error fetching dashboard data:", error);
            });
    }, []);

    const currentCycleDay = checkins.reduce<number | null>(
        (latest, checkin) => {
            if (checkin.cycle_day === null) {
                return latest;
            }

            if (latest === null || checkin.cycle_day > latest) {
                return checkin.cycle_day;
            }

            return latest;
        },
        null
    );

    const latestBBT = [...checkins]
        .filter((checkin) => checkin.bbt !== null)
        .sort((a, b) => b.date.localeCompare(a.date))[0]?.bbt;

    return (
        <main className="min-h-screen bg-gray-50 px-4 py-6">
            <div className="mx-auto max-w-4xl">
                {/* Header */}
                <header className="mb-6">
                    <h1 className="text-2xl font-bold text-gray-900">
                        CycleCync
                    </h1>

                    <p className="mt-1 text-gray-600">
                        Understand your cycle through your own data.
                    </p>
                </header>

                {/* Cycle Summary */}
                <section className="mb-8">
                    <h2 className="mb-3 text-lg font-semibold text-gray-900">
                        Your Cycle
                    </h2>

                    <div className="grid grid-cols-2 gap-3">
                        <div className="rounded-xl bg-white p-4 shadow-sm">
                            <p className="text-sm text-gray-500">
                                Cycle Day
                            </p>

                            <p className="mt-1 text-2xl font-bold text-gray-900">
                                {currentCycleDay ?? "—"}
                            </p>
                        </div>

                        <div className="rounded-xl bg-white p-4 shadow-sm">
                            <p className="text-sm text-gray-500">
                                Days Logged
                            </p>

                            <p className="mt-1 text-2xl font-bold text-gray-900">
                                {checkins.length}
                            </p>
                        </div>

                        <div className="col-span-2 rounded-xl bg-white p-4 shadow-sm">
                            <p className="text-sm text-gray-500">
                                Latest BBT
                            </p>

                            <p className="mt-1 text-2xl font-bold text-gray-900">
                                {latestBBT !== undefined
                                    ? `${latestBBT}°F`
                                    : "—"}
                            </p>
                        </div>
                    </div>
                </section>

                {/* Calendar */}
                <section className="mb-8">
                    <h2 className="mb-3 text-lg font-semibold text-gray-900">
                        Calendar
                    </h2>

                    <Calendar checkins={checkins} />
                </section>

                {/* Trends */}
                <section>
                    <div className="mb-4 flex items-center justify-between">
                        <div>
                            <h2 className="text-xl font-bold text-gray-900">
                                Your Trends
                            </h2>

                            <p className="mt-1 text-sm text-gray-500">
                                See how your data changes across your cycle.
                            </p>
                        </div>
                    </div>

                    <div className="space-y-5">
                        <section className="rounded-xl bg-white p-4 shadow-sm">
                            <h3 className="mb-3 text-lg font-semibold text-gray-900">
                                BBT
                            </h3>
                            <BBTChart checkins={checkins} />
                        </section>

                        <section className="rounded-xl bg-white p-4 shadow-sm">
                            <h3 className="mb-3 text-lg font-semibold text-gray-900">
                                Mood
                            </h3>
                            <MoodChart checkins={checkins} />
                        </section>

                        <section className="rounded-xl bg-white p-4 shadow-sm">
                            <h3 className="mb-3 text-lg font-semibold text-gray-900">
                                Energy
                            </h3>
                            <EnergyChart checkins={checkins} />
                        </section>

                        <section className="rounded-xl bg-white p-4 shadow-sm">
                            <h3 className="mb-3 text-lg font-semibold text-gray-900">
                                Sleep
                            </h3>
                            <SleepChart checkins={checkins} />
                        </section>
                    </div>
                </section>
            </div>
        </main>
    );
}

export default Dashboard;