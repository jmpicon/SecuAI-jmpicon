"""
Genera audio MP3 a partir del guion adaptado del manual SecuAI.

Un MP3 por capítulo, en español, con voz natural (gTTS).
El guion está adaptado a un tono oral: explicaciones, no comandos literales.
"""
from pathlib import Path
from gtts import gTTS

OUT = Path("/home/jmpicon/Documentos/secu_IA/taller/audio")
OUT.mkdir(exist_ok=True)


# =====================================================
# GUION ADAPTADO AL OIDO
# =====================================================
# Reglas:
# - Sin comandos literales. Se describe QUE hace, no COMO se escribe.
# - Bloques cortos. Una idea por frase.
# - Pausas marcadas con dos puntos seguidos o saltos.
# - Tono podcast: cercano, primera persona.

PROLOGO = """
Bienvenido al manual de audio de SecuAI: herramientas para atacar y defender
sistemas de inteligencia artificial. Soy José Picón.

Este audio es una versión adaptada del manual escrito. He quitado los
comandos literales, porque no se aprenden escuchándolos, y he conservado
las ideas, los criterios para elegir cada herramienta y las cosas que he
aprendido por las malas. Si en algún momento quieres copiar y pegar un
comando, abre el PDF del manual, está todo allí. El audio es para que
entiendas el panorama mientras vas en el coche, paseando o haciendo deporte.

Voy a contarte tres cosas en este prólogo.

Primera: este manual sale de un curso que doy. Después de tres ediciones me
di cuenta de que los alumnos volvían siempre con la misma pregunta:
"Vale, ya entiendo qué es prompt injection y por qué importa. Ahora dime
qué pongo el lunes en mi empresa". Las slides estaban llenas de marcos
teóricos pero ninguna respondía a esa pregunta concreta. Este audio sí
intenta responderla.

Segunda: ninguna de las herramientas que vamos a ver, por sí sola, te da
seguridad. La gente que viene de ciberseguridad clásica ya sabe esto. La
que viene de machine learning generativo a veces no. La seguridad de
inteligencia artificial se monta por capas. Un escáner que filtra el
input, un clasificador que da una segunda opinión, el modelo en medio,
otro escáner que limpia la salida, otro clasificador sobre esa salida, un
escáner de modelos antes de cargarlos, una suite de red teaming en
integración continua, métricas en producción. Cada herramienta cubre una
superficie y deja huecos en otras. Si solo montas una, has avanzado un
poco. Si montas cuatro o cinco bien combinadas, has avanzado mucho.

Tercera: el repositorio público con todos los ejemplos está en GitHub,
en jmpicon barra SecuAI guion jmpicon. Si quieres ver los scripts
completos o tirar de copia y pega, es la fuente de verdad.

Empezamos.
"""


CH1 = """
Capítulo uno. Antes de empezar.

La parte aburrida. No la saltes. Si te lo montas mal aquí, vas a perder
treinta minutos por cada herramienta peleándote con dependencias de Python
que no debería ser tu problema.

¿Qué necesitas en tu máquina? Python tres punto diez o posterior. Docker.
Node.js si vas a tocar Promptfoo. Git para clonar el repositorio. Pipx para
instalar las herramientas de línea de comandos cada una en su entorno
aislado. Si nunca has usado pipx, ahora es el momento.

Una clave de OpenAI es útil pero no imprescindible. Si no quieres pagar o
trabajas offline, puedes usar Ollama, que es la forma más cómoda de
ejecutar modelos abiertos en local. Llama tres de ocho mil millones de
parámetros o phi tres mini te cubren el ochenta por ciento de lo que
vamos a hacer.

Una GPU NVIDIA acelera bastante los modelos locales. Sin GPU, en CPU
moderna, los clasificadores tardan dos o tres segundos por consulta. Para
iterar mientras aprendes está bien. Para producción ya hablaremos.

Sobre la instalación de Python: la regla simple es que cada herramienta
tiene sus dependencias y, si las metes todas en el Python del sistema, en
una semana tendrás conflictos imposibles de resolver. Crea un entorno
virtual con venv para las librerías que importas en tu código, y usa pipx
para las herramientas de línea de comandos como Garak, Promptfoo o
ModelScan, que viven solas en su propio entorno.

Sobre Ollama, hay dos formas de instalarlo: nativa, directamente en el
sistema, o en Docker. Para una máquina dedicada, como tu portátil, una
estación de trabajo o una máquina virtual con Kali Linux, te recomiendo la
instalación nativa. Menos capas, menos sorpresas, menos memoria gastada en
virtualización. En Kali, que es distribución basada en Debian, el script
oficial funciona sin tocar nada: descargas, ejecutas, y queda corriendo
como servicio del sistema.

La instalación en Docker la uso cuando quiero aislar la instalación, en
máquinas donde no quiero ensuciar el sistema, o en pipelines de
integración continua. En una máquina virtual no merece la pena: la
máquina virtual ya es tu sandbox.

Una vez Ollama responde, descargas modelos. Te recomiendo tres: llama tres
de ocho mil millones de parámetros para uso general, phi tres mini, que
es más pequeño y rápido para iterar payloads, y llama guard tres, que es
un clasificador defensivo y se va a convertir en una pieza importante de
nuestro stack. Cada modelo ocupa entre dos y cinco gigabytes en disco y
otros tantos en memoria cuando está cargado. Si tu máquina virtual tiene
ocho gigabytes asignados, quédate con phi tres mini, va sobrado.

Antes de pasar al siguiente capítulo, verifica que todo funciona: Python
con versión correcta, Docker respondiendo si lo vas a usar, Ollama
respondiendo en su puerto, las variables de entorno cargadas, y el
repositorio clonado. Si algo falla, párate y arréglalo. Te ahorrarás
dolor más adelante.
"""


