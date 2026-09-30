import { useEffect, useState } from "react";
import BBTChart from "./BBTChart";
import MoodChart from "./MoodChart";
import EnergyChart from "./EnergyChart";
import SleepChart from "./SleepChart";

type DailyCheckIn = {
    id: number;
    date: string;
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

    const latestCheckin = checkins[0];

    return (
        <div className="min-h-screen bg-[#F3F1EA] text-[#173B32]">
            <main className="mx-auto w-full max-w-6xl px-4 py-6 sm:px-6 lg:px-8">



                {/* Header */}
                <header className="mb-7">
                    <div className="mb-3 inline-flex rounded-full bg-[#DDE9E1] px-3 py-1 text-xs font-semibold tracking-widest text-[#245544]">
                        CYCLECYNC
                    </div>

                    <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
                        Your cycle, your patterns.
                    </h1>

                    <p className="mt-2 max-w-xl text-sm leading-6 text-[#61756D] sm:text-base">
                        Keep track of your daily data and start noticing
                        what your cycle looks like over time.
                    </p>
                </header>

                {/* Cycle summary */}
                <section className="mb-8 overflow-hidden rounded-[28px] bg-[#245544] shadow-lg">
                    <div className="p-6 text-white sm:p-8">

                        <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">

                            <div>
                                <p className="text-sm font-medium text-[#C9DED4]">
                                    Current cycle
                                </p>

                                <div className="mt-1 flex items-baseline gap-2">
                                    <span className="text-5xl font-bold">
                                        {latestCheckin?.cycle_day ?? "—"}
                                    </span>

                                    <span className="text-base text-[#C9DED4]">
                                        cycle day
                                    </span>
                                </div>

                                <p className="mt-2 text-sm text-[#C9DED4]">
                                    {latestCheckin
                                        ? "Based on your latest check-in"
                                        : "Start checking in to see your cycle"}
                                </p>
                            </div>

                            <div className="rounded-2xl bg-[#376B5A] px-5 py-4">
                                <p className="text-xs font-medium uppercase tracking-wide text-[#C9DED4]">
                                    Latest check-in
                                </p>

                                <p className="mt-1 text-lg font-semibold">
                                    {latestCheckin?.date ?? "No data yet"}
                                </p>
                            </div>

                        </div>
                    </div>
                </section>

                {/* Patterns heading */}
                <div className="mb-5">
                    <h2 className="text-2xl font-bold">
                        Your patterns
                    </h2>

                    <p className="mt-1 text-sm text-[#657870]">
                        See how your daily measurements change across
                        your cycle.
                    </p>
                </div>

                {/* Charts */}
                <div className="grid gap-5 lg:grid-cols-2">

                    {/* BBT */}
                    <section className="rounded-[28px] bg-[#E9E2F5] p-5 shadow-sm sm:p-6">
                        <div className="mb-4 flex items-start justify-between">
                            <div>
                                <h3 className="text-lg font-bold text-[#463765]">
                                    Basal Body Temperature
                                </h3>

                                <p className="mt-1 text-sm text-[#685C7D]">
                                    Temperature by cycle day
                                </p>
                            </div>

                            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#D5C8EA] text-xl">
                                🌡
                            </div>
                        </div>

                        <div className="overflow-hidden rounded-2xl bg-[#F6F2FA] p-2">
                            <BBTChart checkins={checkins} />
                        </div>
                    </section>

                    {/* Mood */}
                    <section className="rounded-[28px] bg-[#E5DDF2] p-5 shadow-sm sm:p-6">
                        <div className="mb-4 flex items-start justify-between">
                            <div>
                                <h3 className="text-lg font-bold text-[#463765]">
                                    Mood
                                </h3>

                                <p className="mt-1 text-sm text-[#685C7D]">
                                    How you've been feeling
                                </p>
                            </div>

                            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#D0C3E5] text-xl">
                                ◌
                            </div>
                        </div>

                        <div className="overflow-hidden rounded-2xl bg-[#F5F1F9] p-2">
                            <MoodChart checkins={checkins} />
                        </div>
                    </section>

                    {/* Energy */}
                    <section className="rounded-[28px] bg-[#F6E3C8] p-5 shadow-sm sm:p-6">
                        <div className="mb-4 flex items-start justify-between">
                            <div>
                                <h3 className="text-lg font-bold text-[#754719]">
                                    Energy
                                </h3>

                                <p className="mt-1 text-sm text-[#89694B]">
                                    Your energy across the cycle
                                </p>
                            </div>

                            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#EBCB9F] text-xl">
                                ☀
                            </div>
                        </div>

                        <div className="overflow-hidden rounded-2xl bg-[#FCF4E8] p-2">
                            <EnergyChart checkins={checkins} />
                        </div>
                    </section>

                    {/* Sleep */}
                    <section className="rounded-[28px] bg-[#DDE9F0] p-5 shadow-sm sm:p-6">
                        <div className="mb-4 flex items-start justify-between">
                            <div>
                                <h3 className="text-lg font-bold text-[#31566B]">
                                    Sleep
                                </h3>

                                <p className="mt-1 text-sm text-[#5E7482]">
                                    Your sleep quality
                                </p>
                            </div>

                            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[#C3D9E5] text-xl">
                                ☾
                            </div>
                        </div>

                        <div className="overflow-hidden rounded-2xl bg-[#F1F7FA] p-2">
                            <SleepChart checkins={checkins} />
                        </div>
                    </section>

                </div>

                {/* Compare */}
                <section className="mt-7 rounded-[28px] bg-[#DDE9E1] p-5 shadow-sm sm:p-6">
                    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

                        <div>
                            <h3 className="text-lg font-bold text-[#245544]">
                                Compare your patterns
                            </h3>

                            <p className="mt-1 max-w-xl text-sm leading-6 text-[#587066]">
                                Explore connections between your cycle,
                                mood, energy, sleep, and temperature.
                            </p>
                        </div>

                        <span className="w-fit rounded-full bg-[#B9D4C5] px-4 py-2 text-xs font-bold text-[#245544]">
                            Coming soon
                        </span>

                    </div>
                </section>

            </main>
        </div>
    );
}

export default Dashboard;