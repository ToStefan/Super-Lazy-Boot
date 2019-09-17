from utils import cap_first

def generate_enumeration(root_package, enum_name, list_of_enums):
	enums_string = ''
	for enum in list_of_enums:
		if list_of_enums.index(enum) == len(list_of_enums)-1: enums_string += "    " + enum + "\n"
		else: enums_string += "    " + enum + ",\n"
	return \
		f'package {root_package}.entity;\n\n' + \
		f'public enum {enum_name} ' + '{\n' + \
		enums_string + \
		'}'

def mapper_interface_template(root_package, collection, pagination = False):
	ret_val = \
		f'package {root_package}.web.mapper;\n\n'
	if(pagination):
		ret_val += 'import org.springframework.data.domain.Page;\n'
		ret_val += 'import org.springframework.data.domain.Pageable;\n'
		ret_val += f'import {root_package}.web.dto.PageDTO;\n'
	ret_val = ret_val + \
		'import java.util.Collection;\n' + \
		f'import java.util.{collection};\n\n' + \
		'public interface Mapper<E, DTO> {\n' + \
		'    DTO toDTO(E entity);\n' + \
		f'    {collection}<DTO> toDTO(Collection<E> entities);\n' + \
		'    DTO toDTOStripped(E entity);\n' + \
		f'    {collection}<DTO> toDTOStripped(Collection<E> entities);\n'
	if(pagination):
		ret_val += '    PageDTO<DTO> toPageDTO(Page<E> pages, Pageable pageable);\n'
	ret_val = ret_val + \
		'    E toEntityWithId(DTO dto);\n' + \
		'    E toEntity(DTO dto);\n' + \
		f'    {collection}<E> toEntity(Collection<DTO> dtos);\n' + \
		'}'
	return ret_val

def repository_template(root_package, e, primary_key_type):
	return \
		f'package {root_package}.repository;\n\n' + \
		'import org.springframework.data.jpa.repository.JpaRepository;\n' + \
		'import org.springframework.stereotype.Repository;\n' + \
		f'import {root_package}.entity.{e};\n\n' + \
		'@Repository\n' + \
		f'public interface {e}Repository extends JpaRepository<{e}, {primary_key_type}>' + '{\n\n' + \
		'}'

def service_impl_template(root_package, e, collection = "Set", lombok = False, pagination = False):
	e_low = e.lower()
	ret_val = \
		f'package {root_package}.service.impl;\n\n'
	if(pagination):
		ret_val += f'import {root_package}.web.dto.PageDTO;\n'
		ret_val += 'import org.springframework.data.domain.Pageable;\n'
	ret_val = ret_val + \
		f'import java.util.{collection};\n\n' + \
		'import org.springframework.stereotype.Service;\n' + \
		'import javax.transaction.Transactional;\n\n' + \
		f'import {root_package}.repository.{e}Repository;\n' + \
		f'import {root_package}.service.{e}Service;\n' + \
		f'import {root_package}.web.dto.{e}DTO;\n' + \
		f'import {root_package}.web.mapper.{e}Mapper;\n\n'
	if(lombok): ret_val = ret_val + \
		'import lombok.AllArgsConstructor;\n\n' + \
		'@AllArgsConstructor\n'
	ret_val = ret_val + \
		'@Transactional\n' + \
		'@Service\n' + \
		f'public class {e}ServiceImpl implements {e}Service ' + '{\n\n' + \
		f'    private final {e}Repository {e_low}Repository;\n' + \
		f'    private final {e}Mapper {e_low}Mapper;\n\n'
	if(not lombok): ret_val = ret_val + \
		f'    public {e}ServiceImpl({e}Repository {e_low}Repository, {e}Mapper {e_low}Mapper) ' + '{\n' + \
		f'    	this.{e_low}Repository = {e_low}Repository;\n' + \
		f'    	this.{e_low}Mapper = {e_low}Mapper;\n' + \
		'    }\n\n'

	findAll = \
		'    @Override\n' + \
		f'    public {collection}<{e}DTO> findAll() ' + '{\n' + \
		f'        return {e_low}Mapper.toDTOStripped({e_low}Repository.findAll());\n' + \
		'    }\n\n'

	if(not pagination):
		findAllPagination = ''
	else:
		findAllPagination = \
			'    @Override\n' + \
			f'    public PageDTO<{e}DTO> findAll(Pageable pageable) ' + '{\n' + \
			f'        return {e_low}Mapper.toPageDTO({e_low}Repository.findAll(pageable), pageable);\n' + \
			'	}\n\n'

	findById = \
		'    @Override\n' + \
		f'    public {e}DTO findById(Long id) ' + '{\n' + \
		f'        return {e_low}Mapper.toDTO({e_low}Repository.getOne(id));\n' + \
		'    }\n\n'

	create = \
		'    @Override\n' + \
		f'    public {e}DTO create({e}DTO {e_low}DTO) ' + '{\n' + \
		f'        return {e_low}Mapper.toDTO({e_low}Repository.save({e_low}Mapper.toEntity({e_low}DTO)));\n' + \
		'    }\n\n'

	update = \
		'    @Override\n' + \
		f'    public {e}DTO update({e}DTO {e_low}DTO) ' + '{\n' + \
		f'        return {e_low}Mapper.toDTO({e_low}Repository.save({e_low}Mapper.toEntityWithId({e_low}DTO)));\n' + \
		'    }\n\n'

	delete = \
		'    @Override\n' + \
		f'    public void remove(Long {e_low}Id) ' + '{\n' + \
		f'        {e_low}Repository.deleteById({e_low}Id);\n' + \
		'    }\n\n'

	return ret_val + findAll + findAllPagination + findById + create + update + delete + "}"

