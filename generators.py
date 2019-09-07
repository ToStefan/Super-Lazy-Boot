import os

from utils import cap_first, switch_package

entity_package = ".entity"
repository_package = ".repository"
service_package = ".service"
service_impl_package = service_package + ".impl"
controller_package = ".web.controller"
dto_package = ".web.dto"
mapper_package = ".web.mapper"

def generate_project(root_package):
    if not os.path.exists(switch_package("src_main", root_package)): os.makedirs(switch_package("src_main", root_package))
    if not os.path.exists(switch_package("src_test", root_package)): os.makedirs(switch_package("src_test", root_package))
    if not os.path.exists(switch_package("entity", root_package)): os.makedirs(switch_package("entity", root_package))
    if not os.path.exists(switch_package("service", root_package)): os.makedirs(switch_package("service", root_package))
    if not os.path.exists(switch_package("service_impl", root_package)): os.makedirs(switch_package("service_impl", root_package))
    if not os.path.exists(switch_package("repository", root_package)): os.makedirs(switch_package("repository", root_package))
    if not os.path.exists(switch_package("web", root_package)): os.makedirs(switch_package("web", root_package))
    if not os.path.exists(switch_package("dto", root_package)): os.makedirs(switch_package("dto", root_package))
    if not os.path.exists(switch_package("controller", root_package)): os.makedirs(switch_package("controller", root_package))
    if not os.path.exists(switch_package("mapper", root_package)): os.makedirs(switch_package("mapper", root_package))

def generate_mapper_inteface(root_package):
    mapper_interface = "package " + root_package + mapper_package + ";\n\n"

    # Imports
    mapper_interface += "import java.util.List;\n\n"

    # Methods
    mapper_interface += "public interface Mapper<E, DTO> {\n\n"
    mapper_interface += "    DTO toDTO(E entity);\n"
    mapper_interface += "    E toEntity(DTO dto);\n"
    mapper_interface += "    List<DTO> toDTO(List<E> entities);\n"
    mapper_interface += "    List<E> toEntity(List<DTO> dtos);\n\n"
    mapper_interface += "}\n"
    return mapper_interface

def generate_mappers(root_package, class_name, attributes):
    mapper_class = "package " + root_package + mapper_package + ";\n\n"

    # Imports
    mapper_class += "import java.util.List;\n"
    mapper_class += "import java.util.stream.Collectors;\n"
    mapper_class += "import org.springframework.stereotype.Component;\n"
    mapper_class += "import " + root_package + entity_package + "." + class_name + ";\n"
    mapper_class += "import " + root_package + dto_package + "." + class_name + "DTO;\n\n"

    # Class header
    mapper_class += "@Component\n"
    mapper_class += "public class " + class_name + "Mapper implements Mapper<" + class_name + ", " + class_name + "DTO> {\n\n"

    #toDTO -> DTO
    mapper_class += "    @Override\n"
    mapper_class += "    public " + class_name + "DTO toDTO(" + class_name + " " + class_name.lower() + ") {\n"
    mapper_class += "        " + class_name + "DTO dto = new " + class_name + "DTO();\n"
    for att in attributes:
        attribute = att.split(":")
        mapper_class += "        dto.set" + cap_first(attribute[1]) + "(" + class_name.lower() + ".get" + cap_first(attribute[1]) + "());\n"
    mapper_class += "        return dto;\n"
    mapper_class += "    }\n\n"

    #toDTO -> List<DTO>
    mapper_class += "    @Override\n"
    mapper_class += "    public List<" + class_name + "DTO> toDTO(List<" + class_name + "> entities) {\n"
    mapper_class += "        return entities\n"
    mapper_class += "                    .stream()\n"
    mapper_class += "                    .map(" + class_name.lower() + " -> toDTO(" + class_name.lower() + "))\n"
    mapper_class += "                    .collect(Collectors.toList());\n"
    mapper_class += "    }\n\n"

    #toEntity -> Entity
    mapper_class += "    @Override\n"
    mapper_class += "    public " + class_name + " toEntity(" + class_name + "DTO " + class_name.lower() + "DTO) {\n"
    mapper_class += "        " + class_name + " entity = new " + class_name + "();\n"
    for att in attributes:
        attribute = att.split(":")
        mapper_class += "        entity.set" + cap_first(attribute[1]) + "(" + class_name.lower() + "DTO.get" \
                                                                                + cap_first(attribute[1]) + "());\n"
    mapper_class += "        return entity;\n"
    mapper_class += "    }\n\n"

    #toEntity -> List<Entity>
    mapper_class += "    @Override\n"
    mapper_class += "    public List<" + class_name + "> toEntity(List<" + class_name + "DTO> dtos) {\n"
    mapper_class += "        return dtos\n"
    mapper_class += "                    .stream()\n"
    mapper_class += "                    .map(" + class_name.lower() + "DTO -> toEntity(" + class_name.lower() + "DTO))\n"
    mapper_class += "                    .collect(Collectors.toList());\n"
    mapper_class += "    }\n\n"
    mapper_class += "}"
    return mapper_class

