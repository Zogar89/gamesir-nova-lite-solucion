# GameSir Nova Lite: recuperar el cambio de modo

Guía en español para el **GameSir Nova Lite / T4n Lite original**, con capturas, instrucciones y archivos del receptor. Fuente estática en `dist/`, sin dependencias de ejecución.

La solución final del caso fue **mando 7000 + dongle V16**. Como alternativa funcionó **mando 4200 + dongle de fábrica**, cuya versión exacta no se identificó. Las combinaciones cruzadas fallaron. Incluye el cambio de modo con View (ventanitas) + Menu (tres rayitas), la ventana de 10 segundos para iniciar la escritura y la experiencia de actualización en Windows 10 como administrador.

## Sitio y descargas

- [Guía en GitHub Pages](https://zogar89.github.io/gamesir-nova-lite-solucion/)
- [Kit del dongle V16](dist/downloads/GameSir_Nova_Lite_SOLO_DONGLE_V16.zip)
- [Solo firmware del dongle](dist/downloads/T4N_dog_V16_update.ufw)
- [Instrucciones en español](dist/downloads/LEEME.txt)
- [Hashes de los archivos](dist/downloads/SHA256SUMS.txt)
- [Tamaño y SHA-256 del ZIP](dist/downloads/kit-manifest.json)

**No incluye firmware del mando. No usar GameSir Connect con este dongle:** GameSir advierte que puede inutilizarlo. No usar estos archivos con Nova 2 Lite, Nova Lite 2 ni otros modelos.

## Vista previa

```powershell
python -m http.server 8787 --bind 127.0.0.1 --directory dist
```

## Descarga archivada

`build_downloads.py <carpeta-con-binarios-originales>` valida los hashes conocidos y genera un ZIP que contiene exclusivamente herramienta, DLL y firmware del dongle, además del LEEME, la guía visual y sus hashes. Nunca se ejecuta el actualizador para construir o validar el sitio.

El ZIP, el .ufw, el LEEME y los hashes tienen enlaces directos y se descargan sin JavaScript. El programa permanece en chino; su tutorial en inglés es del paquete V15 y se presenta expresamente como referencia de botones.

## Verificación y publicación

`python validate.py` comprueba los enlaces locales, el contenido del ZIP y sus hashes sin ejecutar el programa de actualización. El workflow `.github/workflows/pages.yml` repite esa verificación y publica `dist/` en GitHub Pages al actualizar `main`.

## Fuentes

- https://doc.xiaoji.com/zh/t4nlite/detail/1192.html
- https://gamesir.com/pages/faq-questions-about-nova-lite
- https://gamesir.com/support/manuals/gamesir-nova-lite
- https://gamesir.com/pages/gamesir-connect-software

Los binarios y capturas de GameSir pertenecen a sus titulares. La fuente Manrope se distribuye bajo SIL Open Font License, incluida junto al archivo. No se incluyen credenciales, datos del chat ni firmware del mando.

Las observaciones de funcionamiento corresponden al caso documentado; no cubren todas las combinaciones posibles de firmware ni demuestran una incompatibilidad general con Windows 11.

[Otra guía: AMD LoadLibrary error 87](https://github.com/Zogar89/amd-loadlibrary-error-87-fix)
