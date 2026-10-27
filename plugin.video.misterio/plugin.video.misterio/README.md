# Misterio 3.0.0

Catálogo de terror y misterio para Kodi, con prioridad en Kodi 21 y preparado con la API Python moderna para Kodi 22. La reproducción y los resultados de búsqueda los gestiona `plugin.video.youtube`.

## Instalación

1. Instala o actualiza YouTube desde el repositorio de Kodi (7.4.4 o posterior) y completa su asistente. Si solicita claves API o acceso a la cuenta, sigue sus instrucciones. Comprueba que reproduce un vídeo directamente.
2. En Kodi abre **Add-ons → Instalar desde un archivo ZIP** y selecciona `plugin.video.misterio-3.0.0.zip`. Si Kodi lo pide, habilita la instalación desde orígenes desconocidos.
3. Abre **Add-ons de vídeo → Misterio**. Si tenías la versión 2.0, el identificador es el mismo y se instala como actualización.

## Qué incluye

- 28 canales: se conservan los 24 originales y se incorporan Noviembre Nocturno, Terrores Nocturnos, MIEDOTECA MX y Hablemos de lo que no existe.
- 12 secciones: relatos a oscuras; brujería; expedientes paranormales; casas encantadas; carreteras; nahuales y leyendas; horror cósmico; misterios de Internet; desapariciones; conspiraciones; OVNIS; grabaciones inquietantes.
- Portada con 3 vídeos seleccionados y acceso a canales destacados.
- 26 búsquedas temáticas limitadas a canales concretos, identificadas con «Buscar:»; no son listas fijas de vídeos.
- Accesos a voces de Latinoamérica y castellano. Los canales sin clasificación regional suficiente siguen disponibles en Todos los canales.
- Buscador libre, ayuda y acceso a los ajustes de YouTube. Kodi permite guardar entradas en Favoritos mediante su menú contextual.

El idioma identifica la voz principal del canal, no garantiza el idioma de invitados o de todas sus publicaciones. Las categorías son una selección editorial y pueden contener ficción, folclore o afirmaciones no verificadas. Las descripciones distinguen estos formatos.

## Compatibilidad y límites de la revisión

Se declara `xbmc.python` 3.0.1, la versión presente en Kodi 21.3. Se utilizan `getVideoInfoTag`, `setArt`, `xbmcvfs.translatePath` y rutas públicas del addon YouTube. No se usa `six`, extracción de streams ni una API propia de YouTube.

Se probaron con dobles de la API de Kodi las rutas, idiomas, búsquedas con caracteres especiales, cancelaciones, errores y metadatos de carpetas/vídeos. Esto no sustituye una prueba dentro de Kodi. Kodi 21.3 está instalado en el equipo de desarrollo; no se ejecutó una prueba de reproducción ni de interfaz en él. Kodi 22 tampoco se probó en ejecución.

Las 28 páginas de canales y las 3 de vídeos devolvieron títulos concordantes al revisar las fuentes. Esto confirma su identificación pública, no reproducción en todas las regiones/cuentas. Si una entrada deja de funcionar, abre su canal o prueba el vídeo directamente desde YouTube.

## Mantenimiento

El catálogo se edita en `resources/catalog.json`. Cada canal y vídeo incluye una URL de fuente. Los identificadores estables `UC…` evitan depender del nombre visible del canal. El código de navegación está en `resources/lib/misterio.py`.

En la carpeta superior del proyecto:

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_sources.py
python3 tools/build_zip.py
```

El comprobador de fuentes requiere Internet. El empaquetador solo incluye los archivos necesarios: excluye cachés, archivos `._` de macOS y herramientas de desarrollo.

## Créditos

Addon original: MK. La versión original utilizaba Plugintools de Jesús / pelisalacarta. El respaldo 2.0 conserva su código y avisos. La navegación 3.0 se reescribió con Python 3 y las APIs de Kodi. Se conserva la identidad gráfica original. Código de esta versión: GPL-3.0-or-later; los vídeos y marcas pertenecen a sus respectivos titulares.

## Referencias técnicas

- [API de ListItem de Kodi](https://xbmc.github.io/docs.kodi.tv/master/kodi-dev-kit/group__python__xbmcgui__listitem.html)
- [API de InfoTagVideo de Kodi](https://xbmc.github.io/docs.kodi.tv/master/kodi-dev-kit/group__python___info_tag_video.html)
- [Addon YouTube y versiones](https://github.com/anxdpanic/plugin.video.youtube/releases)
- [Implementación de rutas de YouTube](https://github.com/anxdpanic/plugin.video.youtube/blob/master/resources/lib/youtube_plugin/youtube/provider.py)
