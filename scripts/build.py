############################
# @author EliasDH Team     #
# @see https://eliasdh.com #
# @since 12/11/2026        #
############################
"""Generates the EliasDH Dark/Light colour themes from the EliasDH design tokens and packs a .vsix into Release/.

Usage: python scripts/build.py   (bump "version" in package.json first)
"""
import json, os, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "package.json"), encoding="utf-8") as f:
    pkg = json.load(f)
VERSION = pkg["version"]

# EliasDH design tokens (shared by eliasdh.com, app.eliasdh.com and DHMail),
# plus syntax colours derived from the chart palette.
P = {
    "dark": dict(
        text="#edeff2", bg="#060709", surface="#0d1016", surface2="#141924", primary="#0f54ae",
        secondary="#818a92", accent="#3d587b", success="#199e70", danger="#f87171", warn="#fcd34d",
        ink="#86b6ff", focus="#3987e5", line="#80808038", lineSoft="#80808021", hover="#8080801f",
        tint="#0f54ae38", sel="#0f54ae66", selHi="#0f54ae40", shadow="#0000008c",
        frame="#0d1016", status="#0f54ae", statusFg="#ffffff", statusHover="#ffffff26",
        lineHl="#0d1016", panel="#0d1016", input="#0d1016",
        # syntax
        comment="#6b747d", keyword="#86b6ff", func="#5aa0f2", string="#3fbf8f", number="#e0a32e",
        type="#e87ba4", attr="#f08a5d", prop="#a9bdd8", param="#c9d1db", punct="#818a92",
        ansi=dict(black="#141924", red="#f87171", green="#3fbf8f", yellow="#fcd34d", blue="#3987e5",
                  magenta="#e87ba4", cyan="#4fc3d9", white="#edeff2", bblack="#818a92", bred="#fca5a5",
                  bgreen="#6ee7b7", byellow="#fde68a", bblue="#86b6ff", bmagenta="#f5a8c5",
                  bcyan="#8be0ee", bwhite="#ffffff"),
    ),
    "light": dict(
        # blue-tinted surfaces so the light variant carries the EliasDH blue instead of plain white
        text="#1b2535", bg="#eef3fb", surface="#e1eaf7", surface2="#d3e0f3", primary="#4f94f0",
        secondary="#5d6b80", accent="#829ec2", success="#1baf7a", danger="#e74c3c", warn="#92400e",
        ink="#2f6fc4", focus="#4f94f0", line="#4f94f055", lineSoft="#4f94f038", hover="#4f94f024",
        tint="#4f94f038", sel="#4f94f055", selHi="#4f94f033", shadow="#1f3b6626",
        frame="#cfdef4", status="#4f94f0", statusFg="#ffffff", statusHover="#ffffff26",
        lineHl="#e0eaf8", panel="#e1eaf7", input="#f7faff",
        comment="#6f7d92", keyword="#2a64b8", func="#1d6ccc", string="#12855c", number="#a86500",
        type="#c4457a", attr="#c8501f", prop="#3d587b", param="#4a5a70", punct="#5d6b80",
        ansi=dict(black="#1b2535", red="#d64545", green="#12855c", yellow="#a86500", blue="#2a78d6",
                  magenta="#c4457a", cyan="#0f7f9a", white="#5d6b80", bblack="#7a879a", bred="#e74c3c",
                  bgreen="#1baf7a", byellow="#c98500", bblue="#4f94f0", bmagenta="#e05a91",
                  bcyan="#1aa3c4", bwhite="#3a4a60"),
    ),
}


