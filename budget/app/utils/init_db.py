from ..domain.configs import DEFAULT_CATEGORIES, ADMIN_USER_ID
from ..infrastructure.database.models import Category
from sqlalchemy import text

async def init_db(db):
    """Create default categories for all users"""
    try:
        query = text('SELECT COUNT(*) FROM categories WHERE user_id= :admin_id')
        result = await db.execute(query, {'admin_id': ADMIN_USER_ID})
        count = result.scalar()
        if count > 0:
            return

        for category_type, categories in DEFAULT_CATEGORIES.items():
            for category_name, category_data in categories.items():
                main_category = Category(
                    name=category_name,
                    type=category_type,
                    user_id=ADMIN_USER_ID,
                    favicon=category_data["favicon"]
                )
                db.add(main_category)
                await db.flush()
                for sub in category_data["subcategories"]:
                    subcategory = Category(
                        name=sub["name"],
                        type=category_type,
                        user_id=ADMIN_USER_ID,
                        parent_category_id=main_category.id,
                        favicon=sub["favicon"]
                    )
                    db.add(subcategory)
    
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
