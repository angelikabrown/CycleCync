export type DailyCheckIn = {
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