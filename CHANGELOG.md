# Changelog

Todos los cambios notables en este proyecto están documentados en este archivo.

## [3.0.0] - 2025-12-08

### REFACTORIZACIÓN COMPLETA

**Breaking Changes**:
- Estructura completamente nueva organizada en directorios (src/)
- Requiere Python 3.7+ (anteriormente 3.6+)
- Nuevas dependencias: Pydantic 2.x, Rich 13.x, pydantic-settings 2.x
- Archivo principal reemplazado: usar `./run.sh` o `python -m src.main`
- Instalación automática con `./run.sh`

**Agregado**:
- **UI con Rich**: Tablas coloridas, paneles, progress bars y spinners
- **Modelos Pydantic**: Validación automática de datos con Job, SalaryInfo y SearchParameters
- **Código organizado**: Aproximadamente 30 archivos organizados en src/ (api/, models/, services/, ui/, utils/)
- **Sistema de Testing**: Tests con pytest, fixtures y objetivo de cobertura mayor a 80%
- **Instalación simplificada**: Script `./run.sh` configura todo automáticamente
- **Logging mejorado**: Sistema de logging sin duplicados con Rich
- **Type hints completos**: Mejor soporte de IDEs y mypy
- **Prompts interactivos**: Validación de inputs con Rich Prompt

**Mejorado**:
- **Código más corto**: Eliminada duplicación de código (aproximadamente 200 líneas)
- **Separación de responsabilidades**: Cada módulo menor a 300 líneas
- **Fácil mantenimiento**: Un archivo por responsabilidad
- **Testeable**: Cada componente testeable independientemente
- **Mejor documentación**: Docstrings completos en todos los módulos
- **Mejor UX**: Interfaz visual, spinners, confirmaciones interactivas

**Migración desde v2.x**:
1. Configurar archivo .env con tu API_KEY
2. Ejecutar: `./run.sh` (instala dependencias automáticamente)
3. El archivo antiguo fue eliminado (ya no es necesario)

---

## [2.0.0] - 2025-12-08

### Cambiado
- Migración de RapidAPI a OpenWeb Ninja API
- Variables de entorno renombradas: `RAPIDAPI_KEY` a `API_KEY`, `RAPIDAPI_HOST` a `API_HOST`
- Endpoint de API actualizado a `https://api.openwebninja.com/jsearch/search`
- Menú principal reorganizado con secciones: "Búsquedas Predefinidas" y "Funciones Adicionales"

### Agregado
- **NUEVAS FUNCIONALIDADES DE API**:
  - **Opción 11 - Detalles de trabajo por ID**: Obtención de información completa de cualquier trabajo usando su Job ID
  - **Opción 12 - Estimación de salarios**: Consulta de rangos salariales por puesto, ubicación y nivel de experiencia
  - **Opción 13 - Salarios por empresa**: Investigación de salarios de empresas específicas para roles determinados
  - Función `get_job_details()`: Endpoint `/jsearch/job-details`
  - Función `get_estimated_salary()`: Endpoint `/jsearch/estimated-salary` con 6 niveles de experiencia
  - Función `get_company_salary()`: Endpoint `/jsearch/company-job-salary`
  - Función `print_salary_info()`: Visualización formateada de información salarial
  - Funciones interactivas para cada nueva característica con validación de entrada

- **Sistema de logging completo**: Logs guardados en carpeta `logs/` con formato por día
- **Exportación a JSON**: Además de CSV, se pueden guardar resultados en formato JSON
- **Rate limiting automático**: Espera de 1 segundo entre peticiones para evitar límites de API
- **Reintentos automáticos**: Sistema de reintentos (máximo 3) con backoff exponencial
- **Mejor manejo de errores**:
  - Validación de parámetros de entrada
  - Manejo de errores HTTP específicos (429 Too Many Requests, etc.)
  - Timeout de 30 segundos en peticiones HTTP
  - Mensajes de error más descriptivos
- **Logging mejorado**: Registro detallado de todas las operaciones (búsquedas, errores, guardado de archivos)

### Mejorado
- **.gitignore**: Agregadas entradas para logs, caché y datos sensibles
- **Documentación**: README actualizado con nueva API y características
- **Código más robusto**: Uso de `pathlib.Path` para manejo de rutas
- **Sin emojis**: Emojis removidos de código y documentación

### Seguridad
- Mejor protección de archivos sensibles en .gitignore
- Validación de API keys antes de realizar peticiones

---

## [1.0.0] - Versión Original

### Inicial
- Script básico de scraping de trabajos de LinkedIn
- Menú interactivo en español
- 10 búsquedas predefinidas
- Exportación a CSV
- Integración con RapidAPI