def service_template(root_package, e, collection = 'Set', pagination = False):
	ret_val = \
		f'package {root_package}.service;\n\n'
	if(pagination):
		ret_val += 'import org.springframework.data.domain.Pageable;\n'
		ret_val += f'import {root_package}.web.dto.PageDTO;\n'
	ret_val = ret_val + \
		f'import java.util.{collection};\n' + \
		f'import {root_package}.web.dto.{e}DTO;\n\n' + \
		f'public interface {e}Service ' + '{\n' + \
		f'    {collection}<{e}DTO> findAll();\n'
	if(pagination):
		ret_val += f'    PageDTO<{e}DTO> findAll(Pageable pageable);\n'
	ret_val = ret_val + \
		f'    {e}DTO findById(Long id);\n' + \
		f'    {e}DTO create({e}DTO jobDTO);\n' + \
		f'    {e}DTO update({e}DTO jobDTO);\n' + \
		'    void remove(Long id);\n' + \
		'}'
	return ret_val

def controller_template(root_package, e, collection = "Set", lombok = False, pagination = False):
	e_low = e.lower()
	ret_val = \
		f'package {root_package}.web.controller;\n\n' + \
		f'import java.util.{collection};\n\n' + \
		'import org.springframework.http.HttpStatus;\n' + \
		'import org.springframework.http.ResponseEntity;\n' + \
		'import org.springframework.web.bind.annotation.DeleteMapping;\n' + \
		'import org.springframework.web.bind.annotation.GetMapping;\n' + \
		'import org.springframework.web.bind.annotation.PathVariable;\n' + \
		'import org.springframework.web.bind.annotation.PostMapping;\n' + \
		'import org.springframework.web.bind.annotation.PutMapping;\n' + \
		'import org.springframework.web.bind.annotation.RequestBody;\n' + \
		'import org.springframework.web.bind.annotation.RequestMapping;\n' + \
		'import org.springframework.web.bind.annotation.RestController;\n\n' + \
		f'import {root_package}.service.impl.{e}ServiceImpl;\n' + \
		f'import {root_package}.web.dto.{e}DTO;\n\n'
	if(pagination):
		ret_val += f'import {root_package}.web.dto.PageDTO;\n'
		ret_val += 'import org.springframework.data.domain.Pageable;\n'
	if(lombok): ret_val = ret_val + \
		'import lombok.AllArgsConstructor;\n\n' + \
		'@AllArgsConstructor\n'
	ret_val = ret_val + \
		'@RestController\n' + \
		f'@RequestMapping(value = "/api/{e_low}")\n' + \
		f'public class {e}Controller ' + '{\n\n' + \
		f'    private final {e}ServiceImpl {e_low}Service;\n\n'
	if(not lombok) : ret_val = ret_val + \
		f'    public {e}Controller({e}ServiceImpl {e_low}Service) ' + '{\n' + \
		f'    	this.{e_low}Service = {e_low}Service;\n' + \
		'    }\n\n'

	findAll =  \
		'    @GetMapping\n' + \
		f'    public ResponseEntity<{collection}<{e}DTO>> findAll()' + ' {\n' + \
		f'         {collection}<{e}DTO> retVal = {e_low}Service.findAll();\n' + \
		'         return new ResponseEntity<>(retVal, HttpStatus.OK);\n' + \
		'    }\n\n'

	if(not pagination):
		findAllPagination = ''
	else:
		findAllPagination = \
			'    @GetMapping(value = "/pages")\n' + \
			f'    public ResponseEntity<PageDTO<{e}DTO>> findAllByPages(Pageable pageable) ' + '{\n' + \
			f'        PageDTO<{e}DTO> retVal = {e_low}Service.findAll(pageable);\n' + \
			f'        return new ResponseEntity<PageDTO<{e}DTO>>(retVal, HttpStatus.OK);\n' + \
			'    }\n\n'

	findById = \
		'    @GetMapping(value = "/{id}")\n' + \
		f'    public ResponseEntity<{e}DTO> findById(@PathVariable("id") Long id)' + ' {\n' + \
		f'        {e}DTO retVal = {e_low}Service.findById(id);\n' + \
		'        return new ResponseEntity<>(retVal, HttpStatus.OK);\n' + \
		'    }\n\n'

	create = \
		'    @PostMapping\n' + \
		f'    public ResponseEntity<{e}DTO> create(@RequestBody {e}DTO {e_low}DTO) ' + '{\n' + \
		f'        {e}DTO retVal = {e_low}Service.create({e_low}DTO);\n' + \
		'        return new ResponseEntity<>(retVal, HttpStatus.OK);\n' + \
		'    }\n\n'

	update = \
		'    @PutMapping\n' + \
		f'    public ResponseEntity<{e}DTO> update(@RequestBody {e}DTO {e_low}DTO) ' + '{\n' + \
		f'        {e}DTO retVal = {e_low}Service.update({e_low}DTO);\n' + \
		'        return new ResponseEntity<>(retVal, HttpStatus.OK);\n' + \
		'    }\n\n'

	delete = \
		'    @DeleteMapping(value = "/{id}")\n' + \
		'    public ResponseEntity<HttpStatus> delete(@PathVariable("id") Long id) {\n' + \
		f'        {e_low}Service.remove(id);\n' + \
		'        return new ResponseEntity<>(HttpStatus.OK);\n' + \
		'    }\n\n'

	return ret_val + findAll + findAllPagination + findById + create + update + delete + '}'

