import os

src = "src"
web = src + "/web"
entity = src + "/entity/"
service = src + "/service/"
serviceImpl = service + "impl/"
repository = src + "/repository/"
dto = web + "/dto/"
controller = web + "/controller/"
mapper = web + "/mapper/"

def generateProject():
    if not os.path.exists(src):
        os.makedirs(src)
    if not os.path.exists(entity):
        os.makedirs(entity)
    if not os.path.exists(service):
        os.makedirs(service)
    if not os.path.exists(serviceImpl):
        os.makedirs(serviceImpl)
    if not os.path.exists(repository):
        os.makedirs(repository)
    if not os.path.exists(web):
        os.makedirs(web)
    if not os.path.exists(dto):
        os.makedirs(dto)
    if not os.path.exists(controller):
        os.makedirs(controller)
    if not os.path.exists(mapper):
        os.makedirs(mapper)
        
    print(">> Project structure generated!\n")