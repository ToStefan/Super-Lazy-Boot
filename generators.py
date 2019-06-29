import os

import structure
from utils import getPrimaryKeyType

lombok = False

def generator(classMap, enumMap, settingsMap):
    structure.generateProject()

    fileMapperInterface = open(structure.mapper + "/Mapper.java", "w+")
    mapperInterface = generateMapperInteface()
    fileMapperInterface.write(mapperInterface)

    for key, values in classMap.items():

        fileEntity = open(structure.entity + key + ".java", "w+")
        javaEntity = generateEntities(key, values)
        fileEntity.write(javaEntity)

        fileDto = open(structure.dto + key + "DTO.java", "w+")
        javaDto = generateDtos(key, values)
        fileDto.write(javaDto)

        fileRepository = open(structure.repository + key + "Repository.java", "w+")
        javaRepository = generateRepositories(key, getPrimaryKeyType(values))
        fileRepository.write(javaRepository)

        fileMapperClass = open(structure.mapper + key + "Mapper.java", "w+")
        mapperClass = generateMappers(key, values)
        fileMapperClass.write(mapperClass)

        fileServiceInterface = open(structure.service + key + "Service.java", "w+")
        serviceInterface = generateServiceInterface(key, values)
        fileServiceInterface.write(serviceInterface)

        fileServiceImpl = open(structure.serviceImpl + key + "ServiceImpl.java", "w+")
        serviceImpl = generateService(key, values)
        fileServiceImpl.write(serviceImpl)

        fileController = open(structure.controller + key + "Controller.java", "w+")
        controllerClass = generateControllers(key, values)
        fileController.write(controllerClass)
        print("")

    for key, values in enumMap.items():
        fileEnum = open(structure.entity + key + ".java", "w+")
        javaEnum = generateEnumeration(key, values)
        fileEnum.write(javaEnum)

    for key, value in settingsMap.items():
        if(key == "lombok"):
            global lombok
            lombok = value.capitalize()

def generateMapperInteface():
    print(">> Generating Mapper Interface...\n")
    mapperInterface = ""

    # Imports
    mapperInterface += "import java.util.List;\n\n"

    # Methods
    mapperInterface += "public interface Mapper<E, DTO> {\n\n"
    mapperInterface += "    DTO toDTO(E entity);\n"
    mapperInterface += "    E toEntity(DTO dto);\n"
    mapperInterface += "    List<DTO> toDTO(List<E> entities);\n"
    mapperInterface += "    List<E> toEntity(List<DTO> dtos);\n\n"
    mapperInterface += "}\n"
    return mapperInterface

def generateMappers(className, attributes):

    print(">> Generating mapper for " + className)
    mapperClass = ""

    mapperClass += "import java.util.List;\n"
    mapperClass += "import java.util.stream.Collectors;\n"
    mapperClass += "import org.springframework.stereotype.Component;\n\n"

    mapperClass += "@Component\n"
    mapperClass += "public class " + className + "Mapper implements Mapper<" + className + ", " + className + "DTO> {\n\n"

    #toDTO -> DTO
    mapperClass += "    @Override\n"
    mapperClass += "    public " + className + "DTO toDTO(" + className + " " + className.lower() + ") {\n"
    mapperClass += "        " + className + "DTO dto = new " + className + "DTO();\n"
    for att in attributes:
        attribute = att.split(":")
        mapperClass += "        dto.set" + attribute[1].capitalize() + "(" + className.lower() + ".get" + attribute[1].capitalize() + "());\n"
    mapperClass += "        return dto;\n"
    mapperClass += "    }\n\n"

    #toDTO -> List<DTO>
    mapperClass += "    @Override\n"
    mapperClass += "    public List<" + className + "DTO> toDTO(List<" + className + "> entities) {\n"
    mapperClass += "        return entities\n"
    mapperClass += "                    .stream()\n"
    mapperClass += "                    .map(" + className.lower() + " -> toDTO(" + className.lower() + "))\n"
    mapperClass += "                    .collect(Collectors.toList());\n"
    mapperClass += "    }\n\n"

    #toEntity -> Entity
    mapperClass += "    @Override\n"
    mapperClass += "    public " + className + " toEntity(" + className + "DTO " + className.lower() + "DTO) {\n"
    mapperClass += "        " + className + " entity = new " + className + "();\n"
    for att in attributes:
        attribute = att.split(":")
        mapperClass += "        entity.set" + attribute[1].capitalize() + "(" + className.lower() + "DTO.get" \
                                                                                + attribute[1].capitalize() + "());\n"
    mapperClass += "        return entity;\n"
    mapperClass += "    }\n\n"

    #toEntity -> List<Entity>
    mapperClass += "    @Override\n"
    mapperClass += "    public List<" + className + "> toEntity(List<" + className + "DTO> dtos) {\n"
    mapperClass += "        return dtos\n"
    mapperClass += "                    .stream()\n"
    mapperClass += "                    .map(" + className.lower() + "DTO -> toEntity(" + className.lower() + "DTO))\n"
    mapperClass += "                    .collect(Collectors.toList());\n"
    mapperClass += "    }\n\n"
    mapperClass += "}"
    return mapperClass

