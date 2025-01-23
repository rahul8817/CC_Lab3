from products import dao


class Product:
    def _init_(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data):
        return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])


def list_products() -> list[Product]:
    return [Product.load(product) for product in dao.list_products()]


def get_product(product_id: int) -> Product:
    product_data = dao.get_product(product_id)
    return Product.load(product_data) if product_data else None


def add_product(product: dict):
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    if qty < 0:
        raise ValueError("Quantity cannot be negative")
    dao.update_qty(product_id, qty)
