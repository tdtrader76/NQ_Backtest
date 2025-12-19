# Informe Técnico: 

**Resumen Ejecutivo:**
Este informe técnico proporciona un análisis exhaustivo del proceso de ingeniería inversa aplicado a los indicadores de NinjaScript, el lenguaje de programación propietario de la plataforma de trading NinjaTrader. Dada la arquitectura de NinjaScript, basada en C# y el framework .NET de Microsoft, los indicadores compilados se distribuyen como ensamblados .NET (archivos DLL), lo que los hace susceptibles a la decompilación. El objetivo de este documento es detallar las metodologías, herramientas y consideraciones técnicas necesarias para analizar, comprender y recrear la lógica de estos indicadores. Se abordan los fundamentos de la arquitectura de NinjaScript, el uso de herramientas de decompilación como ILSpy, las técnicas de análisis de código, las estrategias para gestionar y eliminar dependencias de librerías externas, y el proceso paso a paso para la reconstrucción del código fuente. Adicionalmente, se incluyen ejemplos prácticos y se discuten las mejores prácticas para asegurar la fidelidad del indicador recreado. Finalmente, el informe concluye con una sección crítica sobre los aspectos legales y éticos que rigen la ingeniería inversa de software en el marco jurídico español, destacando los usos permitidos, como la interoperabilidad, y las actividades que constituyen una infracción de la propiedad intelectual.

## 1. Fundamentos de la Arquitectura de NinjaScript

Para abordar la ingeniería inversa de cualquier software, es imperativo primero comprender su arquitectura subyacente. NinjaScript, el lenguaje utilizado para el desarrollo de estrategias de trading automatizado, indicadores y otros complementos en la plataforma NinjaTrader, está intrínsecamente ligado al ecosistema de Microsoft .NET. Esta base tecnológica define no solo cómo se desarrollan los scripts, sino también cómo se compilan, distribuyen y ejecutan, sentando las bases para las técnicas de decompilación.

NinjaScript es, en esencia, un derivado del lenguaje de programación C#, utilizando específicamente la versión C# 8 y compilando para el framework .NET 4.8. Esta elección arquitectónica por parte de los desarrolladores de NinjaTrader ofrece una ventaja significativa para los programadores familiarizados con el entorno de Microsoft, ya que pueden aplicar sus conocimientos de C# directamente al desarrollo de herramientas de trading. La sintaxis, las estructuras de control y los paradigmas de programación orientada a objetos son los mismos que en C# estándar. Esto significa que los desarrolladores tienen acceso a una vasta gama de funcionalidades proporcionadas por el framework .NET. Por ejemplo, clases fundamentales como `System.Math` están disponibles de forma nativa para realizar cálculos matemáticos complejos, eliminando la necesidad de reinventar funciones básicas y permitiendo a los desarrolladores centrarse en la lógica de trading.

Una de las características más potentes de esta arquitectura es la interoperabilidad con librerías de enlace dinámico (.NET DLLs). Los desarrolladores pueden crear sus propias librerías de funciones en C# o utilizar las de terceros, compilarlas como un archivo DLL y luego referenciarlas desde sus indicadores o estrategias en NinjaScript. Esto fomenta la modularidad y la reutilización de código. Sin embargo, esta capacidad introduce una capa de complejidad cuando se trata de dependencias. Si una librería .NET personalizada depende a su vez de una librería no gestionada (una DLL nativa de C++, por ejemplo), ambas deben ser colocadas en el directorio `bin/custom` de la instalación de NinjaTrader para que la plataforma pueda localizarlas y cargarlas correctamente en tiempo de ejecución.

El ciclo de vida de un indicador o estrategia en NinjaScript culmina en su compilación. El código C# escrito en el editor de NinjaScript se transforma en un ensamblado .NET, que es un archivo DLL. Este proceso no solo optimiza el rendimiento, sino que también sirve como un mecanismo de protección de la propiedad intelectual. Los desarrolladores pueden distribuir sus indicadores en este formato compilado, permitiendo a los usuarios finales utilizarlos en la plataforma sin tener acceso al código fuente original. Es precisamente este archivo DLL el objeto de análisis en un proceso de ingeniería inversa.

