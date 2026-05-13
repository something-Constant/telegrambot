from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from pathlib import Path



# Get the current script's directory
current_dir = Path(__file__).parent

# Build database path
db_path = current_dir / "DataBase.sqlite3"

engine = create_async_engine(
    f"sqlite+aiosqlite:///{db_path}",
    echo=False,
)

# Create async engine
# engine = create_async_engine(
#     "sqlite+aiosqlite:///F:/Documents/VsCode/Telegram/Bot/database/DataBase.sqlite3",
#     echo=False,
# )

# Create async session factory
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

TableName = "Users"


class Users(Base):
    __tablename__ = TableName
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=True)


async def create_tables():
    """Create all tables in the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session() -> AsyncSession:
    """Get a database session"""
    async with Session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def search_user(
    username: Optional[str] = None, user_id: Optional[int] = None
) -> Optional[Users]:
    """Search for a user by username or ID"""
    async with Session() as session:
        query = select(Users)

        if user_id:
            query = query.where(Users.id == user_id)
        elif username:
            query = query.where(Users.username == username)
        else:
            return None

        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user


async def add_user(
    user_id: int, name: Optional[str] = None, username: Optional[str] = None
) -> Users:
    """Add a new user to the database"""
    async with Session() as session:
        query = select(Users)

        query = query.where(Users.id == user_id)

        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            user = Users(id=user_id, name=name, username=username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
        else:
            return user


async def remove_user(user_id: int) -> bool:
    """Remove a user by ID, returns True if user was removed"""
    async with Session() as session:
        # Find the user first
        result = await session.execute(select(Users).where(Users.id == user_id))
        user = result.scalar_one_or_none()

        if user:
            await session.delete(user)
            await session.commit()
            return True
        return False


async def get_all_users() -> list[Users]:
    """Get all users from the database"""
    async with Session() as session:
        result = await session.execute(select(Users))
        users = result.scalars().all()
        return list(users)


"""
# Example usage
async def main():
    # Create tables
    await create_tables()

    # Add a user
    new_user = await add_user(name="John Doe", username="johndoe", user_id=1111111)
    print(f"Added user: {new_user.name}, ID: {new_user.id}")

    # Search for user
    found_user = await search_user(username="johndoe")
    if found_user:
        print(f"Found user: {found_user.name}")

    # Get all users
    all_users = await get_all_users()
    print(f"Total users: {len(all_users)}")
    

    found_user = await search_user(user_id=551111)

    if found_user:
        # Remove user
        removed = await remove_user(found_user.id)
        if removed:
            print(f"User removed successfully")


# Run the example
if __name__ == "__main__":

    asyncio.run(main())
"""
