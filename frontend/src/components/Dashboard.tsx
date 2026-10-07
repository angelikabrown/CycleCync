import { useEffect, useState } from "react";
import BBTChart from "./BBTChart";
import MoodChart from "./MoodChart";
import EnergyChart from "./EnergyChart";
import SleepChart from "./SleepChart";
import Calendar from "./Calendar";

type DailyCheckIn = {
    id: number;
    date: string;
    period: boolean;
    cycle_day: number | null;
    bbt: number | null;
    mood: string | null;
    energy_level: string | null;
    sleep_quality: string | null;
    notes: string | null;
};

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
                console.error(
                    "Error fetching dashboard data:",
                    error
                );
            });
    }, []);

    return (
        <main className="min-h-screen bg-[#F4F1EA] px-4 py-6 sm:px-6 lg:px-8">

            {/* Page Header */}
            <div className="mx-auto max-w-5xl">
            </div>

            <header className="mb-6">
                <p className="text-sm font-medium text-[#5B7F71]">
                    CycleCync
                </p>

                <h1 className="mt-1 text-3xl font-bold tracking-tight text-[#24352F] sm:text-4xl">
                    Your cycle, your patterns.
                </h1>

                <p className="mt-2 max-w-xl text-sm leading-6 text-[#6B6B65]">
                    Track your daily data and see how your patterns
                    change throughout your cycle.
                </p>
            </header>

            {/* Current Cycle Card */}
            <section className="mb-6 overflow-hidden rounded-3xl bg-[#315C4E] p-6 text-white shadow-sm">
                <p className="text-sm font-medium text-[#D8E8E1]">
                    Current Cycle
                </p>

                <div className="mt-2 flex items-end justify-between">
                    <div>
                        <p className="text-4xl font-bold">
                            Day {checkins[0]?.cycle_day ?? "—"}
                        </p>

                        <p className="mt-1 text-sm text-[#D8E8E1]">
                            Based on your latest check-in
                        </p>
                    </div>

                    <div className="rounded-2xl bg-white/10 px-4 py-3 text-right">
                        <p className="text-xs text-[#D8E8E1]">
                            Days logged
                        </p>

                        <p className="text-xl font-semibold">
                            {checkins.length}
                        </p>
                    </div>
                </div>
            </section>

            {/* Calendar */}
            <section className="mb-6">
                <div className="mb-3">
                    <h2 className="text-xl font-bold text-[#24352F]">
                        Your Calendar
                    </h2>

                    <p className="mt-1 text-sm text-[#6B6B65]">
                        Select a day to see what you recorded.
                    </p>
                </div>

                <Calendar checkins={checkins} />
            </section>

            {/* Patterns Heading */}
            <div className="mb-4">
                <h2 className="text-xl font-bold text-[#24352F]">
                    Your Patterns
                </h2>

                <p className="mt-1 text-sm text-[#6B6B65]">
                    Explore how your daily measurements change
                    throughout your cycle.
                </p>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">

                {/* BBT */}
                <section className="lg:col-span-2 rounded-3xl bg-[#E8E0F2] p-5 shadow-sm">
                    <div className="mb-4">
                        <h3 className="text-lg font-bold text-[#433B52]">
                            Basal Body Temperature
                        </h3>

                        <p className="text-sm text-[#6E6678]">
                            Temperature changes across your cycle.
                        </p>
                    </div>

                    <BBTChart checkins={checkins} />
                </section>

                {/* Mood */}
                <section className="rounded-3xl bg-[#EEE8F7] p-5 shadow-sm">
                    <div className="mb-4">
                        <h3 className="text-lg font-bold text-[#433B52]">
                            Mood
                        </h3>

                        <p className="text-sm text-[#6E6678]">
                            How your mood changes from day to day.
                        </p>
                    </div>

                    <MoodChart checkins={checkins} />
                </section>

                {/* Energy */}
                <section className="rounded-3xl bg-[#F7E4CF] p-5 shadow-sm">
                    <div className="mb-4">
                        <h3 className="text-lg font-bold text-[#65452D]">
                            Energy
                        </h3>

                        <p className="text-sm text-[#80644E]">
                            Notice changes in your energy levels.
                        </p>
                    </div>

                    <EnergyChart checkins={checkins} />
                </section>

                {/* Sleep */}
                <section className="rounded-3xl bg-[#DDEBF0] p-5 shadow-sm">
                    <div className="mb-4">
                        <h3 className="text-lg font-bold text-[#34515C]">
                            Sleep
                        </h3>

                        <p className="text-sm text-[#5E737C]">
                            See how your sleep quality changes.
                        </p>
                    </div>

                    <SleepChart checkins={checkins} />
                </section>

            </div>

            {/* Compare */}
            <section className="mt-6 rounded-3xl bg-[#DDD7E8] p-6 shadow-sm">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                        <p className="text-sm font-medium text-[#665D75]">
                            Explore your data
                        </p>

                        <h2 className="mt-1 text-xl font-bold text-[#393246]">
                            Compare your patterns
                        </h2>

                        <p className="mt-1 max-w-lg text-sm leading-6 text-[#665D75]">
                            Compare mood, energy, sleep, and other
                            measurements to look for relationships
                            in your own data.
                        </p>
                    </div>

                    <button
                        type="button"
                        className="rounded-xl bg-[#315C4E] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#264A3F]"
                    >
                        Compare
                    </button>
                </div>
            </section>

        </main>
    );
}

export default Dashboard;