def colors(c, dark):
    a = c["ansi"]
    on_primary = "#ffffff"
    pc = c["ink"]  # primary colour as readable text
    return {
        # base
        "foreground": c["text"], "descriptionForeground": c["secondary"], "disabledForeground": c["secondary"] + "99",
        "errorForeground": c["danger"], "focusBorder": c["focus"], "contrastBorder": "#00000000",
        "selection.background": c["sel"], "icon.foreground": c["secondary"], "widget.shadow": c["shadow"],
        "widget.border": c["line"], "sash.hoverBorder": c["primary"], "textLink.foreground": c["ink"],
        "textLink.activeForeground": c["focus"], "textPreformat.foreground": c["ink"],
        "textBlockQuote.background": c["surface2"], "textBlockQuote.border": c["primary"],
        "textCodeBlock.background": c["surface2"], "textSeparator.foreground": c["line"],
        "toolbar.hoverBackground": c["hover"], "toolbar.activeBackground": c["hover"],
        "progressBar.background": c["primary"] if not dark else c["focus"],
        # buttons / inputs
        "button.background": c["primary"], "button.foreground": on_primary,
        "button.hoverBackground": c["focus"] if dark else "#3d84e4", "button.border": "#00000000",
        "button.secondaryBackground": c["surface2"], "button.secondaryForeground": c["text"],
        "button.secondaryHoverBackground": c["hover"], "button.separator": "#ffffff40",
        "checkbox.background": c["bg"] if dark else c["bg"], "checkbox.border": c["line"],
        "checkbox.foreground": c["text"], "checkbox.selectBackground": c["primary"],
        "input.background": c["input"], "input.border": c["line"],
        "input.foreground": c["text"], "input.placeholderForeground": c["secondary"],
        "inputOption.activeBackground": c["tint"], "inputOption.activeBorder": c["primary"],
        "inputOption.activeForeground": c["ink"], "inputOption.hoverBackground": c["hover"],
        "inputValidation.errorBackground": c["surface"], "inputValidation.errorBorder": c["danger"],
        "inputValidation.warningBackground": c["surface"], "inputValidation.warningBorder": c["number"],
        "inputValidation.infoBackground": c["surface"], "inputValidation.infoBorder": c["focus"],
        "dropdown.background": c["input"], "dropdown.border": c["line"],
        "dropdown.foreground": c["text"], "dropdown.listBackground": c["bg"],
        "badge.background": c["primary"], "badge.foreground": on_primary,
        "activityBarBadge.background": c["primary"], "activityBarBadge.foreground": on_primary,
        "scrollbar.shadow": "#00000000", "scrollbarSlider.background": c["primary"] + "38",
        "scrollbarSlider.hoverBackground": c["primary"] + "66", "scrollbarSlider.activeBackground": c["primary"] + "99",
        # lists
        "list.activeSelectionBackground": c["tint"], "list.activeSelectionForeground": c["ink"],
        "list.activeSelectionIconForeground": c["ink"], "list.inactiveSelectionBackground": c["hover"],
        "list.inactiveSelectionForeground": c["text"], "list.hoverBackground": c["hover"],
        "list.hoverForeground": c["text"], "list.focusBackground": c["tint"], "list.focusForeground": c["text"],
        "list.focusOutline": c["focus"] + "80", "list.inactiveFocusOutline": "#00000000",
        "list.highlightForeground": c["ink"], "list.focusHighlightForeground": c["ink"],
        "list.errorForeground": c["danger"], "list.warningForeground": c["number"],
        "list.dropBackground": c["tint"], "listFilterWidget.background": c["surface2"],
        "listFilterWidget.outline": c["primary"], "listFilterWidget.noMatchesOutline": c["danger"],
        "tree.indentGuidesStroke": c["line"], "tree.inactiveIndentGuidesStroke": c["lineSoft"],
        # activity bar / side bar
        "activityBar.background": c["frame"], "activityBar.foreground": pc,
        "activityBar.inactiveForeground": c["secondary"], "activityBar.border": c["lineSoft"],
        "activityBar.activeBorder": c["primary"] if not dark else c["focus"],
        "activityBar.activeBackground": c["tint"], "activityBar.activeFocusBorder": c["focus"],
        "activityBarTop.foreground": pc, "activityBarTop.inactiveForeground": c["secondary"],
        "activityBarTop.activeBorder": c["primary"] if not dark else c["focus"], "activityBarTop.activeBackground": c["tint"],
        "sideBar.background": c["surface"], "sideBar.foreground": c["text"], "sideBar.border": c["lineSoft"],
        "sideBarTitle.foreground": pc, "sideBarSectionHeader.background": c["surface"],
        "sideBarSectionHeader.foreground": pc, "sideBarSectionHeader.border": c["lineSoft"],
        "sideBar.dropBackground": c["tint"],
        # title / menu / command center
        "titleBar.activeBackground": c["primary"], "titleBar.activeForeground": on_primary,
        "titleBar.inactiveBackground": c["primary"] + "d9", "titleBar.inactiveForeground": "#ffffffb3",
        "titleBar.border": c["primary"], "menubar.selectionBackground": "#ffffff26",
        "menubar.selectionForeground": on_primary, "window.activeBorder": c["primary"], "window.inactiveBorder": c["line"], "menu.background": c["bg"], "menu.foreground": c["text"],
        "menu.selectionBackground": c["tint"], "menu.selectionForeground": c["ink"],
        "menu.separatorBackground": c["lineSoft"], "menu.border": c["line"],
        "commandCenter.background": "#ffffff1f", "commandCenter.foreground": on_primary,
        "commandCenter.border": "#ffffff40", "commandCenter.activeBackground": "#ffffff33", "commandCenter.activeForeground": on_primary, "commandCenter.activeBorder": "#ffffff66",
        "commandCenter.inactiveForeground": "#ffffffb3", "commandCenter.inactiveBorder": "#ffffff26",
        # quick input / widgets
        "quickInput.background": c["bg"], "quickInput.foreground": c["text"],
        "quickInputTitle.background": c["surface"], "quickInputList.focusBackground": c["tint"],
        "quickInputList.focusForeground": c["ink"], "quickInputList.focusIconForeground": c["ink"],
        "pickerGroup.foreground": c["primary"] if not dark else c["focus"], "pickerGroup.border": c["lineSoft"],
        "keybindingLabel.background": c["surface2"], "keybindingLabel.foreground": c["text"],
        "keybindingLabel.border": c["line"], "keybindingLabel.bottomBorder": c["line"],
        "editorWidget.background": c["surface"], "editorWidget.foreground": c["text"],
        "editorWidget.border": c["line"], "editorWidget.resizeBorder": c["primary"],
        "editorSuggestWidget.background": c["surface"], "editorSuggestWidget.border": c["line"],
        "editorSuggestWidget.foreground": c["text"], "editorSuggestWidget.highlightForeground": c["ink"],
        "editorSuggestWidget.focusHighlightForeground": c["ink"],
        "editorSuggestWidget.selectedBackground": c["tint"], "editorSuggestWidget.selectedForeground": c["text"],
        "editorHoverWidget.background": c["surface"], "editorHoverWidget.border": c["line"],
        "editorHoverWidget.foreground": c["text"], "editorHoverWidget.statusBarBackground": c["surface2"],
        "notifications.background": c["surface"], "notifications.foreground": c["text"],
        "notifications.border": c["lineSoft"], "notificationCenterHeader.background": c["surface2"],
        "notificationToast.border": c["line"], "notificationLink.foreground": c["ink"],
        "notificationsErrorIcon.foreground": c["danger"], "notificationsWarningIcon.foreground": c["number"],
        "notificationsInfoIcon.foreground": c["focus"],
        # editor
        "editor.background": c["bg"], "editor.foreground": c["text"],
        "editorLineNumber.foreground": c["secondary"] + "80", "editorLineNumber.activeForeground": pc,
        "editorCursor.foreground": c["ink"] if dark else c["primary"],
        "editor.selectionBackground": c["sel"], "editor.inactiveSelectionBackground": c["selHi"],
        "editor.selectionHighlightBackground": c["selHi"], "editor.wordHighlightBackground": c["hover"],
        "editor.wordHighlightStrongBackground": c["selHi"], "editor.findMatchBackground": c["number"] + "59",
        "editor.findMatchBorder": c["number"], "editor.findMatchHighlightBackground": c["number"] + "2e",
        "editor.findRangeHighlightBackground": c["hover"], "editor.hoverHighlightBackground": c["selHi"],
        "editor.lineHighlightBackground": c["lineHl"],
        "editor.lineHighlightBorder": "#00000000", "editor.rangeHighlightBackground": c["hover"],
        "editorLink.activeForeground": c["ink"], "editorWhitespace.foreground": c["secondary"] + "40",
        "editorIndentGuide.background1": c["lineSoft"], "editorIndentGuide.activeBackground1": c["primary"] + "80",
        "editorRuler.foreground": c["lineSoft"], "editorCodeLens.foreground": c["secondary"],
        "editorBracketMatch.background": c["tint"], "editorBracketMatch.border": c["focus"] + "99",
        "editorBracketHighlight.foreground1": c["ink"] if dark else c["keyword"],
        "editorBracketHighlight.foreground2": c["type"], "editorBracketHighlight.foreground3": c["number"],
        "editorBracketHighlight.foreground4": c["string"], "editorBracketHighlight.foreground5": c["attr"],
        "editorBracketHighlight.foreground6": c["prop"],
        "editorBracketHighlight.unexpectedBracket.foreground": c["danger"],
        "editorError.foreground": c["danger"], "editorWarning.foreground": c["number"],
        "editorInfo.foreground": c["focus"], "editorHint.foreground": c["string"],
        "editorGutter.background": c["bg"], "editorGroup.emptyBackground": c["bg"], "editorGutter.addedBackground": c["success"],
        "editorGutter.modifiedBackground": c["focus"], "editorGutter.deletedBackground": c["danger"],
        "editorOverviewRuler.border": "#00000000", "editorOverviewRuler.addedForeground": c["success"] + "99",
        "editorOverviewRuler.modifiedForeground": c["focus"] + "99",
        "editorOverviewRuler.deletedForeground": c["danger"] + "99",
        "editorOverviewRuler.errorForeground": c["danger"], "editorOverviewRuler.warningForeground": c["number"],
        "editorOverviewRuler.findMatchForeground": c["number"] + "99",
        "editorInlayHint.background": c["surface2"], "editorInlayHint.foreground": c["secondary"],
        "editorGhostText.foreground": c["secondary"] + "b3", "editorStickyScroll.background": c["bg"],
        "editorStickyScrollHover.background": c["hover"], "editorStickyScroll.shadow": c["shadow"],
        "minimap.selectionHighlight": c["sel"], "minimap.findMatchHighlight": c["number"] + "99",
        "minimapSlider.background": "#80808026", "minimapSlider.hoverBackground": "#80808040",
        "minimapSlider.activeBackground": c["primary"] + "66",
        # tabs / groups / breadcrumbs
        "editorGroup.border": c["lineSoft"], "editorGroup.dropBackground": c["tint"],
        "editorGroupHeader.tabsBackground": c["surface"], "editorGroupHeader.tabsBorder": c["lineSoft"],
        "editorGroupHeader.noTabsBackground": c["bg"],
        "tab.activeBackground": c["bg"], "tab.activeForeground": pc,
        "tab.activeBorderTop": c["primary"] if not dark else c["focus"], "tab.activeBorder": c["bg"],
        "tab.inactiveBackground": c["surface"], "tab.inactiveForeground": c["secondary"],
        "tab.hoverBackground": c["hover"], "tab.hoverForeground": c["text"], "tab.border": c["lineSoft"],
        "tab.unfocusedActiveForeground": c["secondary"], "tab.unfocusedActiveBorderTop": c["line"],
        "tab.unfocusedInactiveForeground": c["secondary"] + "b3", "tab.activeModifiedBorder": c["ink"],
        "tab.inactiveModifiedBorder": c["secondary"],
        "breadcrumb.background": c["bg"], "breadcrumb.foreground": c["secondary"],
        "breadcrumb.focusForeground": pc, "breadcrumb.activeSelectionForeground": c["ink"],
        "breadcrumbPicker.background": c["surface"],
        # panel / terminal
        "panel.background": c["panel"], "panel.border": c["lineSoft"],
        "panelTitle.activeForeground": pc, "panelTitle.inactiveForeground": c["secondary"],
        "panelTitle.activeBorder": c["primary"] if not dark else c["focus"],
        "panelSection.border": c["lineSoft"], "panelInput.border": c["line"],
        "terminal.background": c["panel"], "terminal.foreground": c["text"],
        "terminal.selectionBackground": c["sel"], "terminalCursor.foreground": c["ink"] if dark else c["primary"],
        "terminal.border": c["lineSoft"],
        "terminal.ansiBlack": a["black"], "terminal.ansiRed": a["red"], "terminal.ansiGreen": a["green"],
        "terminal.ansiYellow": a["yellow"], "terminal.ansiBlue": a["blue"], "terminal.ansiMagenta": a["magenta"],
        "terminal.ansiCyan": a["cyan"], "terminal.ansiWhite": a["white"],
        "terminal.ansiBrightBlack": a["bblack"], "terminal.ansiBrightRed": a["bred"],
        "terminal.ansiBrightGreen": a["bgreen"], "terminal.ansiBrightYellow": a["byellow"],
        "terminal.ansiBrightBlue": a["bblue"], "terminal.ansiBrightMagenta": a["bmagenta"],
        "terminal.ansiBrightCyan": a["bcyan"], "terminal.ansiBrightWhite": a["bwhite"],
        # status bar
        "statusBar.background": c["status"], "statusBar.foreground": c["statusFg"],
        "statusBar.border": c["lineSoft"], "statusBar.focusBorder": c["focus"],
        "statusBar.noFolderBackground": c["status"], "statusBar.noFolderForeground": c["statusFg"],
        "statusBar.debuggingBackground": c["primary"] if dark else c["attr"], "statusBar.debuggingForeground": on_primary,
        "statusBarItem.hoverBackground": c["statusHover"], "statusBarItem.hoverForeground": c["statusFg"] if not dark else c["text"],
        "statusBarItem.activeBackground": c["statusHover"], "statusBarItem.remoteBackground": c["primary"] if dark else c["ink"],
        "statusBarItem.remoteForeground": on_primary, "statusBarItem.prominentBackground": c["statusHover"],
        "statusBarItem.errorBackground": c["danger"], "statusBarItem.errorForeground": "#ffffff",
        "statusBarItem.warningBackground": c["number"], "statusBarItem.warningForeground": "#000000",
        # git / diff
        "gitDecoration.addedResourceForeground": c["string"],
        "gitDecoration.untrackedResourceForeground": c["string"],
        "gitDecoration.modifiedResourceForeground": c["ink"] if dark else c["keyword"],
        "gitDecoration.deletedResourceForeground": c["danger"],
        "gitDecoration.conflictingResourceForeground": c["attr"],
        "gitDecoration.ignoredResourceForeground": c["secondary"] + "99",
        "gitDecoration.submoduleResourceForeground": c["prop"],
        "diffEditor.insertedTextBackground": c["success"] + "26",
        "diffEditor.removedTextBackground": c["danger"] + "26",
        "diffEditor.insertedLineBackground": c["success"] + "14",
        "diffEditor.removedLineBackground": c["danger"] + "14", "diffEditor.border": c["lineSoft"],
        "merge.currentHeaderBackground": c["success"] + "66", "merge.currentContentBackground": c["success"] + "1f",
        "merge.incomingHeaderBackground": c["primary"] + "66", "merge.incomingContentBackground": c["primary"] + "1f",
        # misc
        "peekView.border": c["primary"], "peekViewEditor.background": c["surface"],
        "peekViewResult.background": c["surface"], "peekViewTitle.background": c["surface2"],
        "peekViewEditor.matchHighlightBackground": c["number"] + "40",
        "peekViewResult.matchHighlightBackground": c["number"] + "40",
        "peekViewResult.selectionBackground": c["tint"],
        "debugToolBar.background": c["surface2"], "debugIcon.breakpointForeground": c["danger"],
        "extensionButton.prominentBackground": c["primary"], "extensionButton.prominentForeground": on_primary,
        "extensionButton.prominentHoverBackground": c["focus"] if dark else "#3d84e4",
        "extensionBadge.remoteBackground": c["primary"], "extensionBadge.remoteForeground": on_primary,
        "settings.headerForeground": c["text"], "settings.modifiedItemIndicator": c["focus"],
        "settings.focusedRowBackground": c["hover"], "settings.rowHoverBackground": c["hover"] ,
        "welcomePage.tileBackground": c["surface"], "welcomePage.tileHoverBackground": c["surface2"],
        "welcomePage.tileBorder": c["lineSoft"], "walkThrough.embeddedEditorBackground": c["surface"],
        "chat.requestBackground": c["surface"], "chat.slashCommandBackground": c["tint"],
        "chat.slashCommandForeground": c["ink"], "charts.blue": a["blue"], "charts.red": c["danger"],
        "charts.green": c["string"], "charts.yellow": c["number"], "charts.orange": c["attr"],
        "charts.purple": c["type"], "charts.foreground": c["text"], "charts.lines": c["line"],
    }


