/src/usecases/
│
├── __init__.py  # (deve ter algo aqui????)
│
├── auth/
│   ├── __init__.py
│   ├── login_use_case.py            # (Classe: LoginUseCase) (ok)
│   └── get_authenticated_user.py  # (Classe: GetAuthenticatedUserUseCase) (ok)
│
├── waiter/
│   ├── __init__.py
│   ├── list_tables_use_case.py        # (Classe: ListTablesUseCase) (ok)
│   ├── open_table_use_case.py         # (Classe: OpenTableUseCase)  (ok)
│   ├── get_table_details_use_case.py  # (Classe: GetTableDetailsUseCase) (ok)
│   ├── create_order_use_case.py       # (Classe: CreateOrderUseCase) (ok)
│   ├── add_item_to_order_use_case.py  # (Classe: AddItemToOrderUseCase) (ok)
│   └── close_table_use_case.py        # (Classe: CloseTableUseCase) (ok)
│
├── kitchen/
│   ├── __init__.py
│   ├── list_pending_orders_use_case.py  # (Classe: ListPendingOrdersUseCase) (ok)
│   ├── start_order_preparation.py     # (Classe: StartOrderPreparationUseCase)  (ok)
│   └── complete_order_preparation.py  # (Classe: CompleteOrderPreparationUseCase) (ok)
│
└── admin/
    ├── __init__.py
    ├── create_product_use_case.py   # (Classe: CreateProductUseCase) (ok)
    ├── update_product_use_case.py   # (Classe: UpdateProductUseCase) (ok)
    ├── list_all_products_use_case.py  # (Classe: ListAllProductsUseCase) (ok)
    ├── create_user_use_case.py      # (Classe: CreateUserUseCase) (ok)
    └── update_user_use_case.py      # (Classe: UpdateUserUseCase) (ok)