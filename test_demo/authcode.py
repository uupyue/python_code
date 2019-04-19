import time
import uuid

t = time.time()
uid = str(uuid.uuid4())
suid = ''.join(uid.split('-'))
a=(str(int(t))+'00123456'+suid)
print(a)



print(a[10:18])