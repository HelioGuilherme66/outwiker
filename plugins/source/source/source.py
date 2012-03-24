#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.pages.wiki.wikipanel import WikiPagePanel
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo

from .sourceconfig import SourceConfig


class PluginSource (Plugin):
    """
    Плагин, добавляющий обработку команды (:source:) в википарсер
    """
    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        # Для работы этого плагина требуется OutWiker 1.6.0.632
        if getCurrentVersion() < Version (1, 6, 0, 632, status=StatusSet.DEV):
            raise BaseException ("OutWiker version requirement: 1.6.0.632")

        Plugin.__init__ (self, application)
        self.__version = u"1.4.0"
        self.SOURCE_TOOL_ID = u"PLUGIN_SOURCE_TOOL_ID"


    @property
    def _isCurrentWikiPage (self):
        return (self._application.selectedPage != None and
                self._application.selectedPage.getTypeString() == u"wiki")


    def initialize(self):
        self.__initlocale()

        self.__correctSysPath()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPreferencesDialogCreate += self.__onPreferencesDialogCreate

        if self._isCurrentWikiPage:
            self.__onPageViewCreate (self._application.selectedPage)


    def __correctSysPath (self):
        cmd_folder = unicode (os.path.dirname(os.path.abspath(__file__)), getOS().filesEncoding )
        syspath = [unicode (item, getOS().filesEncoding) if type (item) != type(u"") else item for item in sys.path]

        if cmd_folder not in syspath:
            sys.path.insert(0, cmd_folder)

    
    def __onWikiParserPrepare (self, parser):
        from .commandsource import CommandSource
        parser.addCommand (CommandSource (parser, self._application.config))


    def __onPreferencesDialogCreate (self, dialog):
        from .preferencepanel import PreferencePanel
        prefPanel = PreferencePanel (dialog.treeBook, self._application.config, _)

        panelName = _(u"Source [Plugin]")
        panelsList = [PreferencePanelInfo (prefPanel, panelName)]
        dialog.appendPreferenceGroup (panelName, panelsList)


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow != None

        if page.getTypeString() != u"wiki":
            return

        pageView = self.__getPageView()

        helpString = _(u"Source Code (:source ...:)")
        pageView.addTool (pageView.commandsMenu, 
                self.SOURCE_TOOL_ID, 
                self.__onInsertCommand, 
                helpString, 
                helpString, 
                None)


    def __getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        pageView = self._application.mainWindow.pagePanel.pageView
        assert type (pageView) == WikiPagePanel

        return pageView


    @property
    def config (self):
        return SourceConfig (self._application.config)


    def __onInsertCommand (self, event):
        config = self.config

        startCommand = u'(:source lang="{language}" tabwidth={tabwidth}:)\n'.format (
                language=config.defaultLanguage.value,
                tabwidth=config.tabWidth.value
                )

        endCommand = u'\n(:sourceend:)'

        pageView = self.__getPageView()
        pageView.codeEditor.turnText (startCommand, endCommand)


    @property
    def name (self):
        return u"Source"


    @property
    def description (self):
        return _(u"""Add command (:source:) in wiki parser. This command highlight your source code.

<B>Usage:</B>:
(:source params... :)
source code
(:sourceend:)

<B>Params:</B>
<I>lang</I> - programming language
<I>tabwidth</I> - tab size

<B>Example:</B>
<PRE>(:source lang="python" tabwidth=4:)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>
""")


    @property
    def version (self):
        return self.__version


    def __initlocale (self):
        domain = u"source"

        langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
        global _

        try:
            _ = self._init_i18n (domain, langdir)
        except BaseException as e:
            print e


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPreferencesDialogCreate -= self.__onPreferencesDialogCreate

        if self._isCurrentWikiPage:
            self.__getPageView().removeTool (self.SOURCE_TOOL_ID)