El modelo de programación de NinjaScript es predominantemente orientado a eventos. En lugar de un bucle de programa continuo, los scripts reaccionan a eventos específicos que ocurren en la plataforma. El evento más fundamental es `OnBarUpdate()`, que se invoca con cada nueva barra de precios (o cada tick, si está configurado para ello). Es dentro de este método donde reside la mayor parte de la lógica de cálculo de un indicador. Otros eventos cruciales incluyen `OnStateChange()`, que gestiona las diferentes fases del ciclo de vida del script (configuración, carga de datos históricos, transición a tiempo real); `OnMarketData()`, para reaccionar a cambios en el libro de órdenes; y eventos relacionados con la gestión de órdenes y posiciones como `OnOrderUpdate()`, `OnExecutionUpdate()` y `OnPositionUpdate()`. Comprender este modelo es vital para localizar la lógica principal durante el análisis del código decompilado.

## 2. Herramientas de Decompilación para Ensamblados .NET

Dado que los indicadores de NinjaScript se compilan en ensamblados .NET (DLLs), el proceso de ingeniería inversa depende fundamentalmente de herramientas capaces de revertir este proceso de compilación. Estas herramientas, conocidas como decompiladores, analizan el Lenguaje Intermedio de Microsoft (MSIL o IL) contenido en el ensamblado y lo reconstruyen en un lenguaje de alto nivel, como C#. Entre las diversas opciones disponibles, **ILSpy** se destaca como una de las herramientas más potentes, versátiles y ampliamente utilizadas en la comunidad de desarrollo de .NET.

ILSpy es un proyecto de código abierto, distribuido bajo la licencia MIT, lo que garantiza su uso gratuito tanto para fines personales como comerciales. Su función principal es tomar un binario compilado (.dll, .exe, .winmd) y presentar una reconstrucción legible de su código fuente en C#. El proceso interno de ILSpy es sofisticado: primero, analiza el ensamblado para extraer el código IL y los metadatos asociados, que describen las clases, métodos, propiedades y sus relaciones. A continuación, construye un Árbol de Sintaxis Abstracta (AST, por sus siglas en inglés), que es una representación jerárquica de la estructura del código. Finalmente, su motor de decompilación traduce este AST a la sintaxis de C#, aplicando optimizaciones y heurísticas para producir un código lo más parecido posible al original.

La potencia de ILSpy no reside únicamente en su motor de decompilación, sino también en su amplio conjunto de características y su ecosistema de herramientas. Ofrece una funcionalidad de **decompilación de proyecto completo**, que permite no solo ver un archivo de código, sino guardar un ensamblado entero como un proyecto de Visual Studio (`.csproj`), con todas sus clases y recursos organizados. Esto es invaluable para analizar indicadores complejos o librerías con múltiples componentes. Su explorador de ensamblados proporciona una vista detallada de los metadatos, permitiendo navegar por espacios de nombres, tipos, métodos y atributos. La navegación se ve facilitada por hipervínculos que conectan las declaraciones con sus usos, y la capacidad de explorar jerarquías de herencia (clases base y derivadas).

ILSpy está disponible a través de varias interfaces o "frontends" para adaptarse a diferentes flujos de trabajo. La más común es la aplicación de escritorio para Windows (basada en WPF), que ofrece una experiencia visual e interactiva. Para la automatización y la integración en pipelines de CI/CD, existe **ILSpyCmd**, una utilidad de línea de comandos multiplataforma. Con un simple comando como `ilspycmd MiIndicador.dll -p -o C:\CodigoFuente`, se puede automatizar la decompilación de un ensamblado y guardarlo como un proyecto. Además, ILSpy se integra directamente en los entornos de desarrollo más populares. Existen extensiones para Visual Studio (2017-2026) y Visual Studio Code (`ilspy-vscode`), que permiten decompilar ensamblados sobre la marcha, por ejemplo, al navegar al código de una librería de terceros. Para los desarrolladores que deseen incorporar la funcionalidad de decompilación en sus propias aplicaciones, el motor principal está disponible como un paquete NuGet (`ICSharpCode.Decompiler`).

Aunque ILSpy es extremadamente eficaz, es importante reconocer que la decompilación no siempre es perfecta. En algunos casos, especialmente con código ofuscado o construcciones de compilador muy complejas, el código resultante puede contener artefactos o no compilar directamente. En tales situaciones, puede ser útil considerar herramientas alternativas como **JustDecompile** de Telerik o **dotPeek** de JetBrains para obtener una segunda perspectiva, ya que cada decompilador utiliza heurísticas ligeramente diferentes que pueden tener éxito donde otro falla. Sin embargo, para la gran mayoría de los indicadores de NinjaScript, ILSpy proporciona una reconstrucción de alta fidelidad que sirve como una base sólida para el análisis.