def generateEnumeration(enumName, values):
    print(">> Generating enum: " + enumName)
    javaEnum = ""

    javaEnum += "public enum " + enumName + "\n"
    for enum in values:
        if values.index(enum) == len(values)-1:
            javaEnum += "    " + enum + "\n"
        else:
            javaEnum += "    " + enum + ",\n"
    javaEnum += "}\n"
    return javaEnum

def generateEntities(className, attributes):
    print(">> Generating class: {className} -> attributes: {attributes}".format(className=className, attributes=attributes))
    javaEntity = "";

    # Imports
    javaEntity += "import javax.persistence.Entity;\n"
    javaEntity += "import javax.persistence.GeneratedValue;\n"
    javaEntity += "import javax.persistence.GenerationType;\n"
    javaEntity += "import javax.persistence.Id;\n"
    javaEntity += "import javax.persistence.Table;\n\n"

    # Class header
    javaEntity += "@Entity\n"
    javaEntity += "@Table(name = \"{classNameLowerCase}\")".format(classNameLowerCase=className.lower()) + "\n"
    javaEntity += "public class " + className + " {\n"
    javaEntity += "\n"
    
    # Attributes
    for att in attributes:
        attribute = att.split(":")
        try:
            if(attribute[2] == "primary"):
                javaEntity += "    @Id\n"
                javaEntity += "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
                javaEntity += "    private {attType} {attName}".format(attType=attribute[0], attName=attribute[1]) + ";\n"
        except:
            javaEntity += "    private {attType} {attName}".format(attType=attribute[0], attName=attribute[1]) + ";\n"
        javaEntity += "\n"
            

    # Default constructor
    javaEntity += "    public " + className + "() {\n"
    javaEntity += "\n"
    javaEntity += "    }\n"
    javaEntity += "\n"

    # Getters/Setters
    for att in attributes:
        attribute = att.split(":")
        javaEntity += "    public " + attribute[0] + " get" + attribute[1].capitalize() + "() {\n"
        javaEntity += "        return " + attribute[1] + ";\n"
        javaEntity += "    }\n"
        javaEntity += "\n"
        javaEntity += "    public void set" + attribute[1].capitalize() + "(" + attribute[0] + " " + attribute[1] + ") {\n"
        javaEntity += "        this." + attribute[1] + " = " + attribute[1] + ";\n"
        javaEntity += "    }\n"
        javaEntity += "\n"
    javaEntity += "}"

    return javaEntity

def generateDtos(className, attributes):
    print(">> Generating DTO: {className}DTO -> attributes: {attributes}".format(className=className, attributes=attributes))
    javaDto = ""

    # Class header
    javaDto += "public class " + className + "DTO {\n\n"

    # Attributes
    for att in attributes:
        attribute = att.split(":")
        javaDto += "    private {attType} {attName}".format(attType=attribute[0], attName=attribute[1]) + ";\n"
    javaDto += "\n"
    javaDto += "    public " + className + "DTO() {\n"
    javaDto += "\n"
    javaDto += "    }\n"
    javaDto += "\n"

    # Getters/Setters
    for att in attributes:
        attribute = att.split(":")
        javaDto += "    public " + attribute[0] + " get" + attribute[1].capitalize() + "() {\n"
        javaDto += "        return " + attribute[1] + ";\n"
        javaDto += "    }\n"
        javaDto += "\n"
        javaDto += "    public void set" + attribute[1].capitalize() + "(" + attribute[0] + " " + attribute[1] + ") {\n"
        javaDto += "        this." + attribute[1] + " = " + attribute[1] + ";\n"
        javaDto += "    }\n"
        javaDto += "\n"
    javaDto += "}"

    return javaDto

