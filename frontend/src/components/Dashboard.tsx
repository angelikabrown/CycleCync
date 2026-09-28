import { useEffect, useState } from "react";

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
                console.error("Error fetching dashboard data:", error);
            });
    }, []);

    return (
        <div>
            <h1>CycleCync Dashboard</h1>

            <section>
                <h2>Your Cycle</h2>
                <p>
                    Check-ins recorded: {checkins.length}
                </p>
            </section>

            <section>
                <h2>BBT</h2>

                {checkins.length === 0 ? (
                    <p>No BBT data yet.</p>
                ) : (
                    checkins.map((checkin) => (
                        <p key={checkin.id}>
                            {checkin.date}: {checkin.bbt ?? "No BBT"}
                        </p>
                    ))
                )}
            </section>
        </div>
    );
}

export default Dashboard;