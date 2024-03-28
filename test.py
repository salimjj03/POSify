#!/usr/bin/python3


from models.withdraw import Withdraw
from models.user import User
from models import storage

print(storage.delete("User", "eff609f3-1481-4121-9445-6c389f5bd563"))