def generate_enumeration(root_package, enum_name, enums):
    javaEnum = "package " + root_package + entity_package + ";\n\n"

    javaEnum += "public enum " + enum_name + "{\n"
    for enum in enums:
        if enums.index(enum) == len(enums)-1:
            javaEnum += "    " + enum + "\n"
        else:
            javaEnum += "    " + enum + ",\n"
    javaEnum += "}\n"
    return javaEnum

def generate_entities(root_package, lombok, class_name, attributes):
    java_entity = "package " + root_package + entity_package + ";\n\n"

    # Imports
    java_entity += "import javax.persistence.Entity;\n"
    java_entity += "import javax.persistence.GeneratedValue;\n"
    java_entity += "import javax.persistence.GenerationType;\n"
    java_entity += "import javax.persistence.Id;\n"
    java_entity += "import javax.persistence.Table;\n\n"
    if(lombok) == True:
        java_entity += "import lombok.Getter;\n"
        java_entity += "import lombok.Setter;\n"
        java_entity += "import lombok.NoArgsConstructor;\n\n"

    # Class header
    if(lombok) == True:
        java_entity += "@Getter\n"
        java_entity += "@Setter\n"
        java_entity += "@NoArgsConstructor\n"
    java_entity += "@Entity\n"
    java_entity += "@Table(name = \"{class_nameLowerCase}\")".format(class_nameLowerCase=class_name.lower()) + "\n"
    java_entity += "public class " + class_name + " {\n"
    java_entity += "\n"
    
    # Attributes
    for att in attributes:
        attribute = att.split(":")
        try:
            if(attribute[2] == "primary"):
                java_entity += "    @Id\n"
                java_entity += "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
                java_entity += "    private {attType} {attName}".format(attType=attribute[0], attName=attribute[1]) + ";\n"
        except:
            java_entity += "    private {attType} {attName}".format(attType=attribute[0], attName=attribute[1]) + ";\n"
        java_entity += "\n"
            
    if(lombok) == False:
        # Default constructor
        java_entity += "    public " + class_name + "() {\n"
        java_entity += "\n"
        java_entity += "    }\n"
        java_entity += "\n"

        # Getters/Setters
        for att in attributes:
            attribute = att.split(":")
            java_entity += "    public " + attribute[0] + " get" + cap_first(attribute[1]) + "() {\n"
            java_entity += "        return " + attribute[1] + ";\n"
            java_entity += "    }\n"
            java_entity += "\n"
            java_entity += "    public void set" + cap_first(attribute[1]) + "(" + attribute[0] + " " + attribute[1] + ") {\n"
            java_entity += "        this." + attribute[1] + " = " + attribute[1] + ";\n"
            java_entity += "    }\n"
            java_entity += "\n"
    java_entity += "}"

    return java_entity

def generate_dtos(root_package, lombok, class_name, attributes):
    java_dto = "package " + root_package + dto_package + ";\n\n"

    # Imports
    if(lombok) == True:
        java_dto += "import lombok.Getter;\n"
        java_dto += "import lombok.Setter;\n"
        java_dto += "import lombok.NoArgsConstructor;\n"
    java_dto += "\n"

    # Class header
    if(lombok) == True:
        java_dto += "@Getter\n"
        java_dto += "@Setter\n"
        java_dto += "@NoArgsConstructor\n"
    java_dto += "public class " + class_name + "DTO {\n\n"

    # Attributes
    for att in attributes:
        attribute = att.split(":")
        java_dto += "    private {attType} {attName}".format(attType=attribute[0], attName=attribute[1]) + ";\n"

    # Default constructor
    java_dto += "\n"
    if(lombok) == False:
        java_dto += "    public " + class_name + "DTO() {\n"
        java_dto += "\n"
        java_dto += "    }\n"
        java_dto += "\n"

        # Getters/Setters
        for att in attributes:
            attribute = att.split(":")
            java_dto += "    public " + attribute[0] + " get" + cap_first(attribute[1]) + "() {\n"
            java_dto += "        return " + attribute[1] + ";\n"
            java_dto += "    }\n"
            java_dto += "\n"
            java_dto += "    public void set" + cap_first(attribute[1]) + "(" + attribute[0] + " " + attribute[1] + ") {\n"
            java_dto += "        this." + attribute[1] + " = " + attribute[1] + ";\n"
            java_dto += "    }\n"
            java_dto += "\n"
    java_dto += "}"
    return java_dto

