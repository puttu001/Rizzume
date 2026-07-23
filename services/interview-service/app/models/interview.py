import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import DEFAULT_QUESTION_COUNT
from app.db.base import Base


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # From the JWT's `sub` claim (via X-User-Id) — no FK, auth_db is a
    # different database owned by a different service.
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="in_progress")
    current_difficulty: Mapped[str] = mapped_column(String(16), nullable=False, default="medium")
    question_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Decided once per-interview by the engine (resume + role informed),
    # not a single global constant — see core/constants.py for the bounds.
    max_questions: Mapped[int] = mapped_column(
        Integer, nullable=False, default=DEFAULT_QUESTION_COUNT
    )
    # Extracted resume text, kept on the row so every engine call throughout
    # the interview (not just the opening question) can reference it.
    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    # Reference into Azure Blob Storage (rizzume-resumes container) for the
    # original uploaded PDF — not the extracted text, the source file.
    resume_blob_name: Mapped[str] = mapped_column(String(512), nullable=False)
    feedback: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)