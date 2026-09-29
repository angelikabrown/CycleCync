import { useMemo, useState } from "react";
import type { DailyCheckIn } from "../types/DailyCheckin";

type CalendarProps = {
    checkins: DailyCheckIn[];
};

function Calendar({ checkins }: CalendarProps) {
    const today = new Date();

    const [currentMonth, setCurrentMonth] = useState(
        new Date(today.getFullYear(), today.getMonth(), 1)
    );

    const [selectedCheckIn, setSelectedCheckIn] =
        useState<DailyCheckIn | null>(null);

    const year = currentMonth.getFullYear();
    const month = currentMonth.getMonth();

    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const firstDayOfMonth = new Date(year, month, 1).getDay();

    const monthName = currentMonth.toLocaleString("default", {
        month: "long",
        year: "numeric",
    });

    const checkinsByDate = useMemo(() => {
        const map = new Map<string, DailyCheckIn>();

        checkins.forEach((checkin) => {
            map.set(checkin.date, checkin);
        });

        return map;
    }, [checkins]);

    const previousMonth = () => {
        setCurrentMonth(
            new Date(year, month - 1, 1)
        );
        setSelectedCheckIn(null);
    };

    const nextMonth = () => {
        setCurrentMonth(
            new Date(year, month + 1, 1)
        );
        setSelectedCheckIn(null);
    };

    const days = Array.from(
        { length: firstDayOfMonth + daysInMonth },
        (_, index) => {
            if (index < firstDayOfMonth) {
                return null;
            }

            return index - firstDayOfMonth + 1;
        }
    );

    return (
        <section className="rounded-xl bg-white p-4 shadow-sm">
            {/* Calendar Header */}
            <div className="mb-4 flex items-center justify-between">
                <button
                    onClick={previousMonth}
                    className="rounded-lg px-3 py-2 text-lg hover:bg-gray-100"
                    aria-label="Previous month"
                >
                    ←
                </button>

                <h2 className="text-lg font-semibold text-gray-900">
                    {monthName}
                </h2>

                <button
                    onClick={nextMonth}
                    className="rounded-lg px-3 py-2 text-lg hover:bg-gray-100"
                    aria-label="Next month"
                >
                    →
                </button>
            </div>

            {/* Weekday Headers */}
            <div className="mb-2 grid grid-cols-7 text-center text-xs font-medium text-gray-500">
                <div>Sun</div>
                <div>Mon</div>
                <div>Tue</div>
                <div>Wed</div>
                <div>Thu</div>
                <div>Fri</div>
                <div>Sat</div>
            </div>

            {/* Calendar Days */}
            <div className="grid grid-cols-7 gap-1">
                {days.map((day, index) => {
                    if (day === null) {
                        return <div key={index} />;
                    }

                    const dateString = `${year}-${String(
                        month + 1
                    ).padStart(2, "0")}-${String(day).padStart(
                        2,
                        "0"
                    )}`;

                    const checkin = checkinsByDate.get(dateString);

                    return (
                        <button
                            key={dateString}
                            onClick={() =>
                                checkin &&
                                setSelectedCheckIn(checkin)
                            }
                            disabled={!checkin}
                            className={`min-h-14 rounded-lg p-1 text-sm ${checkin
                                    ? "bg-gray-100 font-semibold hover:bg-gray-200"
                                    : "text-gray-500"
                                }`}
                        >
                            <div>{day}</div>

                            {checkin && (
                                <div className="mt-1 text-xs text-gray-600">
                                    CD {checkin.cycle_day ?? "—"}
                                </div>
                            )}
                        </button>
                    );
                })}
            </div>

            {/* Selected Check-in */}
            {selectedCheckIn && (
                <div className="mt-5 border-t pt-4">
                    <h3 className="font-semibold text-gray-900">
                        {selectedCheckIn.date}
                    </h3>

                    <p className="mt-1 text-sm text-gray-600">
                        Cycle Day{" "}
                        {selectedCheckIn.cycle_day ?? "—"}
                    </p>

                    <div className="mt-3 space-y-1 text-sm">
                        <p>
                            <strong>BBT:</strong>{" "}
                            {selectedCheckIn.bbt ?? "Not recorded"}
                        </p>

                        <p>
                            <strong>Mood:</strong>{" "}
                            {selectedCheckIn.mood ?? "Not recorded"}
                        </p>

                        <p>
                            <strong>Energy:</strong>{" "}
                            {selectedCheckIn.energy_level ??
                                "Not recorded"}
                        </p>

                        <p>
                            <strong>Sleep:</strong>{" "}
                            {selectedCheckIn.sleep_quality ??
                                "Not recorded"}
                        </p>

                        {selectedCheckIn.notes && (
                            <p>
                                <strong>Notes:</strong>{" "}
                                {selectedCheckIn.notes}
                            </p>
                        )}
                    </div>
                </div>
            )}
        </section>
    );
}

export default Calendar;