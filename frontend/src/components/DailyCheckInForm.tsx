import { useState } from "react";

function DailyCheckInForm() {
    const [date, setDate] = useState("");
    const [cycleDay, setCycleDay] = useState("");
    const [bbt, setBbt] = useState("");
    const [mood, setMood] = useState("");
    const [energyLevel, setEnergyLevel] = useState("");
    const [sleepQuality, setSleepQuality] = useState("");
    const [notes, setNotes] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // We'll add the API request here next.
    };

    return (
        <div>
            <h2>Daily Check-In</h2>

            <form onSubmit={handleSubmit}>
                <label>
                    Date:
                    <input
                        type="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                    />
                </label>

                <br />

                <label>
                    Cycle Day:
                    <input
                        type="number"
                        value={cycleDay}
                        onChange={(e) => setCycleDay(e.target.value)}
                    />
                </label>

                <br />

                <label>
                    BBT:
                    <input
                        type="number"
                        step="0.1"
                        value={bbt}
                        onChange={(e) => setBbt(e.target.value)}
                    />
                </label>

                <br />

                <label>
                    Mood:
                    <input
                        type="text"
                        value={mood}
                        onChange={(e) => setMood(e.target.value)}
                    />
                </label>

                <br />

                <label>
                    Energy:
                    <input
                        type="text"
                        value={energyLevel}
                        onChange={(e) => setEnergyLevel(e.target.value)}
                    />
                </label>

                <br />

                <label>
                    Sleep Quality:
                    <input
                        type="text"
                        value={sleepQuality}
                        onChange={(e) => setSleepQuality(e.target.value)}
                    />
                </label>

                <br />

                <label>
                    Notes:
                    <textarea
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                    />
                </label>

                <br />

                <button type="submit">Save Check-In</button>
            </form>
        </div>
    );
}

export default DailyCheckInForm;