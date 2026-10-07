from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.cycle_metrics_schema import CycleMetricsResponse
from app.utils.auth import get_current_user
from app.services.cycle_metrics_service import get_cycle_metrics


router = APIRouter(
    prefix="/cycle-metrics",
    tags=["Cycle Metrics"],
)


@router.get("/", response_model=CycleMetricsResponse)
def cycle_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_cycle_metrics(db, current_user)