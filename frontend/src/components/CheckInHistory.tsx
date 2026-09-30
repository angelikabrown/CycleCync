import { useEffect, useState } from "react";
import type { DailyCheckIn } from "../types/DailyCheckin";
import DailyCheckInForm from "./DailyCheckInForm";

type CheckInHistoryProps = {
    refreshTrigger: number;
};

function CheckInHistory({ refreshTrigger }: CheckInHistoryProps) {
    const [checkins, setCheckins] = useState<DailyCheckIn[]>([]);
    const [checkinToEdit, setCheckinToEdit] =
        useState<DailyCheckIn | null>(null);

    const fetchCheckIns = () => {
        const token = sessionStorage.getItem("token");

        fetch("http://localhost:8000/daily_checkins/", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })
            .then((res) => {
                if (!res.ok) {
                    throw new Error(`HTTP ${res.status}`);
                }

                return res.json();
            })
            .then((data) => {
                setCheckins(data);
            })
            .catch((err) => console.error("Fetch Error:", err));
    };

    useEffect(() => {
        fetchCheckIns();
    }, [refreshTrigger]);

    const handleDelete = async (checkinId: number) => {
        const confirmed = window.confirm(
            "Are you sure you want to delete this check-in?"
        );

        if (!confirmed) {
            return;
        }

        const token = sessionStorage.getItem("token");

        try {
            const response = await fetch(
                `http://localhost:8000/daily_checkins/${checkinId}`,
                {
                    method: "DELETE",
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            setCheckins((currentCheckins) =>
                currentCheckins.filter(
                    (checkin) => checkin.id !== checkinId
                )
            );
        } catch (error) {
            console.error("Delete Error:", error);
            alert("Unable to delete this check-in.");
        }
    };

    const handleEditComplete = () => {
        setCheckinToEdit(null);
        fetchCheckIns();
    };

    return (
        <div>
            <h2>Daily Check-Ins</h2>

            {checkinToEdit && (
                <div>
                    <DailyCheckInForm
                        onCheckInSaved={() => { }}
                        checkinToEdit={checkinToEdit}
                        onEditComplete={handleEditComplete}
                    />

                    <button
                        type="button"
                        onClick={() => setCheckinToEdit(null)}
                    >
                        Cancel
                    </button>

                    <hr />
                </div>
            )}

            {checkins.length === 0 ? (
                <p>No check-ins found.</p>
            ) : (
                checkins.map((checkin) => (
                    <div key={checkin.id}>
                        <p>
                            <strong>Date:</strong> {checkin.date}
                        </p>

                        <p>📅 CD: {checkin.cycle_day}</p>
                        <p>🌡 BBT: {checkin.bbt}</p>
                        <p>😊 Mood: {checkin.mood}</p>
                        <p>⚡ Energy: {checkin.energy_level}</p>
                        <p>😴 Sleep: {checkin.sleep_quality}</p>
                        <p>📝 Notes: {checkin.notes}</p>

                        <button
                            onClick={() =>
                                setCheckinToEdit(checkin)
                            }
                        >
                            Edit
                        </button>

                        <button
                            onClick={() =>
                                handleDelete(checkin.id)
                            }
                        >
                            Delete
                        </button>

                        <hr />
                    </div>
                ))
            )}
        </div>
    );
}

export default CheckInHistory;