CH2_INTRO = """
Capítulo dos. Atacar.

Si vienes de pentesting clásico, este es tu capítulo cómodo. Las
herramientas de aquí son el equivalente de nmap o de burp aplicado a
modelos de lenguaje. Lanzan ataques contra un sistema externo, te dicen
cuántos colaron y, en el mejor caso, generan un informe que puedes
enseñar a alguien.

La elección entre las siete herramientas que vamos a ver depende de tres
preguntas. Primera: ¿tienes acceso solo a un endpoint, o tienes los pesos
del modelo? Si solo tienes el endpoint, hablamos de caja negra; si tienes
los pesos, hablamos de caja blanca. Garak, PyRIT, Promptfoo y HarmBench
funcionan en caja negra. TextAttack y ART necesitan caja blanca.

Segunda pregunta: ¿una sola consulta o varias en cadena? Garak y Promptfoo
asumen que cada ataque se resuelve en un único intercambio. PyRIT está
pensado para atacar en varios turnos, ideal cuando hay autenticación,
estado conversacional o agentes con memoria.

Tercera pregunta: ¿quién consume el resultado? Si es tu equipo técnico,
cualquiera vale. Si es un CISO o un regulador, los informes HTML de Garak
y los números de HarmBench son los que se leen como datos serios.

Mi recomendación para empezar es Garak. Es el menos sofisticado de los
siete pero el que más utilidad te da con menos esfuerzo en la primera
semana.
"""


CH2_GARAK = """
Sección dos punto uno. Garak.

Garak es escáner de vulnerabilidades para modelos de lenguaje. Lo
desarrolla NVIDIA y está liberado bajo licencia Apache. La analogía con
nmap es bastante fiel: un comando, un objetivo, una lista de sondas, y un
informe al final. Las sondas, en jerga de Garak, se llaman probes. Trae
más de ochenta listas para usar.

Lo uso casi siempre como primer paso. Cuando un cliente o un compañero me
dice "hemos desplegado un chatbot, ¿le pegas un vistazo?", lo primero que
hago es lanzar Garak con tres o cuatro familias de probes y mirar qué
sale. Tarda media hora, da una foto razonable y produce un HTML que
puedes mandar por correo. A partir de ahí decido si hace falta algo más
fino.

¿Cómo se lee el resultado? Garak imprime, por cada probe, los intentos
totales y los que consiguieron saltar las defensas. El cociente entre
ambos es la métrica clave: ASR, attack success rate, tasa de éxito de
ataque. Mi regla rápida: por debajo del cinco por ciento lo considero
verde, aceptable para producción si el resto del stack hace su trabajo.
Entre cinco y veinte por ciento es amarillo, normalmente se mitiga con un
scanner de input. Por encima del veinte por ciento no despliego.

Garak se puede apuntar contra OpenAI, Anthropic, modelos locales con
Ollama, modelos de HuggingFace, y endpoints REST genéricos. Para
endpoints custom, donde tu modelo vive detrás de tu propio wrapper, le
pasas un archivo JSON describiendo la API y Garak se encarga de traducir.

Para que Garak deje de ser un test puntual y se convierta en parte de tu
ciclo de desarrollo, hay que enchufarlo a integración continua. En el
repositorio del manual tienes un workflow de GitHub Actions completo que
lo ejecuta en cada pull request y bloquea el merge si el ASR sube del
umbral que definas.

Una advertencia. La primera vez que dejé Garak corriendo con la opción
para ejecutar todos los probes contra una API de pago, me llegó una
factura de ochenta dólares por una ejecución de cuatro horas. La lección:
empieza con un conjunto acotado y mide el coste antes de generalizar.
Reducir el número de generaciones por probe divide el coste por cinco y
rara vez cambia las conclusiones.
"""