def generateRepositories(className, primaryKeyType):
    print(">> Generating repository for " + className + " -> ID type: " + primaryKeyType)
    javaRepository = ""

    # Imports
    javaRepository += "import org.springframework.data.jpa.repository.JpaRepository;\n"
    javaRepository += "import org.springframework.stereotype.Repository;\n\n"

    # Interface header
    javaRepository += "@Repository\n"
    javaRepository += "public interface " + className + "Repository extends JpaRepository<" + className + ", " + primaryKeyType + "> {\n"
    javaRepository += "\n"
    javaRepository += "}"
    return javaRepository

def generateServiceInterface(className, attributes):
    print(">> Generating service interface for " + className)
    serviceInterface = ""

    # Imports
    serviceInterface += "import java.util.List;\n\n"

    # Methods
    serviceInterface += "public interface " + className + "Service {\n\n"
    serviceInterface += "    List<" + className + "DTO> findAll();\n"
    serviceInterface += "    " + className + "DTO findById(Long id);\n"
    serviceInterface += "    " + className + "DTO create(" + className + "DTO " + className.lower() + "DTO);\n"
    serviceInterface += "    " + className + "DTO update(" + className + "DTO " + className.lower() + "DTO);\n"
    serviceInterface += "    void remove(Long id);\n\n"
    serviceInterface += "}\n\n"
    return serviceInterface

def generateService(className, attributes):
    print(">> Generating service for " + className)
    serviceImpl = ""
    
    # Imports
    serviceImpl += "import java.util.List;\n"
    serviceImpl += "import org.springframework.beans.factory.annotation.Autowired;\n"
    serviceImpl += "import org.springframework.stereotype.Service;\n\n"

    # Methods
    serviceImpl += "@Service\n"
    serviceImpl += "public class " + className + "ServiceImpl implements " + className + "Service {\n\n"
    serviceImpl += "    @Autowired\n"
    serviceImpl += "    private " + className + "Repository " + className.lower() + "Repository;\n\n"
    serviceImpl += "    @Autowired\n"
    serviceImpl += "    private " + className + "Mapper " + className.lower() + "Mapper;\n\n"
    serviceImpl += "    @Override\n"
    serviceImpl += "    public List<" + className + "DTO> findAll() {\n"
    serviceImpl += "        return " + className.lower() + "Mapper.toDTO(" + className.lower() + "Repository.findAll());\n"
    serviceImpl += "    }\n\n"
    serviceImpl += "    @Override\n"
    serviceImpl += "    public " + className + "DTO findById(Long id) {\n"
    serviceImpl += "        return " + className.lower() +"Mapper.toDTO(" + className.lower() + "Repository.getOne(id));\n"
    serviceImpl += "    }\n\n"
    serviceImpl += "    @Override\n"
    serviceImpl += "    public " + className + "DTO create(" + className + "DTO " + className.lower() + "DTO) {\n"
    serviceImpl += "        return " + className.lower() + "Mapper.toDTO(" + className.lower() + "Repository.save(" + \
                                                    className.lower() + "Mapper.toEntity(" + className.lower() + "DTO)));\n"
    serviceImpl += "    }\n\n"
    serviceImpl += "    @Override\n"
    serviceImpl += "    public " + className + "DTO update(" + className + "DTO " + className.lower() + "DTO) {\n"
    serviceImpl += "        return " + className.lower() + "Mapper.toDTO(" + className.lower() + "Repository.save(" + \
                                                    className.lower() + "Mapper.toEntity(" + className.lower() + "DTO)));\n"
    serviceImpl += "    }\n\n"
    serviceImpl += "    @Override\n"
    serviceImpl += "    public void remove(Long " + className.lower() + "Id) {\n"
    serviceImpl += "        " + className.lower() + "Repository.deleteById(" + className.lower() + "Id);\n"
    serviceImpl += "    }\n\n"
    serviceImpl += "}"
    return serviceImpl

