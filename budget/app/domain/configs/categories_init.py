from uuid import UUID
from ...domain.schemas.category import CategoryType

ADMIN_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

DEFAULT_CATEGORIES = {
    CategoryType.EXPENSE: {
        "Housing": {
            "favicon": "home",
            "subcategories": [
                {"name": "Rent/Mortgage", "favicon": "key"},
                {"name": "Utilities", "favicon": "bolt"},
                {"name": "Maintenance/Repairs", "favicon": "tools"},
                {"name": "Insurance", "favicon": "shield"},
                {"name": "Property Tax", "favicon": "file-invoice-dollar"}
            ]
        },
        "Food": {
            "favicon": "utensils",
            "subcategories": [
                {"name": "Groceries", "favicon": "shopping-cart"},
                {"name": "Restaurants/Dining Out", "favicon": "restaurant"},
                {"name": "Cafe/Coffee Shops", "favicon": "coffee"},
                {"name": "Food Delivery", "favicon": "truck"},
                {"name": "Snacks", "favicon": "cookie-bite"}
            ]
        },
        "Transportation": {
            "favicon": "car",
            "subcategories": [
                {"name": "Fuel/Gas", "favicon": "gas-pump"},
                {"name": "Public Transit", "favicon": "bus"},
                {"name": "Car Maintenance", "favicon": "wrench"},
                {"name": "Parking", "favicon": "parking"},
                {"name": "Car Insurance", "favicon": "car-crash"}
            ]
        },
        "Personal Care": {
            "favicon": "heart",
            "subcategories": [
                {"name": "Healthcare", "favicon": "hospital"},
                {"name": "Gym/Fitness", "favicon": "dumbbell"},
                {"name": "Personal Grooming", "favicon": "cut"},
                {"name": "Clothing", "favicon": "tshirt"},
                {"name": "Medical Insurance", "favicon": "briefcase-medical"}
            ]
        },
        "Lifestyle": {
            "favicon": "smile",
            "subcategories": [
                {"name": "Entertainment", "favicon": "film"},
                {"name": "Subscriptions", "favicon": "tv"},
                {"name": "Hobbies", "favicon": "gamepad"},
                {"name": "Travel", "favicon": "plane"},
                {"name": "Education", "favicon": "graduation-cap"}
            ]
        }
    },
    CategoryType.INCOME: {
        "Regular Income": {
            "favicon": "wallet",
            "subcategories": [
                {"name": "Salary/Wages", "favicon": "money-bill"},
                {"name": "Bonuses", "favicon": "gift"},
                {"name": "Overtime", "favicon": "clock"}
            ]
        },
        "Additional Income": {
            "favicon": "plus-circle",
            "subcategories": [
                {"name": "Refunds", "favicon": "undo"},
                {"name": "Investment Income", "favicon": "chart-line"},
                {"name": "Side Hustle", "favicon": "briefcase"},
                {"name": "Rental Income", "favicon": "house-user"}
            ]
        }
    }
}
