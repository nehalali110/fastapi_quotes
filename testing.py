import re
import jwt
import secrets
from datetime import datetime, timedelta, timezone
# email_sample = "abc@xyz.japan"
# pattern_search = re.search(r"^\w+@\w+\.\w{2,3}$", email_sample)
# print(pattern_search)

# payload = {
# 	"email" : "johndoe@123.com",
# 	"user_id" : 3 
# }

# token = jwt.encode(payload, "secret", algorithm="HS256")
# print(f"JWT Token => {token}")
# data = jwt.decode(token, "secrett", algorithms="HS256")
# print(f"Original Data {data}")

# with open('.env', 'w') as f:
# 	f.write(f"JWT_SECRET={secrets.token_urlsafe()}")

print(datetime.now(timezone.utc))