def tokens(c):
    def t(name, scope, fg=None, style=None):
        s = {}
        if fg: s["foreground"] = fg
        if style is not None: s["fontStyle"] = style
        return {"name": name, "scope": scope, "settings": s}
    return [
        t("Comments", ["comment", "punctuation.definition.comment", "string.comment"], c["comment"], "italic"),
        t("Doc tags", ["storage.type.class.jsdoc", "keyword.other.phpdoc", "comment keyword.other"], c["prop"], "italic"),
        t("Keywords", ["keyword", "keyword.control", "storage", "storage.type", "storage.modifier",
                       "keyword.operator.new", "keyword.operator.expression", "keyword.operator.logical.python",
                       "variable.language.this", "variable.language.self", "variable.language.super"], c["keyword"]),
        t("Operators & punctuation", ["keyword.operator", "punctuation", "meta.brace", "punctuation.separator",
                                      "punctuation.terminator", "punctuation.accessor"], c["punct"]),
        t("Strings", ["string", "string.quoted", "string.template", "markup.inline.raw", "markup.fenced_code"], c["string"]),
        t("Template expression", ["punctuation.definition.template-expression", "punctuation.section.embedded"], c["keyword"]),
        t("Escapes & regex", ["constant.character.escape", "string.regexp", "constant.other.character-class"], c["attr"]),
        t("Numbers & constants", ["constant.numeric", "constant.language", "constant.character",
                                  "constant.other", "variable.other.constant", "support.constant",
                                  "variable.other.enummember"], c["number"]),
        t("Functions", ["entity.name.function", "support.function", "meta.function-call entity.name.function",
                        "variable.function", "entity.name.method"], c["func"]),
        t("Types & classes", ["entity.name.type", "entity.name.class", "entity.other.inherited-class",
                              "support.type", "support.class", "entity.name.namespace", "storage.type.cs",
                              "storage.type.java", "entity.name.type.interface", "meta.type.annotation entity.name.type"], c["type"]),
        t("Decorators", ["meta.decorator", "entity.name.function.decorator", "punctuation.decorator"], c["attr"]),
        t("Variables", ["variable", "variable.other.readwrite", "meta.definition.variable"], c["text"]),
        t("Parameters", ["variable.parameter", "meta.parameter"], c["param"], "italic"),
        t("Properties", ["variable.other.property", "variable.other.object.property", "support.variable.property",
                         "meta.object-literal.key", "entity.name.tag.yaml", "support.type.property-name",
                         "support.type.property-name.json"], c["prop"]),
        t("HTML/XML tags", ["entity.name.tag", "punctuation.definition.tag", "meta.tag.sgml"], c["keyword"]),
        t("Components (JSX)", ["support.class.component", "entity.name.tag.component"], c["type"]),
        t("Attributes", ["entity.other.attribute-name"], c["attr"]),
        t("CSS selectors", ["entity.other.attribute-name.class.css", "entity.other.attribute-name.id.css",
                            "entity.name.tag.css", "entity.other.attribute-name.pseudo-class.css"], c["func"]),
        t("CSS values / units", ["support.constant.property-value.css", "keyword.other.unit",
                                 "constant.other.color.rgb-value"], c["number"]),
        t("CSS variables", ["variable.css", "variable.argument.css", "support.type.custom-property"], c["prop"]),
        t("Markdown heading", ["markup.heading", "entity.name.section.markdown",
                               "punctuation.definition.heading.markdown"], c["keyword"], "bold"),
        t("Markdown bold", ["markup.bold"], None, "bold"),
        t("Markdown italic", ["markup.italic"], None, "italic"),
        t("Markdown strike", ["markup.strikethrough"], None, "strikethrough"),
        t("Markdown link", ["markup.underline.link", "string.other.link"], c["func"]),
        t("Markdown quote", ["markup.quote"], c["comment"], "italic"),
        t("Markdown list", ["punctuation.definition.list.begin.markdown"], c["attr"]),
        t("Diff inserted", ["markup.inserted", "meta.diff.header.to-file"], c["string"]),
        t("Diff deleted", ["markup.deleted", "meta.diff.header.from-file"], c["danger"]),
        t("Diff changed", ["markup.changed"], c["number"]),
        t("Invalid", ["invalid", "invalid.illegal"], c["danger"]),
        t("Deprecated", ["invalid.deprecated"], c["number"], "strikethrough"),
    ]


