from saleapp import admin, db
from saleapp.models import User, Product, CartItem, Cart
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(CartItem, db.session))
admin.add_view(ModelView(Cart, db.session))
