from database import db

class Category(db.Model):
	__tablename__ = 'categories'

	category = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
	categoryname = db.Column(db.String(50), nullable=False)

t_cust_hist = db.Table(
	'cust_hist',
	db.Column('customerid', db.ForeignKey('customers.customerid', ondelete='CASCADE'), nullable=False,index=True),
	db.Column('orderid', db.Integer, nullable=False),
	db.Column('prod_id', db.Integer, nullable=False))


class Customer(db.Model):
	__tablename__ = 'customers'

	customerid = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
	firstname = db.Column(db.String(50), nullable=False)
	lastname = db.Column(db.String(50), nullable=False)
	address1 = db.Column(db.String(50), nullable=False)
	address2 = db.Column(db.String(50))
	city = db.Column(db.String(50), nullable=False)
	state = db.Column(db.String(50))
	zip = db.Column(db.Integer)
	country = db.Column(db.String(50), nullable=False)
	region = db.Column(db.SmallInteger, nullable=False)
	email = db.Column(db.String(50))
	phone = db.Column(db.String(50))
	creditcardtype = db.Column(db.Integer, nullable=False)
	creditcard = db.Column(db.String(50), nullable=False)
	creditcardexpiration = db.Column(db.String(50), nullable=False)
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(50), nullable=False)
	age = db.Column(db.SmallInteger)
	income = db.Column(db.Integer)
	gender = db.Column(db.String(1))
	version_id= db.Column(db.Integer, default=0)
	beingedited = db.Column(db.Boolean, default=False)

	def _asdict(self):
		return {
			"id": self.customerid,
			"firstname": self.firstname,
			"lastname": self.lastname,
			"address1": self.address1,
			"address2": self.address2,
			"city": self.city,
			"state": self.state,
			"zip": self.zip,
			"country": self.country,
			"region": self.region,
			"email": self.email,
			"phone": self.phone,
			"creditcardtype": self.creditcardtype,
			"creditcard": self.creditcard,
			"creditcardexpiration": self.creditcardexpiration,
			"username": self.username,
			"password": self.password,
			"age": self.age,
			"income": self.income,
			"gender": self.gender,
			"version_id": self.version_id
		}


class Inventory(db.Model):
	__tablename__ = 'inventory'

	prod_id = db.Column(db.Integer, primary_key=True)
	quan_in_stock = db.Column(db.Integer, nullable=False)
	sales = db.Column(db.Integer, nullable=False)

	def _asdict(self):
		return {
			"prod_id": self.prod_id,
			"quan_in_stock": self.quan_in_stock,
			"sales": self.sales
		}


t_orderlines = db.Table(
	'orderlines',
	db.Column('orderlineid', db.Integer, nullable=False),
	db.Column('orderid', db.ForeignKey('orders.orderid', ondelete='CASCADE'), nullable=False),
	db.Column('prod_id', db.ForeignKey('products.prod_id'), nullable=False),
	db.Column('quantity', db.SmallInteger, nullable=False),
	db.Column('orderdate', db.Date, nullable=False),
	db.Index('ix_orderlines_orderid', 'orderid', 'orderlineid'))


class Order(db.Model):
	__tablename__ = 'orders'

	orderid = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
	orderdate = db.Column(db.Date, nullable=False)
	customerid = db.Column(db.ForeignKey('customers.customerid', ondelete='SET NULL'), index=True)
	netamount = db.Column(db.Numeric(12, 2), nullable=False)
	tax = db.Column(db.Numeric(12, 2), nullable=False)
	totalamount = db.Column(db.Numeric(12, 2), nullable=False)

	customer = db.relationship('Customer', primaryjoin='Order.customerid == Customer.customerid', backref='orders')
	items = db.relationship('Product', secondary=t_orderlines, backref="orderid")

	def _asdict(self):
		return {
			"orderid": self.orderid,
			"orderdate": self.orderdate,
			"customerid": self.customerid,
			"netamount": self.netamount,
			"tax": self.tax,
			"totalamount": self.totalamount,
			"items": self.items
		}


class Product(db.Model):
	__tablename__ = 'products'

	prod_id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
	category = db.Column(db.Integer, nullable=False, index=True)
	title = db.Column(db.String(50), nullable=False)
	actor = db.Column(db.String(50), nullable=False)
	price = db.Column(db.Numeric(12, 2), nullable=False)
	special = db.Column(db.SmallInteger, index=True)
	common_prod_id = db.Column(db.Integer, nullable=False)

	def _asdict(self):
		return {
			"prod_id": self.prod_id,
			"category": self.category,
			"title": self.title,
			"actor": self.actor,
			"price": self.price,
			"special": self.special,
			"common_prod_id": self.common_prod_id
		}


t_reorder = db.Table(
	'reorder',
	db.Column('prod_id', db.Integer, nullable=False),
	db.Column('date_low', db.Date, nullable=False),
	db.Column('quan_low', db.Integer, nullable=False),
	db.Column('date_reordered', db.Date),
	db.Column('quan_reordered', db.Integer),
	db.Column('date_expected', db.Date))