## 3. Técnicas de Análisis del Código Decompilado

Una vez que el archivo DLL del indicador de NinjaScript ha sido procesado por un decompilador como ILSpy, el resultado es un cuerpo de código C# que, aunque estructuralmente similar al original, requiere un análisis metódico para ser comprendido en su totalidad. Esta fase es un trabajo de detective digital, donde el objetivo es desentrañar la lógica de negocio, los algoritmos de cálculo y la interacción del indicador con la plataforma NinjaTrader.

El primer paso consiste en cargar el archivo DLL en la interfaz de ILSpy. La herramienta presentará una vista de árbol que desglosa el ensamblado en sus espacios de nombres, clases, métodos y propiedades. La tarea inicial es localizar la clase principal del indicador. Por convención, los indicadores de NinjaScript heredan de la clase base `NinjaTrader.NinjaScript.Indicator`. Navegando por la jerarquía de clases o utilizando la función de búsqueda de ILSpy, se puede identificar rápidamente la clase que implementa la lógica central.

Una vez identificada la clase principal, el foco se desplaza a sus métodos, específicamente a aquellos que responden a los eventos de la plataforma. El método `OnStateChange()` es de suma importancia. Este método se ejecuta en diferentes "estados" del ciclo de vida del indicador. En el estado `State.SetDefaults`, se establecen los valores predeterminados de los parámetros de entrada. En `State.Configure`, se definen los elementos visuales del indicador, como las líneas o "plots", utilizando llamadas al método `AddPlot()`. Analizar esta sección revela cuántas líneas dibuja el indicador, sus colores por defecto y sus nombres. En `State.DataLoaded`, se pueden realizar cálculos iniciales una vez que los datos históricos están disponibles.

El corazón algorítmico de la mayoría de los indicadores reside en el método `OnBarUpdate()`. Este método se ejecuta por cada barra (o tick) de datos que procesa el indicador. Dentro de este método, se encontrarán los cálculos que determinan los valores de las líneas del indicador en cada punto del tiempo. Es crucial prestar atención a cómo se accede a los datos de precios. NinjaTrader proporciona acceso a series de datos como `Close`, `High`, `Low` y `Open` como si fueran arrays. La notación `Close[0]` se refiere al precio de cierre de la barra actual, `Close[1]` al de la barra anterior, y así sucesivamente. El análisis de `OnBarUpdate()` implica rastrear el flujo de datos: desde los parámetros de entrada del usuario y las series de precios, a través de variables intermedias, hasta la asignación final de los valores calculados a las series de los plots. Por ejemplo, una línea de código como `Values[0][0] = miValorCalculado;` asigna el resultado de un cálculo al primer plot (`Values[0]`) en la barra actual (`[0]`).

Los parámetros de entrada del usuario, que aparecen en el cuadro de diálogo de configuración del indicador, se definen en el código como propiedades de la clase adornadas con el atributo `[NinjaScriptProperty]`. Identificar estas propiedades es fundamental para comprender qué aspectos del comportamiento del indicador son configurables. Por ejemplo, una propiedad `Period` de tipo `int` con este atributo corresponderá a la entrada de período de una media móvil.

Durante el análisis, es útil emplear las funciones de navegación de ILSpy. Hacer clic derecho sobre un método, propiedad o variable y seleccionar "Analizar" puede mostrar todos los lugares donde se utiliza, se asigna o se invoca. Esta capacidad es invaluable para seguir la lógica a través de múltiples métodos o clases, especialmente en indicadores más complejos que pueden delegar cálculos a funciones auxiliares. Si el indicador depende de otras librerías DLL personalizadas, ILSpy mostrará las llamadas a esas librerías. Esto indica que el análisis debe extenderse a esas dependencias, repitiendo el proceso de decompilación y análisis para ellas también, con el fin de obtener una imagen completa del funcionamiento.

## 4. Eliminación de Dependencias de DLL Externas