CH2_PYRIT = """
Sección dos punto dos. PyRIT.

PyRIT viene del equipo de red team de Microsoft. La liberaron en dos mil
veinticuatro. Donde Garak es "rocía y mide", PyRIT es "orquesta". La
diferencia importa cuando el ataque no se resuelve en un solo
intercambio: cuando tienes que establecer contexto en el primer turno,
abrir una vía en el segundo y ejecutar la operación destructiva en el
tercero. Garak no sabe hacer eso. PyRIT sí.

La pieza central de PyRIT son los orchestrators, los orquestadores. Cada
uno encapsula una lógica de ataque: enviar prompts en serie, ataque
adaptativo con un modelo rojo que aprende del feedback del modelo
víctima, jailbreak por escalada gradual, y unos cuantos más. Tú compones
objetivos, scorers, y un target. El scorer es cómo decides si el ataque
tuvo éxito; puede ser otro modelo de lenguaje que actúa como juez, o un
clasificador entrenado. Todo lo que pasa se guarda en una base de datos
local, así puedes auditar después.

¿Cuándo saco PyRIT? Cuando el sistema que tengo que evaluar es un agente
con varias herramientas, o un asistente con memoria. En esos casos los
ataques de un solo turno te dan información parcial: el modelo te rechaza
el primer intento porque suena agresivo, pero acepta el tercero porque ya
hay contexto. Garak no captura esa dinámica. PyRIT sí.

También cuando el target tiene autenticación y sesiones, porque PyRIT te
permite escribir Python sin atascarte en adaptadores REST. Si necesitas
mantener una cookie a lo largo de una conversación, lo metes en una
función y listo.

La parte más interesante de PyRIT es el modo red team adaptativo. Le das
un objetivo en lenguaje natural, le das un modelo de lenguaje que actuará
como atacante, y el sistema genera prompts iterativamente según las
respuestas del modelo víctima, hasta el máximo de turnos que indiques.
Cuando funciona, es vagamente inquietante: ves al modelo rojo cambiar de
estrategia entre turnos en respuesta a los rechazos.
"""


CH2_PROMPTFOO = """
Sección dos punto tres. Promptfoo.

Promptfoo es la herramienta que recomiendo a equipos que no son
exclusivamente de Python. Todo se configura en YAML, se ejecuta con un
único comando de Node y produce un dashboard navegable. He visto a
product managers leer y modificar archivos de Promptfoo sin ayuda de un
ingeniero. Eso, en este nicho, no es trivial.

Tiene tres modos de uso. El primero es evaluación de prompts: pruebas
varias variantes del mismo prompt contra varios modelos y comparas la
calidad. El segundo es testing por aserciones: defines reglas como "la
respuesta no debe contener API_KEY", o "debe pasar este criterio
evaluado por otro modelo", y el sistema te dice cuáles fallan. El
tercero, el más interesante para este manual, es el red team automático:
Promptfoo genera adversariales contra tu sistema con dieciséis plugins
distintos. Plugins que cubren contenido dañino, fuga de información
personal, extracción de prompt, secuestro de agente, exceso de agencia,
alucinación, control de acceso por roles, e inyección SQL en herramientas.

Las aserciones más útiles son: contains y not contains, para texto
literal; regex para patrones; llm-rubric, donde otro modelo evalúa según
un criterio en lenguaje natural; similar, similitud por embeddings, útil
cuando quieres "se parece a esto"; y cost y latency, para fallar si la
respuesta cuesta demasiado o tarda demasiado.

Promptfoo es lo que pongo en integración continua cuando trabajo con un
equipo que no se maneja con Python. La integración es trivial: una línea
en el workflow, un script que extrae el pass rate y falla el job si baja
del noventa por ciento.

Una advertencia con la opción llm-rubric: si usas el mismo modelo
evaluado como juez, el sesgo es brutal. El modelo se aprueba a sí mismo.
Cambia el juez a otro modelo distinto.
"""


