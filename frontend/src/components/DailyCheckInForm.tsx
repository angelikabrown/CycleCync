import { useEffect, useState } from "react";
import type { DailyCheckIn } from "../types/DailyCheckin";

type DailyCheckInFormProps = {
    onCheckInSaved: () => void;
    checkinToEdit?: DailyCheckIn | null;
    onEditComplete?: () => void;
};

function DailyCheckInForm({
    onCheckInSaved,
    checkinToEdit = null,
    onEditComplete,
}: DailyCheckInFormProps) {
    const [date, setDate] = useState(
        new Date().toISOString().split("T")[0]
    );
    const [cycleDay, setCycleDay] = useState("");
    const [bbt, setBbt] = useState("");
    const [mood, setMood] = useState("");
    const [energyLevel, setEnergyLevel] = useState("");
    const [sleepQuality, setSleepQuality] = useState("");
    const [notes, setNotes] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    const isEditing = checkinToEdit !== null;

    useEffect(() => {
        if (checkinToEdit) {
            setDate(checkinToEdit.date);
            setCycleDay(
                checkinToEdit.cycle_day !== null
                    ? String(checkinToEdit.cycle_day)
                    : ""
            );
            setBbt(
                checkinToEdit.bbt !== null
                    ? String(checkinToEdit.bbt)
                    : ""
            );
            setMood(checkinToEdit.mood ?? "");
            setEnergyLevel(checkinToEdit.energy_level ?? "");
            setSleepQuality(checkinToEdit.sleep_quality ?? "");
            setNotes(checkinToEdit.notes ?? "");
            setSuccessMessage("");
        }
    }, [checkinToEdit]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const token = sessionStorage.getItem("token");

        const checkInData = {
            date: date,
            cycle_day: cycleDay ? Number(cycleDay) : null,
            bbt: bbt ? Number(bbt) : null,
            mood: mood || null,
            energy_level: energyLevel || null,
            sleep_quality: sleepQuality || null,
            notes: notes || null,
        };

        try {
            const url = isEditing
                ? `http://localhost:8000/daily_checkins/${checkinToEdit.id}`
                : "http://localhost:8000/daily_checkins/checkin";

            const response = await fetch(url, {
                method: isEditing ? "PUT" : "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(checkInData),
            });

            if (!response.ok) {
                const errorData = await response.json();

                throw new Error(
                    errorData.detail ||
                    "Failed to save check-in data"
                );
            }

            if (isEditing) {
                setSuccessMessage("Check-in updated!");

                if (onEditComplete) {
                    onEditComplete();
                }
            } else {
                setSuccessMessage("Check-in saved!");

                onCheckInSaved();

                setDate(
                    new Date().toISOString().split("T")[0]
                );
                setCycleDay("");
                setBbt("");
                setMood("");
                setEnergyLevel("");
                setSleepQuality("");
                setNotes("");
            }
        } catch (error) {
            console.error(
                "Error during check-in submission:",
                error
            );
        }
    };

    return (
        <div>
            <h2>
                {isEditing
                    ? "Edit Check-In"
                    : "Daily Check-In"}
            </h2>

            <form onSubmit={handleSubmit}>
                <label>
                    Date:
                    <input
                        type="date"
                        value={date}
                        onChange={(e) =>
                            setDate(e.target.value)
                        }
                        required
                    />
                </label>

                <br />

                <label>
                    Cycle Day:
                    <input
                        type="number"
                        min="1"
                        value={cycleDay}
                        onChange={(e) =>
                            setCycleDay(e.target.value)
                        }
                    />
                </label>

                <br />

                <label>
                    BBT:
                    <input
                        type="number"
                        step="0.1"
                        value={bbt}
                        onChange={(e) =>
                            setBbt(e.target.value)
                        }
                    />
                </label>

                <br />

                <label>
                    Mood:
                    <select
                        value={mood}
                        onChange={(e) =>
                            setMood(e.target.value)
                        }
                    >
                        <option value="">
                            Select mood
                        </option>
                        <option value="Very Bad">
                            Very Bad
                        </option>
                        <option value="Bad">Bad</option>
                        <option value="OK">OK</option>
                        <option value="Good">
                            Good
                        </option>
                        <option value="Excellent">
                            Excellent
                        </option>
                    </select>
                </label>

                <br />

                <label>
                    Energy:
                    <select
                        value={energyLevel}
                        onChange={(e) =>
                            setEnergyLevel(e.target.value)
                        }
                    >
                        <option value="">
                            Select energy level
                        </option>
                        <option value="Very Low">
                            Very Low
                        </option>
                        <option value="Low">Low</option>
                        <option value="Moderate">
                            Moderate
                        </option>
                        <option value="High">High</option>
                        <option value="Very High">
                            Very High
                        </option>
                    </select>
                </label>

                <br />

                <label>
                    Sleep Quality:
                    <select
                        value={sleepQuality}
                        onChange={(e) =>
                            setSleepQuality(e.target.value)
                        }
                    >
                        <option value="">
                            Select sleep quality
                        </option>
                        <option value="Poor">
                            Poor
                        </option>
                        <option value="Fair">
                            Fair
                        </option>
                        <option value="Good">
                            Good
                        </option>
                        <option value="Very Good">
                            Very Good
                        </option>
                        <option value="Excellent">
                            Excellent
                        </option>
                    </select>
                </label>

                <br />

                <label>
                    Notes:
                    <textarea
                        value={notes}
                        onChange={(e) =>
                            setNotes(e.target.value)
                        }
                    />
                </label>

                <br />

                <button type="submit">
                    {isEditing
                        ? "Save Changes"
                        : "Save Check-In"}
                </button>
            </form>

            {successMessage && (
                <p>{successMessage}</p>
            )}
        </div>
    );
}

export default DailyCheckInForm;