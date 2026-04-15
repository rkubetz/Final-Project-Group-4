from . import orders, order_details, menu_items, recipes, resources, payment_info


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(menu_items.router)
    app.include_router(recipes.router)
    app.include_router(resources.router)
    app.include_router(payment_info.router)