CH2_TEXTATTACK = """
Sección dos punto cuatro. TextAttack.

TextAttack es de otra escuela. Las tres herramientas anteriores son de
caja negra: solo necesitan un endpoint. TextAttack es de caja blanca:
necesita acceso a los logits del modelo, a sus probabilidades internas.
En la práctica, eso significa que la uso para clasificadores propios.
Detectores de spam, de toxicidad, de phishing. Donde tengo los pesos del
modelo y puedo guiar la búsqueda de perturbaciones. Para modelos grandes
accesibles solo por API no aplica.

La parte interesante son las recipes, las recetas: implementaciones
completas de ataques publicados en papers académicos. La más conocida es
TextFooler, que sustituye palabras por sinónimos hasta que el
clasificador cambia su predicción. BAE usa BERT para sugerir las
sustituciones. DeepWordBug introduce typos a nivel carácter. Si tienes
que escribir un paper de robustez o convencer a alguien con literatura,
son los nombres a citar.

Donde TextAttack se gana el sueldo es en adversarial training,
entrenamiento adversarial: generas adversariales con ella, los etiquetas
correctamente, los metes en el dataset y reentrenas. El modelo resultante
es más robusto a los mismos tipos de ataque. Esto sirve para
clasificadores propios. Para modelos grandes de lenguaje la historia es
otra y muchísimo más cara.
"""


CH2_ART = """
Sección dos punto cinco. Adversarial Robustness Toolbox, conocido como
ART.

ART es el toolkit más completo de adversariales clásicos. Lo desarrolla
IBM bajo el paraguas de Trusted AI. Cubre cuatro familias de ataques.
Evasión, engañar al modelo en inferencia. Envenenamiento, corromper el
training set. Extracción, robar el modelo. E inferencia, sacar información
del training set; sí, eso es posible. Soporta TensorFlow, Keras, PyTorch,
scikit-learn, LightGBM y XGBoost.

Lo recomiendo cuando tu pipeline de machine learning no es solo
transformers. Si trabajas con visión por ordenador, datos tabulares,
scoring de fraude, etcétera, ART es lo que sigue cubriendo la superficie.
Para modelos de lenguaje puros, Garak y PyRIT son más útiles.

Un ejemplo concreto del impacto: con un ataque de evasión clásico, FGSM,
sobre un clasificador de imágenes que parte de un noventa y siete por
ciento de precisión, puedes hacer caer la precisión hasta el catorce por
ciento metiendo perturbaciones que un humano ni nota. Ese es el número
que más asusta a la gente cuando se lo enseñas.

Sobre envenenamiento con backdoor: el modelo se comporta normalmente con
datos benignos, pero con un disparador específico, por ejemplo un cuadrado
de cuatro píxeles en una esquina, clasifica todo lo que vea como una
etiqueta concreta. En un escenario real de cadena de suministro, alguien
podría subir un modelo con backdoor a un hub público y tú cargarlo sin
darte cuenta. De ahí el capítulo cuatro de este manual, donde hablamos de
ModelScan y safetensors.
"""


CH2_HARMBENCH_COUNTERFIT = """
Sección dos punto seis y dos punto siete. HarmBench y Counterfit.

HarmBench no es para usar todos los días. Es un benchmark formal:
cuatrocientos comportamientos dañinos predefinidos, veintidós ataques
implementados, dieciocho modelos evaluados de referencia. El valor está
en obtener números comparables con el resto de la literatura. Si vas a
vender un servicio de modelo de lenguaje al sector público o si publicas
un modelo, HarmBench te da el lenguaje común. Para el día a día, Garak es
lo que usas.

Counterfit es un CLI interactivo, con estética parecida a Metasploit, que
envuelve ataques de ART, TextAttack y otras librerías. Lo desarrolló
Microsoft en su día. Su mejor momento ya pasó: la última actualización
seria es de dos mil veintidós y desde entonces se ha quedado detrás. Lo
menciono por completitud. Si te encuentras un entorno donde alguien ya lo
tiene montado, sigue siendo útil. Si vas a empezar de cero, usa ART o
PyRIT directamente.
"""


