from pydantic import BaseModel


class CycleMetricsResponse(BaseModel):
    cycles_tracked: int
    completed_cycles: int

    average_cycle_length: float | None
    shortest_cycle_length: int | None
    longest_cycle_length: int | None

    average_period_length: float | None
    shortest_period_length: int | None
    longest_period_length: int | None