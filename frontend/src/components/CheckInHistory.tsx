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

function CheckInHistory() {
    const [checkins, setCheckins] = useState<DailyCheckIn[]>([]);

    useEffect(() => {
        console.log("useEffect running");

        const token = sessionStorage.getItem("token");
        console.log("Token:", token);

        fetch("http://localhost:8000/daily_checkins/", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
            .then((res) => {
                console.log("Status:", res.status);

                if (!res.ok) {
                    throw new Error(`HTTP ${res.status}`);
                }

                return res.json();
            })
            .then((data) => {
                console.log("Data:", data);
                setCheckins(data);
            })
            .catch((err) => console.error("Fetch Error:", err));
    }, []);

    return (
        <div>
            <h2>Daily Check-Ins</h2>

            {checkins.length === 0 ? (
                <p>No check-ins found.</p>
            ) : (
                checkins.map((checkin) => (
                    <div key={checkin.id}>
                        <p>
                            <strong>Date:</strong> {checkin.date}
                        </p>
                        <p>🌡 BBT: {checkin.bbt}</p>
                        <p>😊 Mood: {checkin.mood}</p>
                        <p>⚡ Energy: {checkin.energy_level}</p>
                        <p>😴 Sleep: {checkin.sleep_quality}</p>
                        <p>📝 Notes: {checkin.notes}</p>
                        <hr />
                    </div>
                ))
            )}
        </div>
    );
}

export default CheckInHistory;