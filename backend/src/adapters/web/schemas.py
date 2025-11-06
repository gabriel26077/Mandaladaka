# src/adapters/web/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Importa os Enums do domínio para validação
# (Assumindo que domain/__init__.py exporta todos eles)
from domain import UserRole, OrderStatus, TableStatus

# ==================================================
# Schemas de Produto (para o Admin)
# ==================================================

class ProductBase(BaseModel):
    """Schema base para produto, com campos comuns."""
    name: str = Field(..., min_length=3, description="Nome do produto")
    price: float = Field(..., gt=0, description="Preço deve ser maior que zero")
    availability: bool = True
    category: str
    imageUrl: str
    visibility: bool = True

class ProductCreateSchema(ProductBase):
    """Schema para validar o JSON de ENTRADA ao criar um produto."""
    pass

class ProductUpdateSchema(BaseModel):
    """Schema para validar o JSON de ENTRADA ao atualizar um produto."""
    name: Optional[str] = Field(None, min_length=3)
    price: Optional[float] = Field(None, gt=0)
    availability: Optional[bool] = None
    category: Optional[str] = None
    imageUrl: Optional[str] = None
    visibility: Optional[bool] = None

class ProductResponseSchema(ProductBase):
    """Schema para formatar o JSON de SAÍDA de um produto."""
    id: int
    
    class Config:
        from_attributes = True 

# ==================================================
# Schemas de Usuário
# ==================================================

class UserBase(BaseModel):
    """Schema base para usuário."""
    username: str = Field(..., min_length=4)
    name: str
    
class UserCreateSchema(UserBase):
    """Schema para validar o JSON de ENTRADA ao criar um usuário."""
    password: str = Field(..., min_length=6)
    roles: List[UserRole] = Field(..., min_length=1)

class UserUpdateSchema(BaseModel):
    """Schema para validar o JSON de ENTRADA ao atualizar um usuário."""
    username: Optional[str] = Field(None, min_length=4)
    name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)
    roles: Optional[List[UserRole]] = Field(None, min_length=1)

class UserResponseSchema(UserBase):
    """Schema para formatar o JSON de SAÍDA de um usuário."""
    id: int
    roles: List[UserRole]
    
    class Config:
        from_attributes = True

# ==================================================
# Schemas de Autenticação
# ==================================================

class LoginSchema(BaseModel):
    """Schema para validar o JSON de ENTRADA do /login."""
    username: str
    password: str

class TokenResponseSchema(BaseModel):
    """Schema para formatar o JSON de SAÍDA do /login."""
    access_token: str
    token_type: str = "bearer"

# ==================================================
# Schemas de Pedido (Order) e Itens
# ==================================================

class ProductInOrderSchema(BaseModel):
    """Schema de SAÍDA para um Produto DENTRO de um pedido."""
    id: int
    name: str
    price: float
    
    class Config:
        from_attributes = True

class ItemOrderResponseSchema(BaseModel):
    """Schema de SAÍDA para um ItemOrder."""
    product: ProductInOrderSchema
    quantity: int
    total_price: float
    
    class Config:
        from_attributes = True

class OrderResponseSchema(BaseModel):
    """Schema para formatar o JSON de SAÍDA de um Pedido (Order)."""
    id: int
    table_number: int
    status: OrderStatus
    created_at: datetime
    items: List[ItemOrderResponseSchema]
    total_price: float
    
    class Config:
        from_attributes = True

# --- Schemas de ENTRADA (para o waiter_router) ---

class CreateOrderItemSchema(BaseModel):
    """Schema de ENTRADA para um item ao criar um pedido."""
    product_id: int = Field(..., gt=0)
    quantity: int = Field(1, gt=0)

class CreateOrderSchema(BaseModel):
    """Schema de ENTRADA para criar um novo pedido."""
    items: List[CreateOrderItemSchema] = Field(..., min_length=1)

class AddItemToOrderSchema(CreateOrderItemSchema):
    """Schema de ENTRADA para adicionar um item a um pedido existente."""
    pass

# ==================================================
# Schemas de Mesa (Table)
# ==================================================

class OpenTableSchema(BaseModel):
    """Schema de ENTRADA para abrir uma mesa."""
    number_of_people: int = Field(..., gt=0, description="Nro de pessoas deve ser > 0")

class TableResponseSchema(BaseModel):
    """Schema de SAÍDA para a lista de mesas (visão "rasa")."""
    id: int
    status: TableStatus
    number_of_people: int
    
    class Config:
        from_attributes = True

class TableDetailsResponseSchema(TableResponseSchema):
    """Schema de SAÍDA para os detalhes de UMA mesa (visão "profunda")."""
    orders: List[OrderResponseSchema]
    total_bill: float
    
    class Config:
        from_attributes = True