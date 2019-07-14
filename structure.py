import os


entity_package = ".entity"
repository_package = ".repository"
service_package = ".service"
service_impl_package = service_package + ".impl"
controller_package = ".web.controller"
dto_package = ".web.dto"
mapper_package = ".web.mapper"

src = "src"
web = src + "/web"
entity = src + "/entity/"
service = src + "/service/"
service_impl = service + "impl/"
repository = src + "/repository/"
dto = web + "/dto/"
controller = web + "/controller/"
mapper = web + "/mapper/"

def generate_project():
    if not os.path.exists(src):
        os.makedirs(src)
    if not os.path.exists(entity):
        os.makedirs(entity)
    if not os.path.exists(service):
        os.makedirs(service)
    if not os.path.exists(service_impl):
        os.makedirs(service_impl)
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
        
    print("\n>> Project structure generated!\n")