def semantic(c):
    return {
        "namespace": c["type"], "class": c["type"], "interface": c["type"], "enum": c["type"],
        "type": c["type"], "typeParameter": c["type"], "function": c["func"], "method": c["func"],
        "decorator": c["attr"], "macro": c["attr"], "parameter": {"foreground": c["param"], "italic": True},
        "property": c["prop"], "enumMember": c["number"], "variable": c["text"],
        "variable.readonly": c["number"], "variable.defaultLibrary": c["number"],
        "keyword": c["keyword"], "regexp": c["attr"], "string": c["string"], "number": c["number"],
        "comment": {"foreground": c["comment"], "italic": True}, "*.deprecated": {"strikethrough": True},
    }


def theme(kind):
    c = P[kind]
    dark = kind == "dark"
    return {
        "$schema": "vscode://schemas/color-theme",
        "name": f"EliasDH {'Dark' if dark else 'Light'}",
        "type": kind,
        "semanticHighlighting": True,
        "colors": colors(c, dark),
        "tokenColors": tokens(c),
        "semanticTokenColors": semantic(c),
    }


os.makedirs(os.path.join(ROOT, "themes"), exist_ok=True)
for k in ("dark", "light"):
    with open(os.path.join(ROOT, "themes", f"eliasdh-{k}-color-theme.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(theme(k), f, indent=4)
        f.write("\n")

# --- .vsix (a zip with a manifest) ---
manifest = f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
  <Metadata>
    <Identity Language="en-US" Id="{pkg['name']}" Version="{VERSION}" Publisher="{pkg['publisher']}" />
    <DisplayName>{pkg['displayName']}</DisplayName>
    <Description xml:space="preserve">{pkg['description']}</Description>
    <Tags>theme,color-theme,dark,light</Tags>
    <Categories>Themes</Categories>
    <GalleryFlags>Public</GalleryFlags>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="{pkg['engines']['vscode']}" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="ui,workspace" />
    </Properties>
    <Icon>extension/icon.png</Icon>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code"/>
  </Installation>
  <Dependencies/>
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Content.Details" Path="extension/README.md" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Content.License" Path="extension/LICENSE.md" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Icons.Default" Path="extension/icon.png" Addressable="true" />
  </Assets>
</PackageManifest>
"""
content_types = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension=".json" ContentType="application/json"/><Default Extension=".md" ContentType="text/markdown"/><Default Extension=".png" ContentType="image/png"/><Default Extension=".vsixmanifest" ContentType="text/xml"/></Types>
"""
os.makedirs(os.path.join(ROOT, "Release"), exist_ok=True)
vsix = os.path.join(ROOT, "Release", f"eliasdh-theme-{VERSION}.vsix")
with zipfile.ZipFile(vsix, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("extension.vsixmanifest", manifest)
    z.writestr("[Content_Types].xml", content_types)
    for rel in ("package.json", "README.md", "LICENSE.md", "icon.png",
                "themes/eliasdh-dark-color-theme.json", "themes/eliasdh-light-color-theme.json"):
        z.write(os.path.join(ROOT, rel), "extension/" + rel)
print("Built", os.path.relpath(vsix, ROOT))
