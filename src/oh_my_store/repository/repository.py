# class ProductDAO:
#     def __init__(self, session: AsyncSession):
#         super().__init__(Product, session)

#     async def get_all_available(self, limit: int, offset: int) -> list[Product]:
#         pass

#     async def create(self) -> Product | None:
#         pass

#     async def update_stock_by_id(self, amount: int):
#         pass


# class SupplierDao:

#     def __init__(self, session: AsyncSession):
#         super().__init__(Supplier, session)

#     async def create(self, **Kwargs) -> Supplier:
#         pass

#     async def update_address_by_id(self, client_id: UUID, address: Address):
#         pass


# class ImageDAO:

#     def __init__(self, session: AsyncSession):
#         super().__init__(Image, session)

#     async def get_image_by_product_id(self, product_id: UUID) -> Image | None:
#         pass

#     async def create(self, **kwargs) -> Image | None:
#         pass

#     async def update(self, image_id: UUID):
#         pass
