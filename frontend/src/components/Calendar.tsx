import { useEffect, useState } from "react";
import type { CalendarDay } from "../types/Calendar";

function Calendar() {
    const today = new Date();

    const [currentMonth, setCurrentMonth] = useState(
        new Date(today.getFullYear(), today.getMonth(), 1)
    );

    const [calendarDays, setCalendarDays] = useState<CalendarDay[]>([]);
    const [selectedDay, setSelectedDay] = useState<CalendarDay | null>(null);

    const year = currentMonth.getFullYear();
    const month = currentMonth.getMonth();

    const monthName = currentMonth.toLocaleString("default", {
        month: "long",
        year: "numeric",
    });

    useEffect(() => {
        const token = sessionStorage.getItem("token");

        const apiMonth = month + 1;

        fetch(
            `http://localhost:8000/calendar/?year=${year}&month=${apiMonth}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                return response.json();
            })
            .then((data) => {
                setCalendarDays(data);
            })
            .catch((error) => {
                console.error("Calendar fetch error:", error);
            });
    }, [year, month]);

    const previousMonth = () => {
        setCurrentMonth(new Date(year, month - 1, 1));
        setSelectedDay(null);
    };

    const nextMonth = () => {
        setCurrentMonth(new Date(year, month + 1, 1));
        setSelectedDay(null);
    };

    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDayOfMonth = new Date(year, month, 1).getDay();

    const calendarDaysByDate = new Map(
        calendarDays.map((day) => [day.date, day])
    );

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

            <div className="mb-2 grid grid-cols-7 text-center text-xs font-medium text-gray-500">
                <div>Sun</div>
                <div>Mon</div>
                <div>Tue</div>
                <div>Wed</div>
                <div>Thu</div>
                <div>Fri</div>
                <div>Sat</div>
            </div>

            <div className="grid grid-cols-7 gap-1">
                {days.map((day, index) => {
                    if (day === null) {
                        return <div key={index} />;
                    }

                    const dateString = `${year}-${String(month + 1).padStart(
                        2,
                        "0"
                    )}-${String(day).padStart(2, "0")}`;

                    const calendarDay = calendarDaysByDate.get(dateString);

                    return (
                        <button
                            key={dateString}
                            onClick={() =>
                                calendarDay && setSelectedDay(calendarDay)
                            }
                            className={`min-h-14 rounded-lg p-1 text-sm ${calendarDay?.period
                                    ? "bg-[#F2D0B5] font-semibold text-[#8A4B2A] hover:bg-[#E8C09F]"
                                    : calendarDay?.checkin
                                        ? "bg-gray-100 font-semibold hover:bg-gray-200"
                                        : "text-gray-500 hover:bg-gray-50"
                                }`}
                        >
                            <div>{day}</div>

                            {calendarDay && (
                                <div
                                    className={`mt-1 text-xs ${calendarDay.period
                                            ? "text-amber-800"
                                            : "text-gray-600"
                                        }`}
                                >
                                    CD {calendarDay.cycle_day ?? "—"}
                                </div>
                            )}
                        </button>
                    );
                })}
            </div>

            {selectedDay && (
                <div className="mt-5 border-t pt-4">
                    <h3 className="font-semibold text-gray-900">
                        {selectedDay.date}
                    </h3>

                    <p className="mt-1 text-sm text-gray-600">
                        Cycle Day {selectedDay.cycle_day ?? "—"}
                    </p>

                    {selectedDay.checkin ? (
                        <div className="mt-3 space-y-1 text-sm">
                            <p>
                                <strong>BBT:</strong>{" "}
                                {selectedDay.checkin.bbt ?? "Not recorded"}
                            </p>

                            <p>
                                <strong>Mood:</strong>{" "}
                                {selectedDay.checkin.mood ?? "Not recorded"}
                            </p>

                            <p>
                                <strong>Energy:</strong>{" "}
                                {selectedDay.checkin.energy_level ??
                                    "Not recorded"}
                            </p>

                            <p>
                                <strong>Sleep:</strong>{" "}
                                {selectedDay.checkin.sleep_quality ??
                                    "Not recorded"}
                            </p>

                            {selectedDay.checkin.notes && (
                                <p>
                                    <strong>Notes:</strong>{" "}
                                    {selectedDay.checkin.notes}
                                </p>
                            )}
                        </div>
                    ) : (
                        <p className="mt-3 text-sm text-gray-500">
                            No check-in recorded for this day.
                        </p>
                    )}
                </div>
            )}
        </section>
    );
}

export default Calendar;