def entity_template(root_package, e, attributes_list_of_tupples, lombok = False):
	def generate_getter(field, field_type):
		return \
			f'    public {field_type} get{cap_first(field)}() ' + '{\n' + \
			f'        return this.{field};\n' + \
			'    }\n\n'

	def generate_setter(field, field_type):
		return \
			f'    public void set{cap_first(field)}({field_type} {field}) ' + '{\n' + \
			f'        this.{field} = {field};\n' + \
			'    }\n\n'

	# Imports and Class Header
	list_import = False
	date_import = False
	ret_val = f'package {root_package}.entity;\n\n'
	for a in attributes_list_of_tupples:
		if((a[2] == "list" or a[2] == "set") and list_import != True):
			ret_val += f'import java.util.{cap_first(a[2])};\n\n'
			list_import = True
		if(a[2] == "date" and date_import != True):
			ret_val += f'import java.time.{a[3]};\n\n'
			date_import = True
	if(lombok): ret_val += 'import lombok.Data;\n\n'
	ret_val += 'import javax.persistence.*;\n\n'
	if(lombok): ret_val += '@Data\n'
	ret_val = ret_val + \
		'@Entity\n' + \
		f'@Table(name = "{e.lower()}")\n' + \
		f'public class {e} ' + '{\n\n'

			#field_type --> normal, id, enum, class, list, set
			#field_type_value --> Enumeration, Long, String, List<Entity>, Set
			#relation --> OneToMany, ManyToOne, ManyToMany, OneToOne
	def generate_entity_field(field_name, field_name_sql, field_type, field_type_value, 
					nullable = "false", relation = False, fetch = "LAZY", cascade = "ALL"):
		field = ''
		if(field_type == 'id'):
			field += '    @Id\n'
			field += '    @GeneratedValue(strategy = GenerationType.IDENTITY)\n'
		if(field_type == "normal" or field_type == "date"):
			field += f'    @Column(name = "{field_name_sql}", nullable = {nullable})\n'
		if(field_type == "enum"):
			field += '    @Enumerated(EnumType.STRING)\n'
			field += f'    @Column(name = "{field_name_sql}", nullable = {nullable})\n'
		if(relation != False):
			if(relation == "ManyToOne"):
				field += f'    @ManyToOne(fetch = FetchType.{fetch}, cascade = CascadeType.{cascade})\n'
				field += f'    @JoinColumn(name = "{field_name_sql}", nullable = {nullable})\n'
			if(relation == "OneToMany"):
				field += f'    @OneToMany(mappedBy = "{e.lower()}", fetch = FetchType.{fetch}, cascade = CascadeType.{cascade})\n'
			if(relation == "ManyToMany"):
				join = field_name_sql.split("_")[0] + "_id"
				inverse_join = field_name_sql.split("_")[1] + "_id"
				field += f'    @ManyToMany(fetch = FetchType.{fetch})\n'
				field += f'    @JoinTable(name = "{field_name_sql}", joinColumns = @JoinColumn(name = "{join}"),\n'
				field += f'            inverseJoinColumns = @JoinColumn(name = "{inverse_join}"))\n'
			if(relation == "OneToOne"):
				field += f'    @OneToOne(targetEntity = {field_type_value}.class, fetch = FetchType.{fetch})\n'
				field += f'    @JoinColumn(name = "{field_name_sql}", nullable = {nullable})\n'
		field += f'    private {field_type_value} {field_name};\n\n'
		return field

	# Attributes
	for each in attributes_list_of_tupples:
		ret_val += generate_entity_field(each[0], each[1], each[2], each[3], each[4], each[5], each[6], each[7])

	# Getters / Setters & Default constructor
	if(not lombok):
		ret_val = ret_val + \
			f'    public {e}()' + '{\n\n' + \
			'    }\n\n'
		for each in attributes_list_of_tupples:
			ret_val += generate_getter(each[0], each[3])
			ret_val += generate_setter(each[0], each[3])

	return ret_val + "}"