def generateControllers(className, attributes):
    print(">> Generating controller for " + className)
    controllerClass = ""

    # Imports
    controllerClass += "import java.util.List;"
    controllerClass += "import org.springframework.beans.factory.annotation.Autowired;\n"
    controllerClass += "import org.springframework.http.HttpStatus;\n"
    controllerClass += "import org.springframework.http.ResponseEntity;\n"
    controllerClass += "import org.springframework.web.bind.annotation.DeleteMapping;\n"
    controllerClass += "import org.springframework.web.bind.annotation.GetMapping;\n"
    controllerClass += "import org.springframework.web.bind.annotation.PathVariable;\n"
    controllerClass += "import org.springframework.web.bind.annotation.PostMapping;\n"
    controllerClass += "import org.springframework.web.bind.annotation.PutMapping;\n"
    controllerClass += "import org.springframework.web.bind.annotation.RequestBody;\n"
    controllerClass += "import org.springframework.web.bind.annotation.RequestMapping;\n"
    controllerClass += "import org.springframework.web.bind.annotation.RestController;\n\n"

    # Class header & dependency injection
    controllerClass += "@RestController\n"
    controllerClass += "@RequestMapping(value = \"/api/" + className.lower() + "\")\n"
    controllerClass += "public class " + className + "Controller {\n\n"
    controllerClass += "    @Autowired\n"
    controllerClass += "    private " + className + "ServiceImpl " + className.lower() + "Service;\n\n"

    # Controllers
    controllerClass += "    @GetMapping\n"
    controllerClass += "    public ResponseEntity<List<" + className + "DTO>> findAll() {\n"
    controllerClass += "         List<" + className + "DTO> dtos = " + className.lower() + "Service.findAll();\n"
    controllerClass += "         return new ResponseEntity<>(dtos, HttpStatus.OK);\n"
    controllerClass += "    }\n\n"
    controllerClass += "    @GetMapping(value = \"/{id}\")\n"
    controllerClass += "    public ResponseEntity<" + className + "DTO> findById(@PathVariable(\"id\") Long id) {\n"
    controllerClass += "        " + className + "DTO dtos = " + className.lower() + "Service.findById(id);\n"
    controllerClass += "        return new ResponseEntity<>(dtos, HttpStatus.OK);\n"
    controllerClass += "    }\n\n"
    controllerClass += "    @PostMapping\n"
    controllerClass += "    public ResponseEntity<" + className + "DTO> create(@RequestBody " + \
                                                                className + "DTO " + className.lower() + "DTO) {\n"
    controllerClass += "        " + className + "DTO retVal = " + className.lower() + "Service.create(" + className.lower() + "DTO);\n"
    controllerClass += "        return new ResponseEntity<>(retVal, HttpStatus.OK);\n"
    controllerClass += "    }\n\n"
    controllerClass += "    @PutMapping\n"
    controllerClass += "    public ResponseEntity<" + className + "DTO> update(@RequestBody " + \
                                                                className + "DTO " + className.lower() + "DTO) {\n"
    controllerClass += "        " + className + "DTO retVal = " + className.lower() + "Service.update(" + className.lower() + "DTO);\n"
    controllerClass += "        return new ResponseEntity<>(retVal, HttpStatus.OK);\n"
    controllerClass += "    }\n\n"
    controllerClass += "    @DeleteMapping(value = \"/{id}\")\n"
    controllerClass += "    public ResponseEntity<HttpStatus> delete(@PathVariable(\"id\") Long id) {\n"
    controllerClass += "        " + className.lower() + "Service.remove(id);\n"
    controllerClass += "        return new ResponseEntity<>(HttpStatus.OK);\n"
    controllerClass += "    }\n\n"
    controllerClass += "}"
    return controllerClass