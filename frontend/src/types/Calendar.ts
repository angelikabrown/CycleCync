export type CalendarDay = {
    date: string;
    cycle_day: number | null;
    period: boolean;
    checkin: {
        id: number;
        date: string;
        cycle_day: number | null;
        period: boolean;
        bbt: number | null;
        mood: string | null;
        energy_level: string | null;
        sleep_quality: string | null;
        notes: string | null;
    } | null;
};