def page_dto_template(root_package, lombok = False):
	attributes_list = [
		('currentPage', 'Integer'), 
		('itemsPerPage', 'Integer'), 
		('totalItems', 'Long'), 
		('items', 'Collection<T>')
	]
	def generate_page_dto_getter(att, java_type):
		return \
			f'    public {java_type} get{cap_first(att)}() ' + '{\n' + \
			f'        return this.{att};\n' + \
			'	}\n\n'

	def generate_page_dto_setter(att, java_type):
		return \
			f'    public void set{cap_first(att)}({java_type} {att}) ' + '{\n' + \
			f'        this.{att} = {att};\n' + \
			'	}\n\n'

	ret_val = \
		f'package {root_package}.web.dto;\n\n' + \
		'import java.util.Collection;\n\n'
	if(lombok):
		ret_val = ret_val + \
			'import lombok.AllArgsConstructor;\n' + \
			'import lombok.Getter;\n' + \
			'import lombok.NoArgsConstructor;\n' + \
			'import lombok.Setter;\n\n' + \
			'@Getter\n' + \
			'@Setter\n' + \
			'@AllArgsConstructor\n' + \
			'@NoArgsConstructor\n'
	ret_val = ret_val + \
		'public class PageDTO<T> {\n\n' + \
		'	private Integer currentPage;\n' + \
		'	private Integer itemsPerPage;\n' + \
		'	private Long totalItems;\n' + \
		'	private Collection<T> items;\n\n'

	if(not lombok):
		ret_val = ret_val + \
			'    public PageDTO() {\n\n    }\n\n' + \
			'    public PageDTO(Integer currentPage, Integer itemsPerPage, Long totalItems, Collection<T> items) {\n' + \
			'		this.currentPage = currentPage;\n' + \
			'		this.itemsPerPage = itemsPerPage;\n' + \
			'		this.totalItems = totalItems;\n' + \
			'		this.items = items;\n' + \
			'	}\n\n'
		for a in attributes_list:
			ret_val += generate_page_dto_getter(a[0], a[1])
			ret_val += generate_page_dto_setter(a[0], a[1])

	ret_val += '}\n'
	return ret_val

