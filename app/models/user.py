class UserModel(object):
    def __init__(self, user: dict):
        self.id = user.get('id')
        self.name = user.get('name')
        self.email = user.get('email')
        self.phone = user.get('phone')
        self.age = user.get('age')
        self.creation_date = user.get('creation_date')
        self.update_date = user.get('update_date')
    
    def validate(self):
        if None in (self.name, self.email, self.phone, self.age):
            return False
        
        return True
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'age': self.age,
            'creation_date': self.creation_date,
            'update_date': self.update_date
        }