CH3_INTRO_LLMGUARD = """
Capítulo tres. Defender.

La regla mental que uso para defender modelos de lenguaje es la misma que
para cualquier otro sistema: no busques la herramienta perfecta, monta
capas. Un scanner de input que filtre lo obvio antes de llamar al modelo.
Un clasificador que dé una segunda opinión sobre la entrada. El modelo en
medio. Un scanner de output que sanitice la respuesta. Un clasificador
sobre la salida. Si el modelo puede ejecutar acciones, una capa de
intervención humana para las que pasan de cierto umbral. Y auditoría de
todo.

La latencia total con las defensas locales son entre doscientos y
cuatrocientos milisegundos extra. Aceptable para casi cualquier chatbot.
Si necesitas menos de cien milisegundos, sustituyes los scanners basados
en modelos por reglas rápidas, regex o análisis sintáctico. Funciona pero
deja huecos.

Sección tres punto uno. LLM Guard.

Si tuviera que elegir una sola herramienta defensiva para empezar, es
esta. LLM Guard trae más de veinte scanners listos para usar, se instala
con un comando de pip y se integra con FastAPI en unos minutos. La
pipeline es siempre la misma: escaneas el input, llamas al modelo,
escaneas el output. Cada scanner devuelve un texto saneado, un booleano
"pasa o no pasa", y un score numérico.

Los scanners que uso de verdad sobre el input son cinco. PromptInjection,
que detecta jailbreaks con un modelo de HuggingFace entrenado para esa
tarea, con razonable acierto. Anonymize, que quita información personal
identificable, usando Presidio por debajo. Secrets, que detecta claves de
API y tokens. TokenLimit, que corta entradas desorbitadas. Y BanTopics, un
clasificador zero-shot contra una lista negra de temas.

Sobre el output, mis cuatro favoritos son: Deanonymize, el par de
Anonymize, que restaura la información personal original tras la
respuesta del modelo; Sensitive, que detecta información sensible en la
salida; NoRefusal, que falla si el modelo rehúsa, útil para validar que
los prompts legítimos sí pasan; y MaliciousURLs, que detecta enlaces
maliciosos.

El truco que hace utilizable todo esto se llama Vault, la bóveda. Cuando
Anonymize reemplaza por ejemplo un email por una etiqueta tipo "email
redactado uno", guarda la correspondencia. Cuando el modelo responde con
la versión saneada y pasas la salida por Deanonymize, el email original
vuelve. El usuario nunca nota que se anonimizó por debajo, y el modelo
nunca vio el dato real.

Una advertencia importante para producción: los scanners basados en
modelos cargan modelos de HuggingFace al instanciarse. Si los creas
dentro del handler de cada petición, tu latencia se va a pique y tu
factura también. Instánciaalos al startup de la aplicación y reutilízalos.
Son thread-safe.
"""


CH3_NEMO_LLAMAGUARD = """
Sección tres punto dos. NeMo Guardrails.

NeMo Guardrails es la pieza que elijo cuando en el equipo hay producto
que necesita leer y modificar las reglas, no solo desarrolladores. El
lenguaje específico que usa se llama Colang y se parece bastante a
inglés. Defines intents, intenciones del usuario, como por ejemplo
"cuándo está preguntando por la competencia". Defines respuestas
predefinidas que el bot da en cada caso. Y defines flujos que conectan
unas con otras.

La separación es elegante: las reglas de seguridad y las reglas de
producto viven en el mismo archivo y se editan con las mismas
herramientas. No hace falta tocar Python para añadir un caso bloqueado.

Hay tres tipos de rails, de barreras, en NeMo. Input rails, que validan
la entrada del usuario. Dialog rails, que controlan el flujo
conversacional. Y output rails, que validan la salida del modelo. Los
tres se combinan.

Donde NeMo me ha dado problemas es en intents demasiado parecidos. Si
defines "pregunta por competidores" y "pregunta por precios", el modelo
puede confundirlos. La solución es añadir más ejemplos por intent, cinco
o seis paráfrasis distintas, y diferenciarlos explícitamente.

Sección tres punto tres. Llama Guard tres.

Llama Guard tres es un modelo de la familia Llama, de ocho mil millones
de parámetros, que Meta finetuneó específicamente para clasificar mensajes
como seguros o no seguros. Devuelve además la categoría violada, de la S
uno a la S catorce en su taxonomía. No es un chatbot. Lo uso como gate
antes y después del modelo principal, no como modelo conversacional.

Las catorce categorías van desde violencia y crímenes no violentos hasta
explotación sexual de menores, discurso de odio, suicidio y autolesión,
elecciones y abuso del intérprete de código. Para reportes de
cumplimiento normativo, esa taxonomía es útil porque mapea bien a lo que
regulan el reglamento europeo de inteligencia artificial y otras normas
similares.

La trampa que conviene conocer: Llama Guard considera "consejo médico
especializado" una categoría a vigilar, la S seis. Si tu aplicación es
legítimamente médica, tienes que ajustar el system prompt de Llama Guard
o aceptar el falso positivo. Lo aviso para que no te sorprenda en el
primer despliegue.

El patrón completo es: clasificas el input del usuario; si es no seguro,
respondes con un mensaje canned; si es seguro, llamas al modelo principal;
clasificas la respuesta del modelo; si la respuesta es no segura, también
respondes con un mensaje canned. Doble gate. La latencia añadida es de
unos doscientos milisegundos por gate en CPU. Si tienes GPU, baja a unos
treinta.
"""


