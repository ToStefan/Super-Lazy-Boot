import os

import structure

def generateEnumeration(enumName, values):
    print(">> Generating enum: " + enumName)

    javaEnum = open(structure.entity + enumName + ".java", "w+")

    javaEnum.write("public enum " + enumName + "\n")
    for enum in values:
        if values.index(enum) == len(values)-1:
            javaEnum.write("    " + enum + "\n")
        else:
            javaEnum.write("    " + enum + ",\n")
    javaEnum.write("}\n")

def generateEntities(className, attributes):
    print(">> Generating class: {className} -> attributes: {attributes}".format(className=className, attributes=attributes))

    javaEntity = open(structure.entity + className + ".java", "w+")

    # imports
    javaEntity.write("import javax.persistence.Entity;\n")
    javaEntity.write("import javax.persistence.GeneratedValue;\n")
    javaEntity.write("import javax.persistence.GenerationType;\n")
    javaEntity.write("import javax.persistence.Id;\n")
    javaEntity.write("import javax.persistence.Table;\n\n")

    # Class name
    javaEntity.write("@Entity\n")
    javaEntity.write("@Table(name = \"{classNameLowerCase}\")".format(classNameLowerCase=className.lower()) + "\n")
    javaEntity.write("public class " + className + " {\n")
    javaEntity.write("\n")
    
    # Attributes
    for att in attributes:
        attribute = att.split(":")
        try:
            if(attribute[2] == "primary"):
                javaEntity.write("    @Id\n")
                javaEntity.write("    @GeneratedValue(strategy = GenerationType.IDENTITY)\n")
                javaEntity.write("    private {attType} {attName}".format(attType=attribute[0], attName=attribute[1]) + ";\n")
        except:
            javaEntity.write("    private {attType} {attName}".format(attType=attribute[0], attName=attribute[1]) + ";\n")
        javaEntity.write("\n")
            

    # Default constructor
    javaEntity.write("    public " + className + "() {\n")
    javaEntity.write("\n")
    javaEntity.write("    }\n")
    javaEntity.write("\n")

    # Getters/Setters
    for att in attributes:
        attribute = att.split(":")
        javaEntity.write("    public " + attribute[0] + " get" + attribute[1].capitalize() + "() {\n")
        javaEntity.write("        return " + attribute[1] + ";\n")
        javaEntity.write("    }\n")
        javaEntity.write("\n")
        javaEntity.write("    public void set" + attribute[1].capitalize() + "(" + attribute[0] + " " + attribute[1] + ") {\n")
        javaEntity.write("        this." + attribute[1] + " = " + attribute[1] + ";\n")
        javaEntity.write("    }\n")
        javaEntity.write("\n")
    javaEntity.write("}")

def generateDtos(className, attributes):

    print(">> Generating DTO: {className}DTO -> attributes: {attributes}".format(className=className, attributes=attributes))

    javaDto = open(structure.dto + className + "DTO.java", "w+")

    javaDto.write("public class " + className + "DTO {\n\n")

    for att in attributes:
        attribute = att.split(":")
        javaDto.write("    private {attType} {attName}".format(attType=attribute[0], attName=attribute[1]) + ";\n")
    javaDto.write("\n")

    javaDto.write("    public " + className + "DTO() {\n")
    javaDto.write("\n")
    javaDto.write("    }\n")
    javaDto.write("\n")


    for att in attributes:
        attribute = att.split(":")
        javaDto.write("    public " + attribute[0] + " get" + attribute[1].capitalize() + "() {\n")
        javaDto.write("        return " + attribute[1] + ";\n")
        javaDto.write("    }\n")
        javaDto.write("\n")
        javaDto.write("    public void set" + attribute[1].capitalize() + "(" + attribute[0] + " " + attribute[1] + ") {\n")
        javaDto.write("        this." + attribute[1] + " = " + attribute[1] + ";\n")
        javaDto.write("    }\n")
        javaDto.write("\n")
    javaDto.write("}")

def generateRepositories(className, primaryKeyType):

    print(">> Generating repository for " + className + " -> ID type: " + primaryKeyType)

    javaRepository = open(structure.repository + className + "Repository.java", "w+")

    # imports
    javaRepository.write("import org.springframework.data.jpa.repository.JpaRepository;\n")
    javaRepository.write("import org.springframework.stereotype.Repository;\n\n")

    javaRepository.write("@Repository\n")
    javaRepository.write("public interface " + className + "Repository extends JpaRepository<" + className + ", " + primaryKeyType + "> {\n")
    javaRepository.write("\n")
    javaRepository.write("}")

def generateMapperInteface():

    print(">> Generating Mapper Interface...\n")
    mapperInterface = open(structure.mapper + "/Mapper.java", "w+")

    mapperInterface.write("import java.util.List;\n\n")

    mapperInterface.write("public interface Mapper<E, DTO> {\n\n")
    mapperInterface.write("    DTO toDTO(E entity);\n")
    mapperInterface.write("    E toEntity(DTO dto);\n")
    mapperInterface.write("    List<DTO> toDTO(List<E> entities);\n")
    mapperInterface.write("    List<E> toEntity(List<DTO> dtos);\n\n")
    mapperInterface.write("}\n")

