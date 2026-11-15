from sqlalchemy import ForeignKey, create_engine, Date
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker, Mapped, mapped_column
from datetime import date

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(default=date.today, nullable=False)
    end_date: Mapped[date | None] = mapped_column(nullable=True)

    # Relationships: A campaign contains multiple adventures
    adventures: Mapped[list["Adventure"]] = relationship(
        back_populates="campaign", cascade="all, delete-orphan"
    )

class Adventure(Base):
    __tablename__ = "adventures"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    campaign_id: Mapped[int] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False,
    )
    start_date: Mapped[date] = mapped_column(default=date.today, nullable=False)
    end_date: Mapped[date | None] = mapped_column(nullable=True)
    adventure_summary: Mapped[str] = mapped_column(
        default='A brief summary of the adventure\'s plot and key events.', nullable=True
    )

    # Relationships: An adventure belongs to a campaign, and contains multiple sessions
    campaign: Mapped["Campaign"] = relationship(back_populates="adventures")
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="adventure", cascade="all, delete-orphan"
    )

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    adventure_id: Mapped[int] = mapped_column(
        ForeignKey("adventures.id", ondelete="CASCADE"), nullable=False
    )
    adventure: Mapped["Adventure"] = relationship(back_populates="sessions")
    session_date: Mapped[date] = mapped_column(default=date.today, nullable=False)

    session_premise: Mapped[str | None] = mapped_column(
        default='A brief summary of the session\'s premise.', nullable=True
    )
    cold_opening: Mapped[str | None] = mapped_column(
        default='Read this to the players at the beginning of the session.',
        nullable=True
    )
    session_secrets: Mapped[str | None] = mapped_column(
        default='A list of secrets, hidden information, or plot twists relevant to this session.',
        nullable=True
    )
    other_notes: Mapped[str | None] = mapped_column(
        default='Any additional notes or information relevant to the session.',
        nullable=True
    )

    # Relationships: A session belongs to an adventure, and contains multiple scenes
    scenes: Mapped[list["Scene"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

class Scene(Base):
    __tablename__ = "scenes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    session: Mapped["Session"] = relationship(back_populates="scenes")
    quick_description: Mapped[str | None] = mapped_column(
        default='A one-sentence description of the scene.', nullable=True
    )
    long_description: Mapped[str | None] = mapped_column(
        default='A detailed description of the scene, including key events and interactions.',
        nullable=True
    )
    location: Mapped[str | None] = mapped_column(
        default='Where does this scene take place?', nullable=True
    )
    opening_narration: Mapped[str | None] = mapped_column(
        default='What is the opening narration for this scene?', nullable=True
    )
    party_goals: Mapped[str | None] = mapped_column(
        default='What does success look like here?', nullable=True
    )
    key_rewards: Mapped[str | None] = mapped_column(
        default='What can the party gain, learn, or win in this scene?', nullable=True
    )
    participants: Mapped[str | None] = mapped_column(
        default='A list of participants (NPCs, creatures, factions) and their roles in the scene.',
        nullable=True
    )