CH3_RESTO = """
Sección tres punto cuatro. Rebuff.

Rebuff es interesante porque combina cuatro capas en una sola
herramienta. Primera: heurística, regex y reglas baratas. Segunda: un
modelo de lenguaje como juez, otro modelo decide si el input es una
inyección. Tercera: una base de datos vectorial, similitud con ataques
conocidos previos. Cuarta, y donde Rebuff aporta algo distinto: canary
tokens.

Un canary token, o token canario, es una palabra única e improbable que
insertas en tu system prompt. Si esa palabra aparece en la respuesta del
modelo, significa que el modelo ha leído el system prompt y lo ha
incluido en la salida. En otras palabras: el atacante ha conseguido una
fuga. Lo detectas en tiempo real y bloqueas la respuesta.

Sección tres punto cinco. Vigil.

Vigil cumple un nicho concreto: dejar de obligar a tu aplicación a ser
Python. Corre como sidecar, expone una API REST y tu aplicación, escrita
en Node, Go, Java o lo que sea, le habla por HTTP. Si tu stack no es
Python en primer lugar, Vigil te ahorra reescribir media aplicación.

La parte que me gusta de Vigil es que soporta reglas YARA. Si ya tienes
gente de seguridad escribiendo YARA para malware, pueden contribuir
reglas para prompts dañinos sin aprender una herramienta nueva.

Sección tres punto seis. Presidio.

Presidio detecta y anonimiza datos personales en texto: emails,
teléfonos, IBANs, tarjetas de crédito, IPs, direcciones, nombres, DNIs,
NIEs, NIFs, y unas cuarenta entidades más. Es multi-idioma. Es crítico
para cualquier aplicación que toque el reglamento europeo de protección
de datos.

Lo uso casi siempre indirectamente: LLM Guard incluye un scanner
Anonymize que internamente es Presidio. Pero a veces lo saco directo
cuando necesito detección sobre logs antes de indexarlos, o sobre un
dataset de entrenamiento antes de pasarlo a un proveedor externo.

A veces necesitas detectar algo que no está en la lista de cajón. Por
ejemplo, identificadores de empleado con formato propio. Presidio te
permite añadir un reconocedor personalizado: defines un patrón regex y,
opcionalmente, palabras de contexto. El contexto es la parte interesante:
si el modelo encuentra el patrón en una frase que menciona "empleado" o
"identificador", el score sube. Si lo encuentra sin ese contexto, lo
trata con más escepticismo.

Sección tres punto siete. Guardrails AI.

Guardrails AI tiene un planteamiento distinto. En lugar de scanners
sueltos, ofrece un framework con un hub público de validadores, más de
sesenta a fecha de este manual, y un mecanismo llamado re-ask: si la
salida no pasa la validación, Guardrails automáticamente le pide al
modelo que reformule, pasándole el error como contexto.

El re-ask es caro: dobla las llamadas en el peor caso. Pero útil cuando
la salida tiene que cumplir un esquema estricto. Si lo que quieres es
JSON válido con ciertos campos, Guardrails es elegante.
"""


CH4 = """
Capítulo cuatro. Lo que descargas: pickle y compañía.

Una de las cosas que más me cuesta convencer a equipos que vienen de
machine learning puro es esto. El formato pickle de Python, que es lo que
está por debajo de torch dot load y de muchas otras funciones parecidas,
ejecuta código al deserializar. No es un bug. Es una funcionalidad del
lenguaje. El método __reduce__ de un objeto permite que cualquier código
Python se ejecute cuando ese objeto se carga desde un archivo.

Consecuencia práctica: si descargas un archivo de modelo de internet, un
repositorio público, un foro, un BitTorrent, una versión antigua en un
bucket, y lo cargas con torch dot load, el creador del archivo puede
ejecutar lo que quiera en tu máquina. Borrar archivos, abrir una shell
inversa, exfiltrar credenciales del entorno, lo que sea. En dos mil
veinticuatro HuggingFace catalogó más de cien casos de modelos
maliciosos subidos a su hub. No fueron casos teóricos. Fueron archivos
descargados por usuarios reales.

Las tres herramientas de este capítulo son tu defensa.

Sección cuatro punto uno. ModelScan.

ModelScan analiza archivos de modelo en múltiples formatos detectando
código embebido peligroso. Soporta pickle, h cinco de Keras, TensorFlow
SavedModel, PyTorch, ONNX, GGUF, y safetensors. Lo uso en integración
continua antes de cualquier carga de pesos, y en pre-commit hooks en
repositorios donde haya gente colaborando.

Hay tres modos de uso típicos. Escanear un archivo local. Escanear un
directorio recursivamente. Y, especialmente útil, escanear un repositorio
de HuggingFace sin descargarlo localmente. Esto último es oro: te ahorra
tener que bajar gigabytes para descubrir que el modelo está infectado.

Sección cuatro punto dos. picklescan.

Picklescan es más estrecho que ModelScan: analiza pickle, nada más. A
cambio es liviano y no arrastra dependencias pesadas. Útil para
pre-commit hooks o para escaneos rápidos en pipelines que ya tienen
muchas herramientas.

Sección cuatro punto tres. safetensors.

Safetensors es la solución real, no un parche. Un formato de
serialización de tensores diseñado por HuggingFace para ser seguro: no
ejecutable, solo datos. Rápido: usa mapeo de memoria sin copia. Y
verificable: incluye checksums en el header. Es el formato por defecto
hoy de Llama, Mistral, Mixtral, Gemma y prácticamente todos los modelos
publicados en HuggingFace desde dos mil veinticuatro.

Convertir de pickle a safetensors es trivial: tres líneas de Python.
Cargar safetensors es igual de trivial pero sin riesgo de ejecución
remota de código.

Mi política para equipos nuevos: ningún modelo en pickle entra al
repositorio. Si llega uno, porque alguien lo descarga de un sitio que
solo lo ofrece en ese formato, se convierte antes de hacer commit. En
integración continua, una búsqueda de archivos pkl o pt que devuelva
cualquier resultado falla el build. Drástico pero limpio.
"""


