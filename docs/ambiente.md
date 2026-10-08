# Ejercicio 1: ambiente verificado

Se inició Docker Desktop y se construyeron ambos servicios con Docker Compose.

| Servicio | Comprobación | Resultado |
|---|---|---|
| JupyterLab | GET :8888/api/status | HTTP 200 |
| Metabase | GET :3000/api/health | HTTP 200, status=ok |
| DuckDB en Docker | Lectura directa de Parquet 2026 | 30.040.469 filas |
| Descargador en Docker | 4 pruebas de integridad | Todas pasan |

Versiones instaladas en el contenedor lab:

```text
3.11.14 (main, Feb 24 2026, 19:56:58) [GCC 14.2.0]
DuckDB 1.5.5
Pandas 3.0.6
PyArrow 25.0.1
Matplotlib 3.11.2
Requests 2.34.2
JupyterLab 4.6.4
```

Metabase v0.63.19 y driver DuckDB 1.5.5.0 según los argumentos de construcción.
Java 21 sobre Jammy proporciona glibc para el driver.

Herramientas: JupyterLab para notebooks, DuckDB para SQL analítico, PyArrow para
Parquet, Pandas para resultados pequeños, Matplotlib para gráficos, Requests para
descarga y Git para verificar archivos versionados.

La ejecución principal se hizo en macOS con las mismas versiones directas. El
benchmark registra su entorno propio en benchmarks/environment.json. La lectura
Parquet y las pruebas también se ejecutaron dentro de Docker; Metabase corre en
Docker. Los puertos solo escuchan en 127.0.0.1.

La carpeta está en iCloud Drive. Se marcó Keep Downloaded y se recuperaron copias
locales de código a partir de Git/upstream cuando el sistema las retiró del disco.
El entorno Python auxiliar está en la caché local fuera de iCloud para evitar
bloqueos de sincronización. Los datos originales no se modificaron.

El README contiene comandos de arranque y explica por qué Docker, versiones, SQL,
reglas y hashes permiten reproducir el análisis. ambiente.json conserva la fecha
y respuestas de salud exactas.

La verificación final dentro de Docker también terminó correctamente: 64 hashes,
conservación incremental, 96 mediciones, 10 tarjetas con resultados y notebook
ejecutado. Resultado: verification.json.
