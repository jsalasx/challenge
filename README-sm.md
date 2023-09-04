# Desafío de ingeniero de software (ML y LLM)

## Descripción general

Bienvenido al desafío de aplicaciones **Ingeniero de software (ML y LLM)**. En este tendrás la oportunidad de acercarte a una parte de la realidad del rol, y demostrar tus habilidades y conocimientos en aprendizaje automático y nube.

## Problema

Se ha proporcionado un cuaderno jupyter (`exploration.ipynb`) con el trabajo de un Data Scientist (en adelante, el DS). El DS entrenó un modelo para predecir la probabilidad de **retraso** de un vuelo que despega o aterriza en el aeropuerto SCL. El modelo fue entrenado con datos públicos y reales, a continuación te brindamos la descripción del conjunto de datos:

|Columna|Descripción|
|-----|-----------|
|`Fecha-I`|Fecha y hora previstas del vuelo.|
|`Vlo-I`|Número de vuelo programado.|
|`Ori-I`|Código de ciudad de origen programado.|
|`Des-I`|Código de ciudad de destino programado.|
|`Emp-I`|Código de línea aérea del vuelo programado.|
|`Fecha-O`|Fecha y hora de operación del vuelo.|
|`Vlo-O`|Número de operación del vuelo.|
|`Ori-O`|Código de ciudad origen de la operación.|
|`Des-O`|Código de ciudad destino de la operación.|
|`Emp-O`|Código de la aerolínea del vuelo operado.|
|`DIA`|Día del mes de operación del vuelo.|
|`MES`|Número del mes de operación del vuelo.|
|`AÑO`|Año de operación del vuelo.|
|`DIANOM`|Día de la semana de operación del vuelo.|
|`TIPOVUELO`|Tipo de vuelo, I =Internacional, N =Nacional.|
|`OPERA`|Nombre de la aerolínea que opera.|
|`SIGLAORI`|Nombre ciudad de origen.|
|`SIGLADES`|Nombre de la ciudad de destino.|

Además, el DS consideró relevante la creación de las siguientes columnas:

|Columna|Descripción|
|-----|-----------|
|`high_season`|1 si `Fecha-I` es entre el 15 de diciembre y el 3 de marzo, o el 15 de julio y el 31 de julio, o el 11 de septiembre y el 30 de septiembre, 0 en caso contrario.|
|`min_diff`|diferencia en minutos entre `Fecha-O` y `Fecha-I`|
|`period_day`|mañana (entre las 5:00 y las 11:59), tarde (entre las 12:00 y las 18:59) y noche (entre las 19:00 y las 4:59), según `Date-I`.|
|`delay`|1 si `min_diff` > 15, 0 si no.|

## Desafío

### Instrucciones

1. Cree un repositorio en **github** y copie todo el contenido del desafío en él. Recuerda que el repositorio debe ser **público**.

2. Utilice la rama **principal** para cualquier versión oficial que debamos revisar. Se recomienda encarecidamente utilizar prácticas de desarrollo de [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow). **NOTA: no elimines tus ramas de desarrollo.**
   
3. Por favor, no cambies la estructura del desafío (nombres de carpetas y archivos).
   
4. Toda la documentación y explicaciones que tengas que darnos deben ir en el archivo `challenge.md` dentro de la carpeta `docs`.

5. Para enviar su desafío, debe realizar una solicitud `POST` a:
     `https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/software-engineer`
     Este es un ejemplo del `body` que debes enviar:
     ```json
     {
       "nombre": "Juan Pérez",
       "correo": "juan.perez@ejemplo.com",
       "github_url": "https://github.com/juanperez/latam-challenge.git",
       "api_url": "https://juan-perez.api"
     }
     ```
     ##### ***POR FAVOR, ENVÍE LA SOLICITUD UNA VEZ.***

     Si su solicitud fue exitosa, recibirá este mensaje:
     ```json
     {
       "estado": "OK",
       "detalle": "su solicitud fue recibida"
     }
     ```


***NOTA: Recomendamos enviar el desafío incluso si no lograste terminar todas las partes.***

### Contexto:

Necesitamos poner en funcionamiento el trabajo de ciencia de datos para el equipo del aeropuerto. Para ello, hemos decidido habilitar una `API` en la que puedan consultar la predicción de retraso de un vuelo.

*Recomendamos leer el desafío completo (todas sus partes) antes de comenzar a desarrollarlo.*

### Parte I

Para poner en funcionamiento el modelo, transcriba el archivo `.ipynb` al archivo `model.py`:

- Si encuentra algún error, corríjalo.
- Al final, DS propuso algunos modelos. Elija el mejor modelo a su discreción, argumente por qué. **No es necesario realizar mejoras al modelo.**
- Aplicar todas las buenas prácticas de programación que considere necesarias en este tema.
- El modelo debe pasar las pruebas ejecutando `make model-test`.

> **Nota:**
> - **No puedes** eliminar o cambiar el nombre o los argumentos de los métodos **proporcionados**.
> - **Puedes** cambiar/completar la implementación de los métodos proporcionados.
> - **Puedes** crear las clases y métodos adicionales que consideres necesarios.

### Parte II

Implemente el modelo en una `API` con `FastAPI` usando el archivo `api.py`.

- La "API" debe pasar las pruebas ejecutando "make api-test".

> **Nota:**
> - **No puedes** usar otro marco.

### Parte III

Implemente la `API` en su proveedor de nube favorito (recomendamos usar GCP).

- Coloque la URL de la `API` en el `Makefile` (`línea 26`).
- La "API" debe pasar las pruebas ejecutando "make stress-test".

> **Nota:**
> - **Es importante que la API esté implementada hasta que revisemos las pruebas.**

### Parte IV

Estamos buscando una implementación adecuada de "CI/CD" para este desarrollo.

- Crea una nueva carpeta llamada `.github` y copia la carpeta `workflows` que proporcionamos dentro de ella.
- Complete tanto `ci.yml` como `cd.yml` (considere lo que hizo en las partes anteriores).