Durante el proceso de ingeniería inversa o simplemente durante el uso y gestión de la plataforma NinjaTrader, puede surgir la necesidad de eliminar dependencias de archivos DLL externos. Estas dependencias pueden ser restos de indicadores de terceros desinstalados, versiones antiguas de una librería, o componentes que causan conflictos o inestabilidad en la plataforma. La eliminación limpia de estas referencias es crucial para mantener un entorno de desarrollo y trading estable, y es un paso preparatorio esencial si el objetivo es recrear un indicador de forma autónoma, sin ataduras a librerías externas.

Existen varios métodos para abordar la eliminación de dependencias, que varían en su enfoque y nivel de intervención, desde utilidades integradas en la plataforma hasta la manipulación manual de archivos de configuración.

El método más directo y a menudo el primero a intentar es la **eliminación manual de archivos**. Los archivos DLL personalizados, tanto los que contienen indicadores como las librerías de las que dependen, se encuentran típicamente en el directorio `[Mis Documentos]\NinjaTrader 8\bin\Custom\`. Navegando a esta carpeta, es posible identificar y eliminar directamente los archivos `.dll` no deseados. Por ejemplo, si se ha actualizado un indicador y coexisten `IndicadorV1.dll` e `IndicadorV2.dll`, eliminar la versión antigua puede resolver conflictos de carga. Este método es efectivo para dependencias que no están profundamente integradas en la configuración de la plataforma.

Para un enfoque más controlado y seguro dentro de la propia plataforma (específicamente en NinjaTrader 8), se puede utilizar el **editor de referencias de NinjaScript**. Este método es ideal para desvincular un indicador o estrategia de una librería sin necesidad de eliminar el archivo DLL de la librería del sistema. El proceso implica abrir cualquier script (indicador o estrategia) en el Editor de NinjaScript. Una vez en el editor, se hace clic derecho en la ventana de código y se selecciona la opción "Referencias". Esto abrirá un cuadro de diálogo que lista todos los ensamblados referenciados por los scripts de NinjaScript. En esta lista, se puede localizar la DLL no deseada, seleccionarla y hacer clic en el botón para eliminar la referencia. Tras eliminarla, es importante compilar cualquier script (incluso el que se usó para abrir el editor) para que NinjaTrader procese el cambio. Después de una compilación exitosa, un reinicio de la plataforma NinjaTrader asegurará que la referencia se elimine por completo de la memoria y la configuración de tiempo de ejecución.

En casos más persistentes, donde las referencias parecen estar "atascadas" en la configuración de la plataforma, puede ser necesario un método más avanzado: la **edición del archivo `Config.xml`**. Este archivo, ubicado en el directorio `[Mis Documentos]\NinjaTrader 8\`, contiene la configuración central de la plataforma. Antes de realizar cualquier cambio, es absolutamente crucial crear una copia de seguridad de este archivo. Una vez respaldado, se puede abrir `Config.xml` con un editor de texto y buscar la sección `<References>`. Dentro de esta sección, cada ensamblado referenciado tendrá una entrada de línea, por ejemplo, `<Reference>C:\Users\...\NinjaTrader 8\bin\Custom\MiLibreria.dll</Reference>`. Se puede eliminar cuidadosamente la línea correspondiente a la DLL que se desea desvincular. Tras guardar el archivo y reiniciar NinjaTrader, la plataforma ya no intentará cargar esa dependencia.

Como último recurso, para problemas de dependencias profundamente arraigados o corrupción de la configuración, la **reinstalación limpia** de NinjaTrader es una opción viable. Este proceso drástico implica primero hacer una copia de seguridad de todos los datos de usuario importantes (workspaces, plantillas, scripts personalizados). Luego, se renombra la carpeta `[Mis Documentos]\NinjaTrader 8` (por ejemplo, a `NT8.bak`). Finalmente, se desinstala y se vuelve a instalar la plataforma NinjaTrader. Esto crea una configuración completamente nueva y libre de cualquier referencia o archivo conflictivo. Posteriormente, los datos de usuario respaldados pueden ser restaurados selectivamente en la nueva instalación.

## 5. Proceso de Recreación del Indicador

La recreación de un indicador de NinjaScript a partir de su código decompilado es la culminación del proceso de ingeniería inversa. Es una tarea que combina el análisis técnico con la programación práctica, con el objetivo de producir un nuevo archivo de código fuente (`.cs`) que, una vez compilado, se comporte de manera idéntica al indicador original. Este proceso requiere atención al detalle y un enfoque sistemático.

**Paso 1: Decompilación y Extracción del Código**
El primer paso es utilizar una herramienta como ILSpy para decompilar el archivo DLL del indicador objetivo. Una vez cargado el ensamblado, se navega hasta la clase principal del indicador. ILSpy ofrece la opción de guardar la clase decompilada como un archivo `.cs` individual o, de manera más robusta, guardar el ensamblado completo como un proyecto de Visual Studio (`.csproj`). Esta última opción es preferible para indicadores complejos, ya que preserva la estructura de archivos y recursos, facilitando el análisis.

**Paso 2: Creación del Nuevo Archivo de Indicador**
Dentro de la plataforma NinjaTrader, se debe utilizar el Asistente de NinjaScript para crear un nuevo indicador en blanco. Esto se hace desde el Centro de Control de NinjaTrader, a través del menú `Nuevo > Indicador NinjaScript`. Este asistente genera una plantilla de código con la estructura básica correcta, incluyendo el espacio de nombres (`namespace`), la declaración de la clase que hereda de `Indicator`, y los métodos de eventos fundamentales como `OnStateChange()` y `OnBarUpdate()`.

**Paso 3: Portabilidad de Propiedades y Configuración**
Con el código decompilado abierto en un editor de texto y la nueva plantilla de indicador en el Editor de NinjaScript, comienza el proceso de transferencia. Primero, se copian las declaraciones de propiedades de la clase. Esto incluye los parámetros de entrada del usuario (aquellos marcados con `[NinjaScriptProperty]`), las series de datos para los plots (declaradas como `Series<double>`) y cualquier otra variable de nivel de clase. A continuación, se transfiere el contenido del método `OnStateChange()` del código decompilado al nuevo archivo. Se debe prestar especial atención a la sección `State.Configure`, donde se realizan las llamadas a `AddPlot()`. Es crucial que estas llamadas se repliquen exactamente, incluyendo el color, el nombre y el tipo de gráfico del plot, para asegurar la correspondencia visual.

**Paso 4: Implementación de la Lógica de Cálculo**
Este es el paso más crítico. La lógica contenida en el método `OnBarUpdate()` del código decompilado debe ser cuidadosamente copiada y pegada en el método `OnBarUpdate()` del nuevo script. Durante este proceso, es posible que sea necesario realizar ajustes menores. El código decompilado a veces puede contener sintaxis o construcciones que, aunque válidas, no son idiomáticas o pueden ser simplificadas. El objetivo es transferir el algoritmo de cálculo de manera intacta. Si el indicador original utilizaba funciones auxiliares (métodos privados dentro de la misma clase), estas también deben ser copiadas al nuevo archivo.

**Paso 5: Resolución de Dependencias y Lógica Externa**
Si el análisis inicial reveló que el indicador original dependía de funciones de otra DLL personalizada, se enfrenta una decisión. Una opción es recrear también la funcionalidad de esa DLL externa, ya sea decompilándola y extrayendo las funciones necesarias para integrarlas directamente en el nuevo script (convirtiéndolo en autónomo), o recreando la DLL como un proyecto separado y manteniendo la referencia. Si la dependencia es de una librería estándar de .NET o de la propia API de NinjaTrader, generalmente no se requiere ninguna acción, ya que estas estarán disponibles automáticamente.

**Paso 6: Compilación, Depuración y Verificación**
Una vez que todo el código ha sido transferido, se utiliza la función de compilación del Editor de NinjaScript (tecla F5). Es muy probable que la primera compilación falle debido a pequeños errores de sintaxis, referencias faltantes o discrepancias. El panel de errores del editor proporcionará pistas para corregir estos problemas. Una herramienta de depuración invaluable en esta fase es el método `Print()`. Insertando llamadas como `Print("Valor en la barra " + CurrentBar + ": " + miVariable);` en puntos clave del código, se pueden imprimir los valores de las variables en la ventana de Salida de NinjaScript. Esto permite comparar, barra por barra, los resultados de los cálculos del indicador recreado con los del original.

El paso final es la verificación visual. Se aplica tanto el indicador original (el del DLL) como el nuevo indicador recreado a la misma ventana de gráfico, con exactamente los mismos parámetros de entrada. Si la recreación ha sido exitosa, las líneas de ambos indicadores deberían superponerse perfectamente, sin ninguna desviación visible. Esta confirmación visual es la prueba definitiva de que la ingeniería inversa ha sido completada con éxito.

## 6. Ejemplos de Código y Casos Prácticos

Para ilustrar de manera concreta los conceptos descritos, esta sección presenta casos prácticos hipotéticos que simulan el proceso de ingeniería inversa sobre diferentes tipos de indicadores de NinjaScript.

**Caso Práctico 1: Indicador Simple - Media Móvil Ponderada**

Supongamos que tenemos un archivo `WeightedMA.dll` que contiene un indicador de media móvil ponderada. Tras decompilarlo con ILSpy, obtenemos un código similar a este:

*Código Decompilado Hipotético:*
```csharp
// ... (declaraciones de namespace y clase)
public class WeightedMA : Indicator
{
    private int period = 14;