def generate_repositories(root_package, class_name, primary_key_type):
    java_repository = "package " + root_package + repository_package + ";\n\n"

    # Imports
    java_repository += "import org.springframework.data.jpa.repository.JpaRepository;\n"
    java_repository += "import org.springframework.stereotype.Repository;\n"
    java_repository += "import " + root_package + entity_package + "." + class_name + ";\n\n"

    # Interface header
    java_repository += "@Repository\n"
    java_repository += "public interface " + class_name + "Repository extends JpaRepository<" + class_name + ", " + primary_key_type + "> {\n"
    java_repository += "\n"
    java_repository += "}"
    return java_repository

def generate_service_interface(root_package, class_name, attributes):
    service_interface = "package " + root_package + service_package + ";\n\n"

    # Imports
    service_interface += "import java.util.List;\n"
    service_interface += "import " + root_package + dto_package + "." + class_name + "DTO;\n\n"

    # Methods
    service_interface += "public interface " + class_name + "Service {\n\n"
    service_interface += "    List<" + class_name + "DTO> findAll();\n"
    service_interface += "    " + class_name + "DTO findById(Long id);\n"
    service_interface += "    " + class_name + "DTO create(" + class_name + "DTO " + class_name.lower() + "DTO);\n"
    service_interface += "    " + class_name + "DTO update(" + class_name + "DTO " + class_name.lower() + "DTO);\n"
    service_interface += "    void remove(Long id);\n\n"
    service_interface += "}\n\n"
    return service_interface

def generate_service(root_package, lombok, class_name, attributes):
    service_impl = "package " + root_package + service_impl_package + ";\n\n"
    
    # Imports
    service_impl += "import java.util.List;\n"
    service_impl += "import org.springframework.beans.factory.annotation.Autowired;\n"
    service_impl += "import org.springframework.stereotype.Service;\n"
    service_impl += "import " + root_package + repository_package + "." + class_name + "Repository;\n"
    service_impl += "import " + root_package + service_package + "." + class_name + "Service;\n"
    service_impl += "import " + root_package + dto_package + "." + class_name + "DTO;\n"
    service_impl += "import " + root_package + mapper_package + "." + class_name + "Mapper;\n\n"
    if(lombok) == True:
        service_impl += "import lombok.AllArgsConstructor;\n\n" 

    # Class header & dependency injection
    if(lombok) == True:
        service_impl += "@AllArgsConstructor\n"
    service_impl += "@Service\n"
    service_impl += "public class " + class_name + "ServiceImpl implements " + class_name + "Service {\n\n"
    if(lombok) == True:
        service_impl += "    private final " + class_name + "Repository " + class_name.lower() + "Repository;\n"
        service_impl += "    private final " + class_name + "Mapper " + class_name.lower() + "Mapper;\n\n"
    else:
        service_impl += "    @Autowired\n"
        service_impl += "    private " + class_name + "Repository " + class_name.lower() + "Repository;\n\n"
        service_impl += "    @Autowired\n"
        service_impl += "    private " + class_name + "Mapper " + class_name.lower() + "Mapper;\n\n"

    # Methods
    service_impl += "    @Override\n"
    service_impl += "    public List<" + class_name + "DTO> findAll() {\n"
    service_impl += "        return " + class_name.lower() + "Mapper.toDTO(" + class_name.lower() + "Repository.findAll());\n"
    service_impl += "    }\n\n"
    service_impl += "    @Override\n"
    service_impl += "    public " + class_name + "DTO findById(Long id) {\n"
    service_impl += "        return " + class_name.lower() +"Mapper.toDTO(" + class_name.lower() + "Repository.getOne(id));\n"
    service_impl += "    }\n\n"
    service_impl += "    @Override\n"
    service_impl += "    public " + class_name + "DTO create(" + class_name + "DTO " + class_name.lower() + "DTO) {\n"
    service_impl += "        return " + class_name.lower() + "Mapper.toDTO(" + class_name.lower() + "Repository.save(" + \
                                                    class_name.lower() + "Mapper.toEntity(" + class_name.lower() + "DTO)));\n"
    service_impl += "    }\n\n"
    service_impl += "    @Override\n"
    service_impl += "    public " + class_name + "DTO update(" + class_name + "DTO " + class_name.lower() + "DTO) {\n"
    service_impl += "        return " + class_name.lower() + "Mapper.toDTO(" + class_name.lower() + "Repository.save(" + \
                                                    class_name.lower() + "Mapper.toEntity(" + class_name.lower() + "DTO)));\n"
    service_impl += "    }\n\n"
    service_impl += "    @Override\n"
    service_impl += "    public void remove(Long " + class_name.lower() + "Id) {\n"
    service_impl += "        " + class_name.lower() + "Repository.deleteById(" + class_name.lower() + "Id);\n"
    service_impl += "    }\n\n"
    service_impl += "}"
    return service_impl

