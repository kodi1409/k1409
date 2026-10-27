# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
import json
import os
from urllib.parse import parse_qs, urlencode

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

YOUTUBE = 'plugin://plugin.video.youtube/'
LANGUAGES = {'latino': 'Español latino', 'castellano': 'Castellano', 'es': 'Español'}


def youtube_search(query, channel_id=None):
    params = {'q': query}
    if channel_id:
        params['channel_id'] = channel_id
    return YOUTUBE + 'search/?' + urlencode(params)


class Misterio:
    def __init__(self, argv):
        self.base = argv[0]
        self.handle = int(argv[1])
        self.params = parse_qs(argv[2].lstrip('?') if len(argv) > 2 else '')
        self.addon = xbmcaddon.Addon()
        self.path = xbmcvfs.translatePath(self.addon.getAddonInfo('path'))
        self.icon = os.path.join(self.path, 'icon.png')
        self.fanart = os.path.join(self.path, 'fanart.jpg')
        with open(os.path.join(self.path, 'resources', 'catalog.json'), encoding='utf-8') as stream:
            self.catalog = json.load(stream)
        self.channels = {c['key']: c for c in self.catalog['channels']}

    def param(self, name, default=''):
        return self.params.get(name, [default])[0]

    def local_url(self, action, **params):
        return self.base + '?' + urlencode(dict(action=action, **params))

    def add(self, title, url, plot='', folder=True, playable=False, thumb=None):
        item = xbmcgui.ListItem(label=title)
        item.setArt({'icon': thumb or self.icon, 'thumb': thumb or self.icon,
                     'fanart': self.fanart})
        tag = item.getVideoInfoTag()
        tag.setTitle(title)
        tag.setPlot(plot)
        item.setProperty('IsPlayable', 'true' if playable else 'false')
        xbmcplugin.addDirectoryItem(self.handle, url, item, isFolder=folder)

    def channel(self, key):
        c = self.channels[key]
        self.add(c['name'] + ' · ' + LANGUAGES[c['language']],
                 YOUTUBE + 'channel/' + c['id'] + '/', c['description'])

    def video(self, v):
        c = self.channels[v['channel']]
        self.add(v['title'] + ' · ' + LANGUAGES[c['language']],
                 YOUTUBE + 'play/?' + urlencode({'video_id': v['id']}),
                 v['description'], folder=False, playable=True,
                 thumb='https://i.ytimg.com/vi/' + v['id'] + '/hqdefault.jpg')

    def home(self):
        self.add('[COLOR FFBB3344][B]Esta noche no apagues la luz[/B][/COLOR]',
                 self.local_url('featured'), 'Tres puertas de entrada: brujería, radio de terror y horror cósmico. Vídeos seleccionados y canales para seguir explorando.')
        for s in self.catalog['sections']:
            self.add(s['title'], self.local_url('section', id=s['id']), s['description'])
        self.add('Voces de Latinoamérica', self.local_url('channels', language='latino'), 'Canales seleccionados en español latino.')
        self.add('Voces en castellano', self.local_url('channels', language='castellano'), 'Noviembre Nocturno, Terrores Nocturnos e Iker Jiménez.')
        self.add('Todos los canales', self.local_url('channels'), 'Los 24 canales originales y las nuevas incorporaciones.')
        self.add('Buscar en YouTube', self.local_url('search'), 'Escribe un tema. Los resultados los proporciona YouTube.')
        self.add('Ayuda y configuración de YouTube', self.local_url('help'), 'Instalación, reproducción y configuración del addon de YouTube.')

    def directory(self):
        action = self.param('action')
        if not action:
            self.home()
        elif action == 'section':
            section = next((s for s in self.catalog['sections'] if s['id'] == self.param('id')), None)
            if section is None:
                raise ValueError('Sección no encontrada')
            xbmcplugin.setPluginCategory(self.handle, section['title'])
            for v in self.catalog['videos']:
                if section['id'] in v['sections']:
                    self.video(v)
            for key in section['channels']:
                self.channel(key)
            for search in section['searches']:
                c = self.channels[search['channel']]
                self.add('Buscar: ' + search['title'] + ' · ' + c['name'],
                         youtube_search(search['query'], c['id']),
                         'Búsqueda dentro de ' + c['name'] + '. Los resultados y su disponibilidad dependen de YouTube.')
        elif action == 'channels':
            language = self.param('language')
            if language and language not in LANGUAGES:
                raise ValueError('Idioma no válido')
            for c in self.catalog['channels']:
                if not language or c['language'] == language:
                    self.channel(c['key'])
        elif action == 'featured':
            for v in self.catalog['videos']:
                self.video(v)
            for key in ('c17', 'c20', 'noviembre', 'terrores', 'hablemos', 'c21'):
                self.channel(key)
        elif action == 'search':
            query = xbmcgui.Dialog().input('¿Qué misterio quieres encontrar?').strip()
            if query:
                self.add('Buscar: ' + query, youtube_search(query), 'Búsqueda libre en YouTube; puede incluir resultados en otros idiomas.')
        elif action == 'help':
            self.add('Abrir YouTube', YOUTUBE, 'Completa su asistente y prueba un vídeo directamente en YouTube.')
            self.add('Configuración de YouTube', self.local_url('youtube_settings'), 'Abre los ajustes de YouTube.', folder=False)
            self.add('Acerca de Misterio', self.local_url('about'), 'Información del catálogo y ayuda.', folder=False)
        elif action == 'youtube_settings':
            try:
                xbmcaddon.Addon('plugin.video.youtube').openSettings()
            except RuntimeError:
                xbmcgui.Dialog().ok('Misterio', 'Instala y habilita YouTube desde el repositorio de Kodi.')
        elif action == 'about':
            xbmcgui.Dialog().textviewer('Misterio',
                'Misterio 3.0.0\n\n28 canales y 12 secciones de terror y misterio.\n'
                'Ficción, folclore, testimonios e investigaciones se describen en cada sección.\n\n'
                'Los vídeos se reproducen mediante el addon YouTube. Completa su asistente; '
                'si solicita claves API o iniciar sesión, sigue las instrucciones de ese addon. '
                'Si un vídeo falla, pruébalo directamente en YouTube. Puede haber restricciones, '
                'retiradas o problemas de cuota.\n\n'
                'Puedes añadir entradas a Favoritos desde el menú contextual de Kodi.\n'
                'Contacto indicado en la versión original: Telegram @grupomundokodi.\n'
                'Catálogo revisado el 22/10/2026. La reproducción no ha sido certificada en Kodi 22.')
        else:
            raise ValueError('Acción no reconocida')


def run(argv):
    handle = int(argv[1])
    try:
        app = Misterio(argv)
        xbmcplugin.setContent(handle, 'videos')
        xbmcplugin.setPluginCategory(handle, 'Misterio')
        app.directory()
    except Exception as exc:
        xbmc.log('[Misterio] {}: {}'.format(type(exc).__name__, exc), xbmc.LOGERROR)
        xbmcgui.Dialog().ok('Misterio', 'No se pudo abrir esta sección. Consulta el registro de Kodi para más detalles.')
        xbmcplugin.endOfDirectory(handle, succeeded=False)
    else:
        xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)
