# src/domain/__init__.py

# Exporta modelos e enums
from domain.models import (  # <-- Make sure this line is exactly 'from domain.models import ...'
    User, UserRole, Product, ItemOrder, Order, OrderStatus, Table, TableStatus
)

# Exporta exceções
from domain.exceptions import (
    DomainException, InvalidCredentialsException, UserNotFoundException,
    ProductNotFoundException, TableNotFoundException, OrderNotFoundException,
    BusinessRuleException
)

# Exporta ports (interfaces)
from domain.ports.user_repository import UserRepositoryPort
from domain.ports.product_repository import ProductRepositoryPort
from domain.ports.order_repository import OrderRepositoryPort
from domain.ports.table_repository import TableRepositoryPort
from domain.ports.password_hasher import PasswordHasherPort
from domain.ports.token_generator import TokenGeneratorPort