def generate_controllers(root_package, lombok, class_name, attributes):
    controller_class = "package " + root_package + controller_package + ";\n\n"

    # Imports
    controller_class += "import java.util.List;\n"
    controller_class += "import org.springframework.beans.factory.annotation.Autowired;\n"
    controller_class += "import org.springframework.http.HttpStatus;\n"
    controller_class += "import org.springframework.http.ResponseEntity;\n"
    controller_class += "import org.springframework.web.bind.annotation.DeleteMapping;\n"
    controller_class += "import org.springframework.web.bind.annotation.GetMapping;\n"
    controller_class += "import org.springframework.web.bind.annotation.PathVariable;\n"
    controller_class += "import org.springframework.web.bind.annotation.PostMapping;\n"
    controller_class += "import org.springframework.web.bind.annotation.PutMapping;\n"
    controller_class += "import org.springframework.web.bind.annotation.RequestBody;\n"
    controller_class += "import org.springframework.web.bind.annotation.RequestMapping;\n"
    controller_class += "import org.springframework.web.bind.annotation.RestController;\n"
    controller_class += "import " + root_package + service_impl_package + "." + class_name + "ServiceImpl;\n"
    controller_class += "import " + root_package + dto_package + "." + class_name + "DTO;\n\n"
    if(lombok) == True:
        controller_class += "import lombok.AllArgsConstructor;\n\n"

    # Class header & dependency injection
    if(lombok) == True:
        controller_class += "@AllArgsConstructor\n"
    controller_class += "@RestController\n"
    controller_class += "@RequestMapping(value = \"/api/" + class_name.lower() + "\")\n"
    controller_class += "public class " + class_name + "Controller {\n\n"
    if(lombok) == True:
        controller_class += "    private final " + class_name + "ServiceImpl " + class_name.lower() + "Service;\n\n"
    else:
        controller_class += "    @Autowired\n"
        controller_class += "    private " + class_name + "ServiceImpl " + class_name.lower() + "Service;\n\n"

    # Controllers
    controller_class += "    @GetMapping\n"
    controller_class += "    public ResponseEntity<List<" + class_name + "DTO>> findAll() {\n"
    controller_class += "         List<" + class_name + "DTO> dtos = " + class_name.lower() + "Service.findAll();\n"
    controller_class += "         return new ResponseEntity<>(dtos, HttpStatus.OK);\n"
    controller_class += "    }\n\n"
    controller_class += "    @GetMapping(value = \"/{id}\")\n"
    controller_class += "    public ResponseEntity<" + class_name + "DTO> findById(@PathVariable(\"id\") Long id) {\n"
    controller_class += "        " + class_name + "DTO dto = " + class_name.lower() + "Service.findById(id);\n"
    controller_class += "        return new ResponseEntity<>(dto, HttpStatus.OK);\n"
    controller_class += "    }\n\n"
    controller_class += "    @PostMapping\n"
    controller_class += "    public ResponseEntity<" + class_name + "DTO> create(@RequestBody " + \
                                                                class_name + "DTO " + class_name.lower() + "DTO) {\n"
    controller_class += "        " + class_name + "DTO retVal = " + class_name.lower() + "Service.create(" + class_name.lower() + "DTO);\n"
    controller_class += "        return new ResponseEntity<>(retVal, HttpStatus.OK);\n"
    controller_class += "    }\n\n"
    controller_class += "    @PutMapping\n"
    controller_class += "    public ResponseEntity<" + class_name + "DTO> update(@RequestBody " + \
                                                                class_name + "DTO " + class_name.lower() + "DTO) {\n"
    controller_class += "        " + class_name + "DTO retVal = " + class_name.lower() + "Service.update(" + class_name.lower() + "DTO);\n"
    controller_class += "        return new ResponseEntity<>(retVal, HttpStatus.OK);\n"
    controller_class += "    }\n\n"
    controller_class += "    @DeleteMapping(value = \"/{id}\")\n"
    controller_class += "    public ResponseEntity<HttpStatus> delete(@PathVariable(\"id\") Long id) {\n"
    controller_class += "        " + class_name.lower() + "Service.remove(id);\n"
    controller_class += "        return new ResponseEntity<>(HttpStatus.OK);\n"
    controller_class += "    }\n\n"
    controller_class += "}"
    return controller_class