CH5 = """
Capítulo cinco. Cómo lo monto todo junto.

Una herramienta aislada no defiende nada. Lo que defiende es el pipeline.
Este capítulo es cómo encajan las piezas de los tres capítulos anteriores
en un sistema real.

El stack defensivo en producción tiene ocho capas. Cada petición pasa por
todas ellas, en orden. Primera capa: autenticación y rate limiting, tu
API gateway de toda la vida. Segunda capa: LLM Guard sobre el input;
sanea, detecta secretos y datos personales. Tercera capa: Llama Guard
sobre el input; clasifica seguro o no seguro. Cuarta capa: el modelo
principal; genera la respuesta. Quinta capa: LLM Guard sobre el output;
re-anonimiza y sanea la salida. Sexta capa: Llama Guard sobre el output;
clasifica la respuesta. Séptima capa: intervención humana para acciones
críticas, como mover dinero o tocar datos sensibles. Octava capa:
auditoría, todo a un sistema de logs centralizado.

Las capas siete y ocho no son negociables. Cualquier acción que toque
dinero o datos sensibles necesita humano antes de ejecutarse. Cualquier
petición necesita dejar rastro auditado, con identificador único, versión
del system prompt y del modelo. Cuando algo se rompe en producción a las
tres de la mañana, lo único que tienes para entender qué pasó es ese log.

Cuatro métricas a reportar al menos cada semana. ASR, attack success
rate, sobre tu suite de test; objetivo, menos del cinco por ciento. FPR,
false positive rate, sobre tráfico legítimo; objetivo, menos del uno por
ciento. P95 de latencia con defensas activas comparado con sin defensas;
objetivo, menos de trescientos milisegundos extra. Y coste extra por
los scanners basados en modelos; objetivo, menos del veinticinco por
ciento sobre el coste base.

Quiero detenerme en el FPR, el ratio de falsos positivos. Es el que más
se descuida y el que más quema al equipo de producto. Si tu defensa
molesta a un cinco por ciento de usuarios legítimos, en producción a
escala se transforma en cientos de quejas al día. La gente acaba pidiendo
desactivar la defensa, y entonces no tienes defensa. Mide el FPR desde el
día uno.

Sobre la cadencia de red teaming, la prueba ofensiva: cada pull request,
Garak en modo smoke, cincuenta prompts, dos minutos de integración
continua. Cada release, suite completa de Garak más Promptfoo, unos
treinta minutos. Mensualmente, red team manual creativo por un ingeniero,
un día de su tiempo. En producción de forma continua, un subconjunto
canario sobre el cinco por ciento del tráfico. Y anualmente, pentest
externo por proveedor especializado.

El mensual creativo es importante y se olvida. Garak y Promptfoo
encuentran lo que ya saben buscar. Un humano con tiempo y curiosidad
encuentra cosas nuevas. Reserva un día al mes para que alguien del
equipo, idealmente rotando, intente romper tu sistema sin guión.
"""