def generateMappers(className, attributes):

    print(">> Generating mapper for " + className)
    mapperClass = open(structure.mapper + className + "Mapper.java", "w+")

    mapperClass.write("import java.util.List;\n")
    mapperClass.write("import java.util.stream.Collectors;\n")
    mapperClass.write("import org.springframework.stereotype.Component;\n\n")

    mapperClass.write("@Component\n")
    mapperClass.write("public class " + className + "Mapper implements Mapper<" + className + ", " + className + "DTO> {\n\n")

    #toDTO -> DTO
    mapperClass.write("    @Override\n")
    mapperClass.write("    public " + className + "DTO toDTO(" + className + " " + className.lower() + ") {\n")
    mapperClass.write("        " + className + "DTO dto = new " + className + "DTO();\n")
    for att in attributes:
        attribute = att.split(":")
        mapperClass.write("        dto.set" + attribute[1].capitalize() + "(" + className.lower() + ".get" + attribute[1].capitalize() + "());\n")
    mapperClass.write("        return dto;\n")
    mapperClass.write("    }\n\n")

    #toDTO -> List<DTO>
    mapperClass.write("    @Override\n")
    mapperClass.write("    public List<" + className + "DTO> toDTO(List<" + className + "> entities) {\n")
    mapperClass.write("        return entities\n")
    mapperClass.write("                    .stream()\n")
    mapperClass.write("                    .map(" + className.lower() + " -> toDTO(" + className.lower() + "))\n")
    mapperClass.write("                    .collect(Collectors.toList());\n")
    mapperClass.write("    }\n\n")

    #toEntity -> Entity
    mapperClass.write("    @Override\n")
    mapperClass.write("    public " + className + " toEntity(" + className + "DTO " + className.lower() + "DTO) {\n")
    mapperClass.write("        " + className + " entity = new " + className + "();\n")
    for att in attributes:
        attribute = att.split(":")
        mapperClass.write("        entity.set" + attribute[1].capitalize() + "(" + className.lower() + "DTO.get" + attribute[1].capitalize() + "());\n")
    mapperClass.write("        return entity;\n")
    mapperClass.write("    }\n\n")

    #toEntity -> List<Entity>
    mapperClass.write("    @Override\n")
    mapperClass.write("    public List<" + className + "> toEntity(List<" + className + "DTO> dtos) {\n")
    mapperClass.write("        return dtos\n")
    mapperClass.write("                    .stream()\n")
    mapperClass.write("                    .map(" + className.lower() + "DTO -> toEntity(" + className.lower() + "DTO))\n")
    mapperClass.write("                    .collect(Collectors.toList());\n")
    mapperClass.write("    }\n\n")
    mapperClass.write("}")

def generateServiceInterface(className, attributes):

    print(">> Generating service interface for " + className)
    serviceInterface = open(structure.service + className + "Service.java", "w+")

    serviceInterface.write("import java.util.List;\n\n")

    serviceInterface.write("public interface " + className + "Service {\n\n")
    serviceInterface.write("    List<" + className + "DTO> findAll();\n")
    serviceInterface.write("    " + className + "DTO findById(Long id);\n")
    serviceInterface.write("    " + className + "DTO create(" + className + "DTO " + className.lower() + "DTO);\n")
    serviceInterface.write("    " + className + "DTO update(" + className + "DTO " + className.lower() + "DTO);\n")
    serviceInterface.write("    void remove(Long id);\n\n")
    serviceInterface.write("}\n\n")

def generateServices(className, attributes):

    print(">> Generating service for " + className)
    serviceClass = open(structure.serviceImpl + className + "ServiceImpl.java", "w+")

    serviceClass.write("import java.util.List;\n")
    serviceClass.write("import org.springframework.beans.factory.annotation.Autowired;\n")
    serviceClass.write("import org.springframework.stereotype.Service;\n\n")

    serviceClass.write("@Service\n")
    serviceClass.write("public class " + className + "ServiceImpl implements " + className + "Service {\n\n")
    serviceClass.write("    @Autowired\n")
    serviceClass.write("    private " + className + "Repository " + className.lower() + "Repository;\n\n")
    serviceClass.write("    @Autowired\n")
    serviceClass.write("    private " + className + "Mapper " + className.lower() + "Mapper;\n\n")
    serviceClass.write("    @Override\n")
    serviceClass.write("    public List<" + className + "DTO> findAll() {\n")
    serviceClass.write("        return " + className.lower() + "Mapper.toDTO(" + className.lower() + "Repository.findAll());\n")
    serviceClass.write("    }\n\n")
    serviceClass.write("    @Override\n")
    serviceClass.write("    public " + className + "DTO findById(Long id) {\n")
    serviceClass.write("        return " + className.lower() +"Mapper.toDTO(" + className.lower() + "Repository.getOne(id));\n")
    serviceClass.write("    }\n\n")
    serviceClass.write("    @Override\n")
    serviceClass.write("    public " + className + "DTO create(" + className + "DTO " + className.lower() + "DTO) {\n")
    serviceClass.write("        return " + className.lower() + "Mapper.toDTO(" + className.lower() + "Repository.save(" + className.lower() + "Mapper.toEntity(" + className.lower() + "DTO)));\n")
    serviceClass.write("    }\n\n")
    serviceClass.write("    @Override\n")
    serviceClass.write("    public " + className + "DTO update(" + className + "DTO " + className.lower() + "DTO) {\n")
    serviceClass.write("        return " + className.lower() + "Mapper.toDTO(" + className.lower() + "Repository.save(" + className.lower() + "Mapper.toEntity(" + className.lower() + "DTO)));\n")
    serviceClass.write("    }\n\n")
    serviceClass.write("    @Override\n")
    serviceClass.write("    public void remove(Long " + className.lower() + "Id) {\n")
    serviceClass.write("        " + className.lower() + "Repository.deleteById(" + className.lower() + "Id);\n")
    serviceClass.write("    }\n\n")
    serviceClass.write("}")

