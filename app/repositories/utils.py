from datetime import datetime, timedelta

from sqlalchemy import func, select

from app.models.boards_state_history import BoardStateHistory, EventType


def get_latest_status():
    latest_status_cte = (
        select(
            BoardStateHistory.id.label("id"),
            BoardStateHistory.board_id.label("board_id"),
            BoardStateHistory.status.label("status"),
            BoardStateHistory.event.label("event"),
            BoardStateHistory.created_at.label("created_at"),
            func.row_number().over(
                partition_by=BoardStateHistory.board_id,
                order_by=BoardStateHistory.created_at.desc()
            ).label("rn")
        )
        .select_from(BoardStateHistory)
        .cte(name="latest_status")
    )
    return latest_status_cte


def get_latest_state_event():
    latest_state_cte = (
        select(
            BoardStateHistory.id.label("id"),
            BoardStateHistory.board_id.label("board_id"),
            BoardStateHistory.status.label("status"),
            BoardStateHistory.event.label("event"),
            BoardStateHistory.created_at.label("created_at"),
            func.row_number()
            .over(
                partition_by=BoardStateHistory.board_id,
                order_by=BoardStateHistory.created_at.desc()
            )
            .label("rn")
        )
        .select_from(BoardStateHistory)
        .where(BoardStateHistory.event == EventType.STATE)
        .cte("latest_state")
    )
    return latest_state_cte