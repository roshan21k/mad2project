from marshmallow import Schema, fields

# To send details in JSON serializable format

# User details
class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    role = fields.String()

#Product details
class ProductSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Float()
    uom = fields.String()
    stock = fields.Integer()
    ratings_sum =fields.Integer()
    ratings_average = fields.Float()
    ratings_count =fields.Integer()
    description =fields.String()

# Category details
class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    products = fields.Nested(ProductSchema, many=True)

# Cart Details
class CartSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    quantity = fields.Integer()
    product_id = fields.Integer()
    product = fields.Nested(ProductSchema)
    added_on = fields.DateTime(format="%d-%m-%Y")

# Order Detail
class OrderSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    total = fields.Float()
    ordered_on = fields.DateTime(format="%d-%m-%Y %H:%M:%S")

# Order Details (More Info)
class OrderDetailsSchema(Schema):
    id = fields.Integer()
    product_id = fields.Integer()
    product_name = fields.String()
    product_price = fields.Float()
    product_uom = fields.String()
    quantity = fields.Integer()

# Review or Comment under product
class ReviewSchema(Schema):
    id = fields.Integer()
    product_id = fields.Integer()
    username = fields.String()
    comment = fields.String()
    rating = fields.Float()

# User role requests sent for approval
class RequestSchema(Schema):
    id = fields.Integer()
    role = fields.String()
    status = fields.String()
    user = fields.Nested(UserSchema)

# Category requests sent for approval
class CategoryRequestSchema(Schema):
    id = fields.Integer()
    action = fields.String()
    name = fields.String()
    status = fields.String()
    old_name = fields.String()
    user = fields.Nested(UserSchema)

# product requests sent for approval
class ProductRequestSchema(Schema):
    id = fields.Integer()
    action = fields.String()
    status = fields.String()
    new_name = fields.String()
    new_desc = fields.String()
    new_uom = fields.String()
    new_price = fields.Integer()
    new_stock = fields.Integer()
    user = fields.Nested(UserSchema)
    # category = fields.Nested(CategorySchema)
    product = fields.Nested(ProductSchema)