def dto_template(root_package, e, attributes_list_of_tupples, lombok = False):
	def generate_dto_field(field, f_type, field_type):
		if(field_type == "class"):
			return f'    private {f_type} {field};\n' + \
					f'    private Long {field}Id;\n'
		else:
			return f'    private {f_type} {field};\n'
	def generate_dto_setter(field, f_type, field_type):
		if(field_type == "class"):
			ret_val = \
				f'    public {f_type} get{cap_first(field)}() ' + '{\n' + \
				f'        return this.{field};\n' + \
				'    }\n\n' + \
				f'    public Long get{cap_first(field)}Id() ' + '{\n' + \
				f'        return this.{field}Id;\n' + \
				'    }\n\n'
			return ret_val
		return \
			f'    public {f_type} get{cap_first(field)}() ' + '{\n' + \
			f'        return this.{field};\n' + \
			'    }\n\n'

	def generate_dto_getter(field, f_type, field_type):
		if(field_type == "class"):
			ret_val = \
				f'    public void set{cap_first(field)}({f_type} {field}) ' + '{\n' + \
				f'        this.{field} = {field};\n' + \
				'    }\n\n' + \
				f'    public void set{cap_first(field)}Id(Long {field}Id) ' + '{\n' + \
				f'        this.{field}Id = {field}Id;\n' + \
				'    }\n\n'
			return ret_val
		return \
			f'    public void set{cap_first(field)}({f_type} {field}) ' + '{\n' + \
			f'        this.{field} = {field};\n' + \
			'    }\n\n'

	ret_val = f'package {root_package}.web.dto;\n\n'
	list_import = False
	set_import = False
	date_import = False

	for att in attributes_list_of_tupples:
		if(att[2] == "class" or att[2] == "enum"):
			ret_val += f'import {root_package}.entity.{att[3]};\n\n'
		if(att[2] == "list" and list_import != True):
			ret_val += f'import java.util.{cap_first(att[2])};\n\n'
			list_import = True
		if(att[2] == "list" and "<" in att[3]):
			to_import_entity = att[3].split("<")[1].split(">")[0]
			ret_val += f'import {root_package}.entity.' + to_import_entity + ";\n"
		if(att[2] == "set" and set_import != True):
			ret_val += f'import java.util.{cap_first(att[2])};\n\n'
			set_import = True
		if(att[2] == "date" and date_import != True):
			ret_val += f'import java.time.{att[3]};\n\n'
			date_import = False

	if(lombok): ret_val = ret_val + \
		'import lombok.Getter;\n' + \
		'import lombok.Setter;\n' + \
		'import lombok.NoArgsConstructor;\n\n' + \
		'@Getter\n@Setter\n@NoArgsConstructor\n'
	ret_val =  ret_val + \
		f'public class {e}DTO ' + '{\n\n'

	# Attributes
	for att in attributes_list_of_tupples:
		ret_val += generate_dto_field(att[0], att[3], att[2])

	# Getters / Setters & Default constructor
	ret_val += "\n"
	if(not lombok):
		ret_val += f'    public {e}DTO()' + '{\n\n    }\n\n'
		for att in attributes_list_of_tupples:
			ret_val += generate_dto_getter(att[0], att[3], att[2])
			ret_val += generate_dto_setter(att[0], att[3], att[2])

	return ret_val + "}"