def generateControllers(className, attributes):

    print(">> Generating controller for " + className)
    controllerClass = open(structure.controller + className + "Controller.java", "w+")

    controllerClass.write("import java.util.List;")
    controllerClass.write("import org.springframework.beans.factory.annotation.Autowired;\n")
    controllerClass.write("import org.springframework.http.HttpStatus;\n")
    controllerClass.write("import org.springframework.http.ResponseEntity;\n")
    controllerClass.write("import org.springframework.web.bind.annotation.DeleteMapping;\n")
    controllerClass.write("import org.springframework.web.bind.annotation.GetMapping;\n")
    controllerClass.write("import org.springframework.web.bind.annotation.PathVariable;\n")
    controllerClass.write("import org.springframework.web.bind.annotation.PostMapping;\n")
    controllerClass.write("import org.springframework.web.bind.annotation.PutMapping;\n")
    controllerClass.write("import org.springframework.web.bind.annotation.RequestBody;\n")
    controllerClass.write("import org.springframework.web.bind.annotation.RequestMapping;\n")
    controllerClass.write("import org.springframework.web.bind.annotation.RestController;\n\n")

    controllerClass.write("@RestController\n")
    controllerClass.write("@RequestMapping(value = \"/api/" + className.lower() + "\")\n")
    controllerClass.write("public class " + className + "Controller {\n\n")
    controllerClass.write("    @Autowired\n")
    controllerClass.write("    private " + className + "ServiceImpl " + className.lower() + "Service;\n\n")
    controllerClass.write("    @GetMapping\n")
    controllerClass.write("    public ResponseEntity<List<" + className + "DTO>> findAll() {\n")
    controllerClass.write("         List<" + className + "DTO> dtos = " + className.lower() + "Service.findAll();\n")
    controllerClass.write("         return new ResponseEntity<>(dtos, HttpStatus.OK);\n")
    controllerClass.write("    }\n\n")
    controllerClass.write("    @GetMapping(value = \"/{id}\")\n")
    controllerClass.write("    public ResponseEntity<" + className + "DTO> findById(@PathVariable(\"id\") Long id) {\n")
    controllerClass.write("        " + className + "DTO dtos = " + className.lower() + "Service.findById(id);\n")
    controllerClass.write("        return new ResponseEntity<>(dtos, HttpStatus.OK);\n")
    controllerClass.write("    }\n\n")
    controllerClass.write("    @PostMapping\n")
    controllerClass.write("    public ResponseEntity<" + className + "DTO> create(@RequestBody " + className + "DTO " + className.lower() + "DTO) {\n")
    controllerClass.write("        " + className + "DTO retVal = " + className.lower() + "Service.create(" + className.lower() + "DTO);\n")
    controllerClass.write("        return new ResponseEntity<>(retVal, HttpStatus.OK);\n")
    controllerClass.write("    }\n\n")
    controllerClass.write("    @PutMapping\n")
    controllerClass.write("    public ResponseEntity<" + className + "DTO> update(@RequestBody " + className + "DTO " + className.lower() + "DTO) {\n")
    controllerClass.write("        " + className + "DTO retVal = " + className.lower() + "Service.update(" + className.lower() + "DTO);\n")
    controllerClass.write("        return new ResponseEntity<>(retVal, HttpStatus.OK);\n")
    controllerClass.write("    }\n\n")
    controllerClass.write("    @DeleteMapping(value = \"/{id}\")\n")
    controllerClass.write("    public ResponseEntity<HttpStatus> delete(@PathVariable(\"id\") Long id) {\n")
    controllerClass.write("        " + className.lower() + "Service.remove(id);\n")
    controllerClass.write("        return new ResponseEntity<>(HttpStatus.OK);\n")
    controllerClass.write("    }\n\n")
    controllerClass.write("}")