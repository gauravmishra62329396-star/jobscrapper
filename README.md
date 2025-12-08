# LinkedIn Job Scraper v3.0

Script interactivo en español para buscar ofertas de trabajo de LinkedIn mediante la API JSearch de OpenWeb Ninja. El proyecto utiliza Pydantic para validación de datos y Rich para la interfaz de consola.

**Autor:** Hex686f6c61
**Versión:** 3.0.0
**Python:** 3.7+

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Testing](#testing)
- [Solución de Problemas](#solución-de-problemas)

## Características

Este proyecto ofrece una solución completa para la búsqueda y análisis de ofertas de trabajo de LinkedIn, con capacidades avanzadas de filtrado y exportación de datos.

### Búsqueda de trabajos

La funcionalidad principal del scraper permite realizar búsquedas personalizadas y predefinidas con múltiples opciones de filtrado:

- Menú interactivo en español con 10 búsquedas predefinidas
- API Key almacenada de forma segura en archivo .env
- Exportación de resultados en formato CSV y JSON
- Búsquedas por país (España, Estados Unidos, Reino Unido, etc.)
- Filtros por tipo de empleo (tiempo completo, parcial, contratista)
- Filtros por fecha de publicación
- Filtros de trabajo remoto

### Funciones avanzadas

Además de las búsquedas básicas, el sistema incluye funcionalidades avanzadas para obtener información detallada:

- Obtención de detalles completos de trabajo por ID
- Consulta de rangos salariales por puesto y ubicación
- Consulta de salarios de empresas específicas
- Comparación salarial por nivel de experiencia

### Sistema

El scraper está diseñado con robustez y confiabilidad en mente, implementando múltiples medidas de protección:

- Logging completo con archivos de registro
- Rate limiting automático
- Reintentos automáticos (hasta 3 intentos)
- Validación de parámetros
- Timeout de 30 segundos en peticiones HTTP

## Requisitos

Para ejecutar este proyecto necesitas tener instalado Python y una API Key válida de OpenWeb Ninja:

- Python 3.7 o superior
- API Key de OpenWeb Ninja ([Obtener aquí](https://www.openwebninja.com/))

## Instalación

```bash
# 1. Clonar el proyecto
git clone <repositorio>
cd linkedIN-Jobs-Scrapper

# 2. Configurar API key
cp .env.example .env
# Editar .env y añadir tu API_KEY

# 3. Ejecutar
./run.sh
```

El script `run.sh` realiza las siguientes operaciones de forma automática:
- Crea el entorno virtual si no existe
- Instala las dependencias necesarias
- Verifica la configuración
- Ejecuta la aplicación

## Uso

### Ejecución

```bash
# Opción recomendada
./run.sh

# Alternativa: ejecución manual
source venv/bin/activate
python -m src.main
```

### Capturas de pantalla

A continuación se muestran ejemplos visuales de la interfaz de usuario del scraper en funcionamiento, mostrando las diferentes funcionalidades disponibles:

**Menú principal:**

![Menú principal](assets/01%20LinkedIN%20Job%20Scraper%20CLI.png)

**Búsqueda predefinida - Project Manager:**

![Project Manager España](assets/02%20Project%20Manager%20Spain.png)

**Consulta de salarios:**

![Salarios Software Engineer](assets/03%20Software%20Engineer%20Salario.png)

**Búsqueda personalizada:**

![Búsqueda personalizada](assets/04%20Busqueda%20personalizada.png)

### Menú principal

Al ejecutar el script se muestra el menú principal con las siguientes opciones:

**Búsquedas predefinidas:**
1. Búsqueda personalizada
2. Project Manager - España
3. Software Engineer - España
4. Data Scientist - España
5. Frontend Developer - España
6. Backend Developer - Estados Unidos
7. Machine Learning Engineer - Estados Unidos
8. Full Stack Developer - Estados Unidos
9. DevOps Engineer - Reino Unido
10. Senior Software Engineer - Remoto global

**Funciones adicionales:**
11. Obtener detalles de un trabajo por ID
12. Consultar salarios estimados por puesto
13. Consultar salarios de empresa específica

0. Salir

### Búsqueda personalizada

La opción 1 del menú permite crear búsquedas completamente personalizadas ajustando cada parámetro según tus necesidades específicas:

- Query de búsqueda
- Código de país (es, us, gb, etc.)
- Período de publicación (todos, hoy, 3 días, semana, mes)
- Filtro de trabajo remoto
- Tipo de empleo (FULLTIME, CONTRACTOR, PARTTIME, INTERN)
- Número de páginas (1-10)

### Detalles de trabajo (Opción 11)

Esta función permite obtener información completa y detallada de una oferta de trabajo específica utilizando su Job ID único. Los detalles incluyen:

- Descripción completa del puesto
- Requisitos (experiencia, educación, habilidades)
- Beneficios
- Enlaces de aplicación
- Información salarial (si disponible)
- Fechas de publicación

### Consulta de salarios (Opciones 12 y 13)

El sistema ofrece dos modalidades para consultar información salarial, permitiendo comparar rangos según diferentes criterios:

**Opción 12 - Salarios estimados:**

Obtiene estimaciones salariales generales del mercado para un puesto específico:

- Título del puesto
- Ubicación
- Años de experiencia (todos, menos de 1 año, 1-3, 4-6, 7-9, 10+)

**Opción 13 - Salarios por empresa:**

Consulta información salarial específica de una empresa en particular:

- Nombre de la empresa
- Título del puesto
- Ubicación (opcional)
- Años de experiencia

## Estructura del proyecto

El proyecto sigue una arquitectura modular bien organizada que separa las responsabilidades en diferentes directorios:

```
linkedin-job-scraper/
├── src/              # Código fuente
├── config/           # Búsquedas predefinidas
├── tests/            # Tests con pytest
├── output/           # Resultados exportados
└── logs/             # Archivos de registro
```

## Testing

El proyecto incluye una suite completa de tests con pytest y cobertura del 100%.

### Ejecución de tests

Para ejecutar los tests del proyecto, primero instala las dependencias de desarrollo y luego utiliza pytest con las siguientes opciones:

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Opción recomendada: usar el script automatizado
./tests/run_tests.sh

# Alternativa: ejecutar todos los tests manualmente
pytest

# Ejecutar con reporte de cobertura
pytest --cov=src --cov-report=html

# Ejecutar tests específicos
pytest tests/test_models/
pytest tests/test_services/
pytest tests/test_api/
pytest tests/test_ui/
```

### Estructura de tests

Los tests están organizados en módulos que reflejan la estructura del código fuente, facilitando el mantenimiento y la identificación de tests específicos:

```
tests/
├── conftest.py              # Fixtures compartidos
├── test_api/                # Tests de capa API
│   ├── test_client.py
│   ├── test_jsearch_client.py
│   └── test_rate_limiter.py
├── test_models/             # Tests de modelos Pydantic
│   ├── test_job.py
│   ├── test_salary.py
│   └── test_search_params.py
├── test_services/           # Tests de servicios
│   ├── test_job_service.py
│   ├── test_salary_service.py
│   └── test_export_service.py
├── test_ui/                 # Tests de interfaz
│   ├── test_console.py
│   ├── test_formatters.py
│   ├── test_menu.py
│   └── test_prompts.py
└── test_utils/              # Tests de utilidades
    ├── test_config.py
    ├── test_file_utils.py
    └── test_logger.py
```

### Estadísticas de cobertura

El proyecto mantiene una cobertura de código del 100% en todos los módulos testeables, garantizando la calidad y confiabilidad del código:

- Total de tests: 291
- Cobertura de código: 100% (excluyendo main.py)
- Líneas cubiertas: 805/805
- Todos los módulos con cobertura completa

## Parámetros disponibles

A continuación se detallan los parámetros que puedes utilizar para personalizar tus búsquedas y filtrar los resultados según tus necesidades.

### Códigos de país

La API soporta búsquedas en múltiples países utilizando códigos ISO de dos letras:

| Código | País |
|--------|------|
| es | España |
| us | Estados Unidos |
| gb | Reino Unido |
| de | Alemania |
| fr | Francia |
| nl | Países Bajos |
| ca | Canadá |
| au | Australia |
| mx | México |
| ar | Argentina |
| co | Colombia |
| cl | Chile |

### Tipos de empleo

Puedes filtrar las ofertas según el tipo de contratación que te interese:

- FULLTIME: Tiempo completo
- CONTRACTOR: Contratista
- PARTTIME: Tiempo parcial
- INTERN: Prácticas

### Períodos de publicación

Filtra las ofertas según la fecha en que fueron publicadas para obtener resultados más recientes:

- all: Todos
- today: Hoy
- 3days: Últimos 3 días
- week: Última semana
- month: Último mes

## Estructura de archivos de salida

El sistema exporta automáticamente los resultados de las búsquedas en formatos CSV y JSON, facilitando el análisis posterior de los datos.

### Formato de nombres

Los archivos se guardan automáticamente en el directorio `output/` con el siguiente formato:

```
{query}_{timestamp}.{formato}
```

Cada archivo incluye la consulta realizada y un timestamp para evitar sobrescrituras. Ejemplos reales de archivos generados:

```
output/project_manager_scrum_agile_20251208_140810.csv
output/python_deloper_spain_20251208_141212.csv
output/python_deloper_spain_20251208_141213.json
output/salary_Software_Engineer_20251208_140922.json
```

### Archivos CSV

Los archivos CSV son ideales para análisis en hojas de cálculo o herramientas de Business Intelligence. Incluyen las siguientes columnas:

- job_id: Identificador único del trabajo
- job_title: Título del puesto
- employer_name: Nombre de la empresa
- job_city, job_state, job_country: Ubicación
- job_is_remote: Indicador de trabajo remoto
- job_employment_type: Tipo de empleo (FULLTIME, PARTTIME, etc.)
- job_min_salary, job_max_salary: Rango salarial
- job_salary_currency, job_salary_period: Moneda y período del salario
- job_description: Descripción completa del puesto
- job_apply_link: URL para aplicar
- job_posted_at_datetime: Fecha de publicación

Ejemplo de contenido CSV:

```csv
job_id,job_title,employer_name,job_city,job_country,job_is_remote,job_employment_type
abc123,Senior Python Developer,Tech Corp,Madrid,Spain,False,FULLTIME
```

### Archivos JSON

Los archivos JSON proporcionan una estructura de datos más rica y anidada, ideal para procesamiento programático. Contienen la misma información que los CSV pero con mejor legibilidad y soporte para estructuras complejas:

```json
[
  {
    "job_id": "abc123xyz",
    "title": "Senior Python Developer",
    "employer_name": "Tech Corp",
    "city": "Madrid",
    "country": "Spain",
    "is_remote": false,
    "employment_type": "FULLTIME",
    "min_salary": 45000.0,
    "max_salary": 65000.0,
    "salary_currency": "EUR",
    "salary_period": "YEAR",
    "description": "Buscamos un desarrollador Python Senior...",
    "apply_link": "https://example.com/apply",
    "posted_at_datetime": "2025-12-08T10:00:00Z"
  }
]
```

### Archivos de salarios

Las consultas de información salarial se exportan exclusivamente en formato JSON, incluyendo datos agregados de múltiples fuentes:

```json
[
  {
    "job_title": "Software Engineer",
    "location": "Madrid, Spain",
    "publisher_name": "Glassdoor",
    "min_salary": 35000.0,
    "max_salary": 65000.0,
    "median_salary": 50000.0,
    "salary_currency": "EUR",
    "salary_period": "YEAR"
  }
]
```

## Solución de problemas

A continuación se detallan los errores más comunes y sus soluciones para facilitar la resolución de problemas.

### Error: "API Key no configurada"

Este error indica que el archivo .env no está configurado correctamente. Verificar que el archivo .env existe y contiene la API key:

```bash
ls -la .env
cat .env
```

Asegurar que no hay espacios extra en la configuración.

### Error: "No module named 'pydantic_settings'"

Este error indica que faltan dependencias por instalar. Ejecutar los siguientes comandos:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "No se encontraron trabajos"

Si no se encuentran resultados, puedes probar las siguientes soluciones:

- Utilizar una búsqueda más general
- Verificar el código del país
- Probar con un período de tiempo más amplio
- Algunos países tienen menos ofertas disponibles

### Error de conexión o timeout

Los errores de conexión pueden deberse a varios factores. Verifica lo siguiente:

- Verificar conexión a internet
- Confirmar que la API key es válida
- Revisar límites del plan en OpenWeb Ninja
- Intentar con menos páginas

### Límites de la API

El sistema implementa medidas de protección para evitar superar los límites de la API:

- El sistema implementa espera automática de 1 segundo entre peticiones
- Reintentos automáticos: 3 intentos por defecto
- Búsquedas con múltiples páginas consumen más créditos

## Seguridad

Es importante mantener la seguridad de tu API key y datos sensibles siguiendo estas recomendaciones:

- No subir el archivo .env a Git
- No compartir la API key públicamente
- El archivo .gitignore protege archivos sensibles

## Notas

Ten en cuenta las siguientes consideraciones al utilizar el scraper:

- Los resultados dependen de lo que Google Jobs indexa
- No todos los trabajos incluyen información salarial
- La información de trabajo remoto puede no ser exacta
- Algunos trabajos pueden aparecer en múltiples búsquedas

## Licencia

Uso libre con fines educativos y personales.