    protected override void OnStateChange()
    {
        if (State == State.SetDefaults)
        {
            Description = "Media Móvil Ponderada";
            Name = "WeightedMA";
            IsOverlay = true;
            period = 14;
            AddPlot(Brushes.Goldenrod, "WMA");
        }
    }

    protected override void OnBarUpdate()
    {
        if (CurrentBar < period) return;

        double num = 0.0;
        double den = 0.0;
        for (int i = 0; i < period; i++)
        {
            num += Close[i] * (period - i);
            den += (period - i);
        }
        Values[0][0] = num / den;
    }

    [NinjaScriptProperty]
    [Range(1, int.MaxValue)]
    public int Period
    {
        get { return period; }
        set { period = Math.Max(1, value); }
    }
}
```

**Proceso de Recreación:**
1.  Se crea un nuevo indicador en NinjaTrader.
2.  Se copia la propiedad `Period` con sus atributos `[NinjaScriptProperty]` y `[Range]`.
3.  Se copia el contenido de `OnStateChange()`, asegurando que la llamada a `AddPlot()` sea idéntica.
4.  Se copia la lógica de `OnBarUpdate()`. El bucle `for` y el cálculo `num / den` son el corazón del algoritmo.
5.  Se compila y se verifica. El nuevo indicador debe trazar una línea idéntica a la del `WeightedMA.dll` original.

**Caso Práctico 2: Indicador con Dependencia Externa**

Imaginemos un indicador `VolatilityIndicator.dll` que utiliza una función de una librería matemática personalizada llamada `CustomMath.dll`.

*Código Decompilado Hipotético de `VolatilityIndicator.dll`:*
```csharp
// ...
using CustomMathLibrary; // Referencia a la DLL externa

