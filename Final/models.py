class User(db.Model):
    id = db.Column(db.Integer, unique=True,autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(128))

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password_hash = pbkdf2_sha256.hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Users(db.Model):
	idusers       = db.Column(db.Integer, unique=True,autoincrement=True, primary_key=True)
	username      = db.Column(db.String(45), unique=True)
	password      = db.Column(db.String(45), unique=True)
	first_name    = db.Column(db.String(45), unique=True)
	last_name     = db.Column(db.String(45), unique=True)
	email_address = db.Column(db.String(45), unique=True)
	def __init__(self,username,password,first_name,last_name,email_address):
		self.username 	   = username
		self.passowrd	   = pbkdf2_sha256.hash(password)
		self.first_name	   = first_name
		self.last_name 	   = last_name
		self.email_address = email_address
	def __repr__(self):
		return '<Users {}>'.format(self.username)


class Bookmarks(db.Model):
	bookmark_id = db.Column(db.Integer,primary_key=True)
	home 		= db.Column(db.Integer)
	user        = db.Column(db.Integer)
	def __init__(bookmark_id,home,user):
		self.bookmark_id=bookmark_id
		self.home=home
		self.user=user
	def __repr__(self):
		return '<Bookmarks {}>'.format(self.bookmark_id)


class Features(db.Model):
	entryid 	 = db.Column(db.Integer,primary_key=True)
	house 		 = db.Column(db.Integer)
	feature_type = db.Column(db.String(30))
	def __init__(entryid,house,feature_type):
		self.entryid=entryid
		self.house=house
		self.feature_type=feature_type
	def __repr__(self):
		return '<Features {}>'.format(self.entryid)


class Seller(db.Model):
	seller_id		= db.Column(db.Integer,primary_key=True)
	phone_num		= db.Column(db.String(12))
	email 			= db.Column(db.String(70))
	seller_fname	= db.Column(db.String(30))
	seller_lname 	= db.Column(db.String(30))
	def __init__(seller_id,phone_num,email,seller_fname,seller_lname):
		self.seller_id 		= seller_id
		self.phone_num 		= phone_num
		self.email 			= email
		self.seller_fname 	= seller_fname
		self.seller_lname 	= seller_lname
	def __repr__(self):
		return '<Seller {}>'.format(self.seller_id)

class Home(db.Model):
	hid				= db.Column(db.Integer,primary_key=True)
	address 		= db.Column(db.String(40))
	home_type		= db.Column(db.String(40))
	acres			= db.Column(db.Numeric())
	construct_date	= db.Column(db.String(10))
	cost 			= db.Column(db.Float)
	seller 			= db.Column(db.Integer)
	def __init__(hid,address,home_type,acres,construct_date,cost,seller):
		self.hid 			= hid
		self.address     	= address
		self.home_type 		= home_type
		self.acres 			= acres
		self.construct_date = construct_date
		self.cost 			= cost
		self.seller 		= seller
	def __repr__(self):
		return '<Home {}>'.format(self.hid)


class Room(db.Model):
	house		 = db.Column(db.Integer)
	room_type	 = db.Column(db.String(15))
	amount 		 = db.Column(db.Integer)
	entryid		 = db.Column(db.Integer,primary_key=True)
	def __init__(house,room_type,amount,entryid):
		self.house		 = house
		self.room_type	 = room_type
		self.amount		 = amount
		self.entryid	 = entryid
	def __repr__(self):
		return '<Room {}>'.format(self.entryid)




class Utilities(db.Model):
	entryid 	= db.Column(db.Integer,primary_key=True)
	house 		= db.Column(db.Integer)
	util_type	= db.Column(db.String(15))
	def __init__(entryid,house,util_type):
		self.entryid 	= entryid
		self.house 		= house
		self.util_type  = util_type
	def __repr__(self):
		return '<Utilities {}>'.format(self.entryid)