CH6 = """
Capítulo seis. Si solo tienes diez horas.

A veces el día a día no da. Hay un proyecto que sale el lunes, no hay
margen para hacerlo bien, pero tampoco quieres salir desnudo. Este
capítulo es para esa situación. Lo que pondría yo en diez horas de un
ingeniero, sin coste de licencias, cubriendo los riesgos top del OWASP
LLM Top diez con cobertura razonable.

Por orden de prioridad.

Primero: ModelScan. Lo metes como pre-commit hook y como paso en
integración continua para cualquier modelo descargado. Treinta minutos
de configuración. Te protege contra el peor de los casos: que descargues
un modelo malicioso y te dé shell remoto en tu propio servidor.

Segundo: LLM Guard. Tres scanners en el input de tu API: PromptInjection,
Anonymize y Secrets. Tres horas de integración. Filtras los ataques más
comunes y proteges la información personal.

Tercero: Llama Guard tres. Lo levantas en Ollama local y montas la
función de gate antes y después del modelo principal. Dos horas. Doble
clasificación safe o unsafe sobre input y output.

Cuarto: Garak. Smoke test semanal en GitHub Actions con tres familias de
probes: promptinject, encoding y dan. Una hora de configuración. Te
detecta regresiones cuando alguien cambia el system prompt.

Quinto: Promptfoo. Regresiones por pull request con aserciones YAML,
incluido en integración continua. Dos horas. Te permite documentar y
testear casos concretos que han fallado antes.

Sexto: Presidio. Anonimizador de información personal en español, si tu
aplicación procesa datos personales. Una hora y media.

Total: menos de diez horas. Coste de licencias: cero. Cobertura: las seis
primeras categorías del OWASP LLM Top diez mitigadas razonablemente. Las
cuatro siguientes parcialmente. No es perfecto pero es muchísimo mejor
que la línea base de la mayoría de equipos que despliegan modelos de
lenguaje hoy.

Cuando este stack está arriba y mides bien, lo siguiente que añado es
Rebuff con canary tokens sobre el system prompt. Tarda otros treinta
minutos y te alerta de fugas en tiempo real, cosa que ninguno de los seis
anteriores hace bien.

Después de eso, si quedan recursos, añadir NeMo Guardrails para que el
equipo de producto pueda editar reglas sin pedirte cambios, y meter PyRIT
en el ciclo mensual de red team manual. Pero eso ya no es del lunes que
viene.

Con eso cierro el manual. Si te ha sido útil, dilo, abre un issue en
GitHub si encuentras un error, y si lo vas a usar en tu organización,
considera aportar las correcciones que vayas viendo. Yo seguiré
actualizándolo. Gracias por escuchar.
"""


# =====================================================
# GENERACIÓN
# =====================================================
CAPITULOS = [
    ("00_prologo",                "Prólogo",                      PROLOGO),
    ("01_setup",                  "Cap. 1 - Setup",               CH1),
    ("02_intro_ataque",           "Cap. 2 - Introducción ataque", CH2_INTRO),
    ("03_garak",                  "Cap. 2.1 - Garak",             CH2_GARAK),
    ("04_pyrit",                  "Cap. 2.2 - PyRIT",             CH2_PYRIT),
    ("05_promptfoo",              "Cap. 2.3 - Promptfoo",         CH2_PROMPTFOO),
    ("06_textattack",             "Cap. 2.4 - TextAttack",        CH2_TEXTATTACK),
    ("07_art",                    "Cap. 2.5 - ART",               CH2_ART),
    ("08_harmbench_counterfit",   "Cap. 2.6-2.7",                 CH2_HARMBENCH_COUNTERFIT),
    ("09_llmguard",               "Cap. 3.1 - LLM Guard",         CH3_INTRO_LLMGUARD),
    ("10_nemo_llamaguard",        "Cap. 3.2-3.3",                 CH3_NEMO_LLAMAGUARD),
    ("11_rebuff_vigil_presidio",  "Cap. 3.4-3.7",                 CH3_RESTO),
    ("12_supply_chain",           "Cap. 4 - Supply chain",        CH4),
    ("13_end_to_end",             "Cap. 5 - End to end",          CH5),
    ("14_diez_horas",             "Cap. 6 - Diez horas",          CH6),
]


def main():
    print(f"Generando {len(CAPITULOS)} capítulos de audio en {OUT}\n")
    total_chars = 0
    for slug, title, text in CAPITULOS:
        mp3 = OUT / f"{slug}.mp3"
        chars = len(text)
        total_chars += chars
        mins_est = chars / 1000  # gTTS ~1000 chars/min en español
        print(f"  {slug:30s}  {chars:>5} chars  ~{mins_est:.1f} min")
        tts = gTTS(text=text, lang="es", slow=False)
        tts.save(str(mp3))
    print(f"\nTotal: {total_chars} caracteres  ~{total_chars/1000:.0f} min")

    # Playlist M3U
    playlist = OUT / "00_playlist.m3u"
    with open(playlist, "w") as f:
        f.write("#EXTM3U\n")
        f.write("#PLAYLIST: SecuAI - Manual de Herramientas\n\n")
        for slug, title, _ in CAPITULOS:
            f.write(f"#EXTINF:-1,{title}\n")
            f.write(f"{slug}.mp3\n")
    print(f"\nPlaylist: {playlist}")


if __name__ == "__main__":
    main()