public class VolatilityIndicator : Indicator
{
    // ... (propiedades y OnStateChange)

    protected override void OnBarUpdate()
    {
        // ...
        double[] priceSeries = new double[20];
        for(int i = 0; i < 20; i++) { priceSeries[i] = Close[i]; }
        
        // Llamada a la función en la DLL externa
        double volatility = AdvancedStats.CalculateStdDev(priceSeries); 
        
        Values[0][0] = volatility;
    }
}
```
En este escenario, el análisis revela una dependencia de `CustomMathLibrary`. Tenemos dos caminos para la recreación:

*   **Camino A: Integrar la Dependencia (Crear un script autónomo):**
    1.  Decompilar `CustomMath.dll` con ILSpy.
    2.  Localizar la clase `AdvancedStats` y el método `CalculateStdDev`.
    3.  Copiar el código fuente de `CalculateStdDev` (y cualquier otra función de la que dependa) y pegarlo como un método privado o una clase estática dentro del nuevo archivo de `VolatilityIndicator.cs`.
    4.  El indicador recreado ahora contiene toda la lógica necesaria y ya no requiere el archivo `CustomMath.dll` para funcionar.

*   **Camino B: Mantener la Dependencia:**
    1.  Asegurarse de que el archivo `CustomMath.dll` esté presente en la carpeta `NinjaTrader 8\bin\Custom\`.
    2.  Al crear el nuevo indicador, hacer clic derecho en el editor, ir a "Referencias" y añadir una referencia explícita a `CustomMath.dll`.
    3.  El código recreado seguirá conteniendo la línea `using CustomMathLibrary;` y la llamada a `AdvancedStats.CalculateStdDev()`.
    4.  Este enfoque es más simple si no se desea modificar la lógica de la librería, pero el indicador resultante no será autónomo.

**Caso Práctico 3: Recreación de Lógica de Estrategia Simple**

La ingeniería inversa también se puede aplicar a estrategias. Supongamos que una estrategia simple en `SimpleStrategy.dll` genera el siguiente código decompilado:

*Código Decompilado Hipotético de `SimpleStrategy.dll`:*
```csharp
public class SimpleStrategy : Strategy
{
    protected override void OnBarUpdate()
    {
        if (CurrentBar < 1) return;

        if (Close[0] > Open[0])
        {
            EnterLong();
        }
        else if (Close[0] < Open[0])
        {
            EnterShort();
        }
    }

