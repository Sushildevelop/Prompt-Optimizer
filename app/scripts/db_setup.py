import asyncio
from app.core.database import connect_to_mongo, close_mongo_connection
from app.models.user import User
from app.utils.logger import app_logger


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        await connect_to_mongo()
        
        print("Creating database indexes...")
        
        # User indexes
        await User.create_indexes()
        print("User indexes created")
        
        
        print("All database indexes created successfully!")
        
    except Exception as e:
        print(f"Error creating indexes: {str(e)}")
        app_logger.error(f"Failed to create indexes: {str(e)}")
        raise
    finally:
        await close_mongo_connection()


async def check_database_connection():
    """Check database connection and collections"""
    try:
        await connect_to_mongo()
        
        print("Checking database connection...")
        
        # Check collections
        user_count = await User.find().count()
    
        print(f"Database connection successful!")
        print(f"Database Statistics:")
        print(f"  Users: {user_count}")
        
        return True
        
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        app_logger.error(f"Database connection failed: {str(e)}")
        return False
    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python -m app.scripts.db_setup indexes")
        print("  python -m app.scripts.db_setup check")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "indexes":
        asyncio.run(create_indexes())
    elif command == "check":
        asyncio.run(check_database_connection())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)