def mapper_template(root_package, e, attributes_list_of_tupples, collection, pagination = False):
	# Imports and class header
	ret_val = \
		f'package {root_package}.web.mapper;\n\n'
	if(pagination):
		ret_val = ret_val + \
			'import org.springframework.data.domain.Page;\n' + \
			'import org.springframework.data.domain.Pageable;\n' + \
			f'import {root_package}.web.dto.PageDTO;\n'
	ret_val = ret_val + \
		'import java.util.Collection;\n' + \
		f'import java.util.{collection};\n' + \
		f'import java.util.stream.Collectors;\n' + \
		'import org.springframework.stereotype.Component;\n' + \
		f'import {root_package}.entity.{e};\n' + \
		f'import {root_package}.web.dto.{e}DTO;\n\n' + \
		'@Component\n' + \
		f'public class {e}Mapper implements Mapper<{e}, {e}DTO> ' + '{\n\n'

	# toDTO
	to_dto = \
		'    @Override\n' + \
		f'    public {e}DTO toDTO({e} entity) ' + '{\n' + \
		f'        {e}DTO dto = new {e}DTO();\n'
	for a in attributes_list_of_tupples: to_dto += f'        dto.set{cap_first(a[0])}(entity.get{cap_first(a[0])}());\n'
	to_dto = to_dto + \
		'        return dto;\n' + \
		'    }\n\n'

	# toDTO (Collection)
	to_dto_collection = \
		'    @Override\n' + \
		f'    public {collection}<{e}DTO> toDTO(Collection<{e}> entities) ' + '{\n' + \
		'        return entities\n' + \
		'                    .stream()\n' + \
		f'                    .map({e.lower()} -> toDTO({e.lower()}))\n' + \
		f'                    .collect(Collectors.to{collection}());\n' + \
		'    }\n\n'

	# toDTOStripped
	to_dto_stripped = \
		'    @Override\n' + \
		f'    public {e}DTO toDTOStripped({e} entity) ' + '{\n' + \
		f'        {e}DTO dto = new {e}DTO();\n'
	for a in attributes_list_of_tupples:
		if(a[2] != "list" and a[2] != "set"):
			if(a[2] == "class"):
				to_dto_stripped += f'        dto.set{cap_first(a[0])}Id(entity.get{cap_first(a[0])}().getId());\n'
			else:
				to_dto_stripped += f'        dto.set{cap_first(a[0])}(entity.get{cap_first(a[0])}());\n'
	to_dto_stripped = to_dto_stripped + \
		'        return dto;\n' + \
		'    }\n\n'

	# toDTOStripped (Collection)
	to_dto_stripped_collection = \
		'    @Override\n' + \
		f'    public {collection}<{e}DTO> toDTOStripped(Collection<{e}> entities) ' + '{\n' + \
		'        return entities\n' + \
		'                    .stream()\n' + \
		f'                    .map({e.lower()} -> toDTOStripped({e.lower()}))\n' + \
		f'                    .collect(Collectors.to{collection}());\n' + \
		'    }\n\n'

	# ToPageDTO
	if(pagination):
		to_page_dto = \
			'    @Override\n' + \
			f'    public PageDTO<{e}DTO> toPageDTO(Page<{e}> pages, Pageable pageable) ' + '{\n' + \
			f'        return new PageDTO<{e}DTO>(pageable.getPageNumber(), \n' + \
			'                pageable.getPageSize(), \n' + \
			'                pages.getTotalElements(), \n' + \
			'                toDTOStripped(pages.getContent()));\n' + \
			'    }\n\n'
	else:
		to_page_dto = ''

	# toEntity
	to_entity = \
		'    @Override\n' + \
		f'    public {e} toEntity({e}DTO dto) ' + '{\n' + \
		f'        {e} entity = new {e}();\n'
	for a in attributes_list_of_tupples: 
		if(a[2] != "id"): 
			to_entity += f'        entity.set{cap_first(a[0])}(dto.get{cap_first(a[0])}());\n'
	to_entity = to_entity + \
		'        return entity;\n' + \
		'    }\n\n'

	# toEntityWithId
	to_entity_with_id = \
		'    @Override\n' + \
		f'    public {e} toEntityWithId({e}DTO dto) ' + '{\n' + \
		f'        {e} entity = new {e}();\n'
	for a in attributes_list_of_tupples: to_entity_with_id += f'        entity.set{cap_first(a[0])}(dto.get{cap_first(a[0])}());\n'
	to_entity_with_id = to_entity_with_id + \
		'        return entity;\n' + \
		'    }\n\n'

	# toEntity (Collection)
	to_entity_collection = \
		'    @Override\n' + \
		f'    public {collection}<{e}> toEntity(Collection<{e}DTO> dtos) ' + '{\n' + \
		'        return dtos\n' + \
		'                    .stream()\n' + \
		f'                    .map({e.lower()} -> toEntity({e.lower()}))\n' + \
		f'                    .collect(Collectors.to{collection}());\n' + \
		'    }\n\n'

	return ret_val + to_dto + to_dto_collection + to_dto_stripped + to_dto_stripped_collection + \
			to_page_dto + to_entity + to_entity_with_id + to_entity_collection + '}'