    protected override void OnStateChange()
    {
        if (State == State.Configure)
        {
            SetStopLoss(CalculationMode.Percent, 0.5);
            SetProfitTarget(CalculationMode.Percent, 1.0);
        }
    }
}
```
**Proceso de Recreación:**
1.  Se crea una nueva estrategia en NinjaTrader.
2.  Se copia la lógica de `OnBarUpdate()`: la condición `if (Close[0] > Open[0])` para entrar en largo y la condición para entrar en corto.
3.  Se copia la configuración de `OnStateChange()`, que en este caso establece un stop loss del 0.5% y un take profit del 1.0% usando `SetStopLoss()` y `SetProfitTarget()`.
4.  Tras compilar, la nueva estrategia ejecutará las mismas entradas y aplicará la misma gestión de riesgo que la original. Este ejemplo, extraído de la documentación de NinjaScript, muestra cómo las reglas de trading fundamentales son fácilmente identificables en el código.

## 7. Mejores Prácticas en la Ingeniería Inversa de NinjaScript

Abordar la ingeniería inversa de indicadores de NinjaScript de manera efectiva y eficiente no solo depende del conocimiento de las herramientas, sino también de la adopción de un conjunto de mejores prácticas. Estas prácticas aseguran un proceso estructurado, minimizan errores y garantizan que el producto final sea una réplica fiel del original.

**Adoptar un Enfoque Sistemático y Documentado:** El proceso no debe ser caótico. Se debe seguir una secuencia lógica: decompilación, análisis, documentación, recreación y verificación. Antes de escribir una sola línea de código nuevo, es fundamental dedicar tiempo a analizar a fondo el código decompilado. Durante esta fase de análisis, es altamente recomendable documentar los hallazgos. Esto puede ser tan simple como añadir comentarios en el propio código decompilado o mantener un documento separado que describa el propósito de las variables clave, el flujo del algoritmo en `OnBarUpdate()`, la función de los parámetros de entrada y la configuración de los plots. Esta documentación se convertirá en el plano para la fase de recreación.

**Utilizar Control de Versiones:** Desde el momento en que se crea el nuevo archivo de indicador, este debe ser gestionado bajo un sistema de control de versiones como Git. Esto proporciona beneficios inmensos. Permite guardar "instantáneas" del código en diferentes etapas del desarrollo. Si una modificación introduce un error o una desviación en el cálculo, es fácil revertir a una versión anterior que funcionaba correctamente. El control de versiones también facilita la experimentación, ya que se pueden crear ramas para probar diferentes enfoques de recreación sin afectar la línea principal de desarrollo.

**Recreación Incremental y Pruebas Continuas:** En lugar de intentar copiar y pegar todo el código decompilado de una sola vez, es mucho más efectivo un enfoque incremental. Se puede comenzar por recrear la estructura básica: los parámetros de entrada y la configuración de los plots en `OnStateChange()`. Compilar y verificar que el indicador se carga en el gráfico con los parámetros y plots correctos. A continuación, añadir una pequeña parte de la lógica de cálculo de `OnBarUpdate()`, compilar y verificar los resultados (usando el método `Print()` o la inspección visual). Continuar añadiendo complejidad gradualmente, probando en cada paso, permite aislar los errores de manera mucho más sencilla. Si un error aparece, se sabe que fue introducido en el último fragmento de código añadido.

**Verificación Exhaustiva y Rigurosa:** La verificación final no debe limitarse a una simple superposición visual en un único gráfico. El indicador recreado debe ser probado rigurosamente en una variedad de condiciones para asegurar su robustez y fidelidad. Esto incluye aplicar ambos indicadores (el original y el recreado) en diferentes instrumentos (acciones, futuros, forex), diferentes marcos de tiempo (minutos, diario, semanal) y con diferentes conjuntos de parámetros de entrada. El objetivo es confirmar que se comportan de manera idéntica en todos los escenarios posibles. Cualquier discrepancia, por mínima que sea, indica un error en la recreación que debe ser investigado y corregido.

**Respeto por la Propiedad Intelectual:** Esta es la práctica más importante desde una perspectiva ética y legal. El conocimiento y las técnicas de ingeniería inversa deben ser utilizados de manera responsable. El objetivo principal debería ser el aprendizaje, la interoperabilidad (hacer que un indicador funcione con una estrategia personalizada) o la recuperación de código propio perdido. Recrear un indicador comercial para uso personal es una zona legalmente gris, pero distribuirlo o venderlo como propio es una clara infracción de los derechos de autor. Siempre se debe actuar con la conciencia de que detrás del indicador original hay un desarrollador cuyo trabajo y propiedad intelectual merecen respeto.


# References
1. [NinjaTrader Algo Trading: A Complete Guide - QuantVPS](https://www.quantvps.com/blog/ninjatrader-algo-trading)
2. [.NET DLL depends on a regular DLL - NinjaTrader Support Forum](https://forum.ninjatrader.com/forum/ninjatrader-8/platform-technical-support-aa/1211085-net-dll-depends-on-a-regular-dll)
3. [Basic Syntax - NinjaTrader 8 Help Guide](https://ninjatrader.com/support/helpguides/nt8/basic_syntax.htm)
4. [GitHub - watthem/ninjascript: A collection of my ninjascript indicators and strategies for ninjatrader 8](https://github.com/watthem/ninjascript)
5. [A Simple Guide To Use NinjaScript - Ninza](https://ninza.co/blog/a-simple-guide-to-use-ninjascript)
6. [icsharpcode/ILSpy - GitHub](https://github.com/icsharpcode/ILSpy)
7. [Is there a way to do automated decompilation with ILSpy? - Stack Overflow](https://stackoverflow.com/questions/60856709/is-there-a-way-to-do-automated-decompilation-with-ilspy)
8. [Help decompiling DLL through ILSpy - Reddit](https://www.reddit.com/r/csharp/comments/ymbpjf/help_decompiling_dll_through_ilspy/)
9. [ILSpy .NET Decompiler](https://ilspy.org/)
10. [How to decompile (read source code) of .NET Framework assemblies using ILSpy - Our Code World](https://ourcodeworld.com/articles/read/456/how-to-decompile-read-source-code-of-net-framework-assemblies-using-ilspy)
11. [How to manually clean out vendor's bootstrapping DLL addon's - NinjaTrader Support Forum](https://forum.ninjatrader.com/forum/ninjatrader-8/platform-technical-support-aa/1067681-how-to-manually-clean-out-vendor-s-bootstrapping-dll-addon-s)
12. [NT8 Manually Uninstall Package - NinjaTrader Support Forum](https://forum.ninjatrader.com/forum/ninjatrader-8/indicator-development/109790-nt8-manually-uninstall-package)
13. [Removing old custom dll files - NinjaTrader Support Forum](https://forum.ninjatrader.com/forum/ninjatrader-7/platform-technical-support/27230-removing-old-custom-dll-files)
14. [How to delete dll strategy file - NinjaTrader Support Forum](https://forum.ninjatrader.com/forum/ninjatrader-7/platform-technical-support/45441-how-to-delete-dll-strategy-file#post458271)
15. [Programación en NinjaScript (II) - EventosTrading](https://www.eventostrading.com/index.php/2024/10/09/programacion-en-ninjascript-ii/)
16. [Trabajar con indicadores - NinjaTrader 8 Help Guide](https://ninjatrader.com/es/support/helpGuides/nt8/working_with_indicators.htm)
17. [Challenge: NinjaScript (C#) interface with a C++ DLL - Stack Overflow](https://stackoverflow.com/questions/30958449/challenge-ninjascript-c-sharp-interface-with-a-c-dll)
18. [La ingeniería inversa, ¿es legal en España? - Abanlex](https://abanlex.com/2013/12/09/la-ingenieria-inversa-es-legal-en-espana/)
19. [Medidas de seguridad, ingeniería inversa y privacidad - El Derecho](https://elderecho.com/medidas-de-seguridad-ingenieria-inversa-y-privacidad)
20. [Ingeniería Inversa - Jeffry Chaves](https://jeffrychaves.com/diccionario/ingenieria-inversa/)
22. [Reverse engineering - what is it and is it legal? - TME](https://www.tme.com/us/en-us/news/library-articles/page/56932/reverse-engineering-what-is-it-and-is-it-legal/)