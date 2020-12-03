/* flaskcode scripts */
'use strict';

var flaskcode = window.flaskcode || {};

require.config({
    baseUrl: flaskcode.config.get('pluginsBaseUrl'),
    paths: { 'vs': 'monaco-editor/min/vs' }
});

flaskcode.editorWidget = {
    editor: null,
    resourceName: null,
    editorState: null,
};
flaskcode.editorElement = null;

flaskcode.languages = [];
flaskcode.defaultExt = 'ps1';
flaskcode.defaultLangId = 'powershell';
flaskcode.defaultLang = null;
flaskcode.fallbackLang = null;

flaskcode.$editorContainer = null;
flaskcode.$editorBody = null;
flaskcode.$editorLoader = null;
flaskcode.$pagePreloader = null;

flaskcode.editorStates = {
    INIT: 'init',
    LOADED: 'loaded',
    MODIFIED: 'modified',
    BUSY: 'busy',
};

flaskcode.defaultEditorTheme = 'vs-dark';
flaskcode.availableEditorThemes = ['vs', 'vs-dark', 'hc-black'];

flaskcode.APP_BUSY = false;

flaskcode.allowedLangIds = [];

flaskcode.onStateChange = $.noop;

flaskcode.editorTheme = function() {
    var theme = flaskcode.config.get('editorTheme', flaskcode.defaultEditorTheme);
    return flaskcode.availableEditorThemes.indexOf(theme) > -1 ? theme : flaskcode.defaultEditorTheme;
};

flaskcode.setEditorState = function(state) {
    var prevState = flaskcode.editorWidget.editorState;
    flaskcode.editorWidget.editorState = state;
    if (flaskcode.editorWidget.editorState != prevState) {
        flaskcode.onStateChange(flaskcode.editorWidget.editorState);
    }
};

flaskcode.getExt = function(filename) {
    var m = filename.match(/\.(\w*)$/i);
    return (m && m.length > 1) ? m[1].toLowerCase() : null;
};

flaskcode.getResourceExt = function(resource_url) {
    var m = resource_url.match(/\.(\w*)\.txt$/i);
    return (m && m.length > 1) ? m[1].toLowerCase() : null;
};

flaskcode.getLanguageById = function(langId) {
    return flaskcode.languages.find(function(lang) {
        return lang.id == langId;
    });
};

flaskcode.getLanguageByExtension = function(extension) {
    return flaskcode.languages.find(function(lang) {
        return lang.extensions.indexOf('.' + extension) > -1;
    });
};

flaskcode.getLanguageByMimetype = function(mimetype) {
    return flaskcode.languages.find(function(lang) {
        return lang.mimetypes.indexOf(mimetype) > -1;
    });
};

flaskcode.minimapEnabled = function(minimapFlag) {
    if (typeof minimapFlag === 'undefined') {
        var flag = flaskcode.storage.get('flaskcodeMinimapEnabled');
        return flag === null ? true : !!parseInt(flag);
    } else {
        if (flaskcode.editorWidget.editor) {
            flaskcode.editorWidget.editor.updateOptions({ minimap: { enabled: !!minimapFlag } });
            flaskcode.storage.set('flaskcodeMinimapEnabled', Number(!!minimapFlag));
        }
    }
};

flaskcode.notifyEditor = function(message, category) {
    var msgType = category == 'error' ? 'danger' : 'success';
    var $msg = $('<div class="alert alert-dismissible alert-' + msgType + '" role="alert">' +
        '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><i class="fa fa-times" aria-hidden="true"></i></button>' +
        '<strong>' + message + '</strong>' +
        '</div>');
    $msg.autoremove(msgType == 'success' ? 5 : 10);
    flaskcode.$editorContainer.find('.editor-notification').empty().append($msg);
};

flaskcode.editorBodyMsg = function(content) {
    return $('<div class="editor-body-msg">' + content + '</div>');
};

flaskcode.resetSelectedResource = function() {
    $('ul#dir-tree .file-item').removeClass('selected');
};

flaskcode.highlightSelectedResource = function(filePath, parentPath) {
    flaskcode.resetSelectedResource();
    var $selectedElement = $('ul#dir-tree .file-item[data-path-name="' + filePath + '"]');
    if ($selectedElement.length) {
        $selectedElement.addClass('selected');
    } else if (parentPath) {
        var $parentItem = $('.dir-item[data-path-name="' + parentPath + '"]');
        if ($parentItem.length) {
            var $parentElement = $parentItem.find('ul:first');
            var $treeItem = $parentElement.find('li.file-item:first');
            if ($treeItem.length) {
                var fileName = filePath.replace(parentPath + '/', '');
                var resource_url = flaskcode.config.get('resourceUrlTemplate').replace('__pathname__', filePath);
                $parentElement.prepend(
                    $treeItem.clone().removeClass('dir-item').addClass('file-item selected').text(fileName).attr({
                        'title': fileName,
                        'data-path-name': filePath,
                        'data-url': resource_url,
                    }).data({
                        pathName: filePath,
                        url: resource_url,
                    })
                );
                if ($parentItem.hasClass('collapsed')) {
                    $parentItem.click();
                }
            }
        }
    }
    $('#editor-header #resource-name').text(flaskcode.strTruncateLeft(filePath)).attr('title', filePath);
};

flaskcode.notifyCursorPosition = function(position) {
    if (position) {
        $('span#line_num').text(position.lineNumber);
        $('span#column_num').text(position.column);
    } else {
        $('span#line_num').text('');
        $('span#column_num').text('');
    }
};

flaskcode.notifyLanguage = function(lang) {
    if (lang && lang.aliases.length) {
        $('span#editor_lang').text(lang.aliases[0]);
    } else {
        $('span#editor_lang').text('');
    }
};

flaskcode.onEditorStateChange = function(state) {
    if (state == flaskcode.editorStates.LOADED) {
        $('#resource-close').show();
    }
    if (state == flaskcode.editorStates.MODIFIED) {
        $('#resource-mod').show();
    } else if (state != flaskcode.editorStates.BUSY) {
        $('#resource-mod').hide();
    }
};

flaskcode.onEditorSave = function(editor) {
    if (flaskcode.editorWidget.editorState != flaskcode.editorStates.MODIFIED /* && !editor.hasWidgetFocus()*/ ) {
        return null;
    }

    var filePath = flaskcode.$editorContainer.data('filePath');
    var isNewResource = flaskcode.$editorContainer.data('isNewResource');

    if (!window.FormData) {
        flaskcode.notifyEditor('This browser does not support editor save', 'error');
    } else if (!filePath) {
        flaskcode.notifyEditor('Editor is not initialized properly. Reload page and try again.', 'error');
    } else {
        var prevState = flaskcode.editorWidget.editorState;
        var data = new FormData();
        data.set('resource_data', editor.getValue());
        data.set('is_new_resource', Number(isNewResource));
        console.log(flaskcode);
        console.log("fichero..." + filePath);
        $.ajax({
            type: 'POST',
            // url: flaskcode.config.get('updateResourceBaseUrl') + filePath,
            url: "/update-resource-data/" + filePath,

            data: data,
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function(xhr, settings) {
                flaskcode.setEditorState(flaskcode.editorStates.BUSY);
                flaskcode.$editorLoader.addClass('transparent').show();
            },
            success: function(data, status, xhr) {
                if (status == 'success' && data.success) {
                    flaskcode.setEditorState(flaskcode.editorStates.LOADED);
                    flaskcode.notifyEditor(data.message || 'Saved!');
                    if (flaskcode.$editorContainer.data('isNewResource')) {
                        flaskcode.highlightSelectedResource(filePath, flaskcode.dirname(filePath).replace(/^\/+|\/+$/gm, ''));
                        flaskcode.$editorContainer.data('isNewResource', false);
                    }
                } else {
                    flaskcode.setEditorState(prevState);
                    flaskcode.notifyEditor(data.message || 'Error!', 'error');
                }
            },
            error: function(xhr, status, err) {
                flaskcode.setEditorState(prevState);
                flaskcode.notifyEditor('Error: ' + err, 'error');
            },
            complete: function(xhr, status) {
                flaskcode.$editorLoader.hide().removeClass('transparent');
            },
        });
    }
    return null;
};

flaskcode.setEditorEvents = function(editor) {
    // save action
    editor.addAction({
        id: 'save',
        label: 'Save',
        keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_S],
        precondition: '!editorReadonly',
        keybindingContext: '!editorReadonly',
        contextMenuGroupId: '1_modification',
        contextMenuOrder: 1.5,
        run: flaskcode.onEditorSave,
    });

    // reload action
    editor.addAction({
        id: 'reload',
        label: 'Reload',
        keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_R],
        precondition: null,
        keybindingContext: null,
        contextMenuGroupId: 'navigation',
        contextMenuOrder: 1,
        run: function(ed) {
            if (flaskcode.editorWidget.editorState == flaskcode.editorStates.INIT || flaskcode.editorWidget.editorState == flaskcode.editorStates.LOADED) {
                flaskcode.loadEditor({ url: flaskcode.$editorContainer.data('url'), filePath: flaskcode.$editorContainer.data('filePath') }, true);
            } else if (flaskcode.editorWidget.editorState == flaskcode.editorStates.MODIFIED) {
                alert('Current changes not saved.');
                ed.focus();
            }
        },
    });

    // force reload action
    editor.addAction({
        id: 'force-reload',
        label: 'Force Reload',
        keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KEY_R],
        precondition: null,
        keybindingContext: null,
        contextMenuGroupId: 'navigation',
        contextMenuOrder: 1.1,
        run: function(ed) {
            if (flaskcode.editorWidget.editorState != flaskcode.editorStates.BUSY) {
                flaskcode.loadEditor({ url: flaskcode.$editorContainer.data('url'), filePath: flaskcode.$editorContainer.data('filePath') }, true);
            }
        },
    });

    // change event
    editor.onDidChangeModelContent(function(e) {
        flaskcode.setEditorState(flaskcode.editorStates.MODIFIED);
    });

    // cursor position change
    editor.onDidChangeCursorPosition(function(e) {
        flaskcode.notifyCursorPosition(e.position);
    });

    // state change event
    flaskcode.onStateChange = flaskcode.onEditorStateChange;
};

flaskcode.initEditorBody = function(editorId, resource, isNewResource) {
    flaskcode.$editorContainer.data('editorId', editorId);
    flaskcode.$editorContainer.data('url', resource.url);
    flaskcode.$editorContainer.data('filePath', resource.filePath);
    flaskcode.$editorContainer.data('isNewResource', !!isNewResource);
    flaskcode.highlightSelectedResource(resource.filePath);
    return flaskcode.$editorBody;
};

flaskcode.resetEditorBody = function() {
    flaskcode.$editorContainer.data('editorId', null);
    flaskcode.$editorContainer.data('url', null);
    flaskcode.$editorContainer.data('filePath', null);
    flaskcode.$editorContainer.data('isNewResource', false);
    return flaskcode.$editorBody.empty();
};

flaskcode.saveResourceState = function() {
    if (flaskcode.editorWidget.editor && flaskcode.editorWidget.editor.getModel() && flaskcode.editorWidget.resourceName) {
        flaskcode.storage.set(flaskcode.editorWidget.resourceName, JSON.stringify(flaskcode.editorWidget.editor.saveViewState()));
    }
};

flaskcode.restoreResourceState = function() {
    if (flaskcode.editorWidget.editor && flaskcode.editorWidget.editor.getModel() &&
        flaskcode.editorWidget.resourceName && flaskcode.storage.get(flaskcode.editorWidget.resourceName)) {
        flaskcode.editorWidget.editor.restoreViewState(JSON.parse(flaskcode.storage.get(flaskcode.editorWidget.resourceName)));
    }
};

flaskcode.setEditor = function(data, resource, isNewResource) {
    var resourceLang = flaskcode.getLanguageByExtension(flaskcode.getResourceExt(resource.url) || resource.extension || flaskcode.defaultExt) || flaskcode.getLanguageByMimetype(resource.mimetype);
    var lang = resourceLang || flaskcode.defaultLang || flaskcode.fallbackLang;

    if (!flaskcode.editorWidget.editor) {
        flaskcode.resetEditorBody();
        flaskcode.editorWidget.editor = monaco.editor.create(flaskcode.editorElement, {
            theme: flaskcode.editorTheme(),
            minimap: { enabled: flaskcode.minimapEnabled() },
            fontSize: 13,
            model: null,
        });
        flaskcode.setEditorEvents(flaskcode.editorWidget.editor);
    } else {
        flaskcode.saveResourceState();
    }

    var oldModel = flaskcode.editorWidget.editor.getModel();
    var newModel = monaco.editor.createModel(data, lang.id);
    flaskcode.editorWidget.editor.setModel(newModel);
    flaskcode.editorWidget.resourceName = resource.url;
    flaskcode.restoreResourceState();
    flaskcode.initEditorBody(flaskcode.editorWidget.editor.getId(), resource, isNewResource);

    flaskcode.setEditorState(flaskcode.editorStates.LOADED);
    flaskcode.editorWidget.editor.focus();
    flaskcode.notifyCursorPosition(flaskcode.editorWidget.editor.getPosition());
    flaskcode.notifyLanguage(lang);

    if (oldModel) {
        oldModel.dispose();
    }
};

flaskcode.clearEditor = function(alt_content) {
    if (flaskcode.editorWidget.editor) {
        if (flaskcode.editorWidget.editor.getModel()) {
            flaskcode.editorWidget.editor.getModel().dispose();
        }
        flaskcode.editorWidget.editor.dispose();
        flaskcode.editorWidget.editor = null;
        flaskcode.editorWidget.resourceName = null;
        flaskcode.setEditorState(flaskcode.editorStates.INIT);
    }
    flaskcode.resetEditorBody().append(alt_content || '');
    flaskcode.notifyCursorPosition(null);
    flaskcode.notifyLanguage(null);
};

flaskcode.loadEditor = function(resource, forceReload, isNewResource) {
    if (!forceReload && (flaskcode.editorWidget.resourceName == resource.url || (flaskcode.editorWidget.editorState == flaskcode.editorStates.MODIFIED && !confirm('Current changes not saved. Are you sure to move on without saving?')))) {
        flaskcode.editorWidget.editor.focus();
        return false;
    }
    if (isNewResource) {
        flaskcode.setEditor('', resource, isNewResource);
    } else {
        $.ajax({
            type: 'GET',
            url: resource.url,
            dataType: 'text',
            cache: false,
            beforeSend: function(xhr, settings) {
                flaskcode.$editorLoader.show();
            },
            success: function(data, status, xhr) {
                if (status == 'success') {
                    resource.mimetype = xhr.getResponseHeader('X-File-Mimetype');
                    resource.extension = xhr.getResponseHeader('X-File-Extension');
                    resource.encoding = xhr.getResponseHeader('X-File-Encoding');
                    flaskcode.setEditor(data, resource);
                } else {
                    flaskcode.clearEditor(flaskcode.editorBodyMsg('<h1 class="text-center">Error while loading file !</h1>'));
                }
            },
            error: function(xhr, status, err) {
                flaskcode.clearEditor(
                    flaskcode.editorBodyMsg(
                        '<h1 class="text-center">Error while loading file !</h1>' +
                        '<h2 class="text-center text-danger">' + err + '</h2>'
                    )
                );
            },
            complete: function(xhr, status) {
                flaskcode.$editorLoader.hide();
            },
        });
    }
};

flaskcode.validResource = function(filename) {
    var ext = flaskcode.getExt(filename);
    var lang = ext ? flaskcode.getLanguageByExtension(ext) : null;
    return lang ? flaskcode.allowedLangIds.indexOf(lang.id) > -1 : false;
};

flaskcode.openResource = function($resourceElement) {
    flaskcode.loadEditor({ url: $resourceElement.data('url'), filePath: $resourceElement.data('pathName') });
    return true;
};

flaskcode.openNewFileModal = function($resourceElement) {
    var $modal = $('#fileNameModal');
    $modal.find('.modal-title').text('Create New File');
    $modal.find('#base_url').val($resourceElement.data('url').replace(/\.txt$/i, ''));
    $modal.find('#base_path_name').val($resourceElement.data('pathName'));
    $modal.find('.base-path-name').text($resourceElement.data('pathName'));
    $modal.find('#new_filename').val('');
    $modal.modal({ show: true, backdrop: 'static' });
};

$(function() {
    flaskcode.$pagePreloader = $('div#page-preloader');
    flaskcode.$editorContainer = $('div#editor-container');
    flaskcode.$editorBody = flaskcode.$editorContainer.find('.editor-body');
    flaskcode.$editorLoader = flaskcode.$editorContainer.find('.editor-preloader');
    flaskcode.editorElement = flaskcode.$editorBody.get(0);

    $('ul#dir-tree').treed();
    flaskcode.setEditorState(flaskcode.editorStates.INIT);

    require(['vs/editor/editor.main'], function() {
        flaskcode.languages = monaco.languages.getLanguages();
        flaskcode.allowedLangIds = flaskcode.languages.map(function(lang) { return lang.id; });
        flaskcode.defaultLang = flaskcode.getLanguageByExtension(flaskcode.defaultExt);
        flaskcode.fallbackLang = flaskcode.getLanguageById(flaskcode.defaultLangId);

        $('ul#dir-tree').on('click', '.file-item', function() {
            return flaskcode.openResource($(this));
        });

        $('.header-actions').on('click', function() {
            if (flaskcode.editorWidget.editor) {
                flaskcode.editorWidget.editor.trigger('mouse', $(this).data('actionId'));
            }
        });

        $('#toggle-minimap').on('click', function() {
            flaskcode.minimapEnabled(!flaskcode.minimapEnabled());
        });

        $.contextMenu({
            selector: 'ul#dir-tree .resource-items',
            autoHide: false,
            build: function($trigger, e) {
                var items = {
                    'title': { name: $trigger.data('pathName'), icon: 'fa-tag', disabled: true },
                    'sep': '---------'
                };
                if ($trigger.hasClass('dir-item')) {
                    items['title']['icon'] = 'fa-folder';
                    if ($trigger.hasClass('expanded')) {
                        items['toggle_collapse'] = { name: 'Collapse', icon: 'fa-compress' };
                    } else {
                        items['toggle_collapse'] = { name: 'Expand', icon: 'fa-expand' };
                    }
                    items['create_new_file'] = { name: 'Create New File', icon: 'fa-file-code-o' };
                } else {
                    items['title']['icon'] = 'fa-file';
                    items['open'] = { name: 'Open', icon: 'fa-external-link', disabled: $trigger.hasClass('selected') };
                }
                return {
                    items: items,
                    callback: function(key, options) {
                        switch (key) {
                            case 'toggle_collapse':
                                options.$trigger.click();
                                break;

                            case 'open':
                                flaskcode.openResource(options.$trigger);
                                break;

                            case 'create_new_file':
                                flaskcode.openNewFileModal(options.$trigger);
                                break;
                        }
                    },
                };
            },
            events: {
                show: function(options) {},
                hide: function(options) {},
            },
        });

        $('#fileNameModal').on('shown.bs.modal', function() {
            $(this).find('#new_filename').focus();
        });

        $('form#fileNameForm').on('submit', function(evt) {
            evt.preventDefault();
            var $form = $(this);
            var $button = $form.find('[type="submit"]');
            var base_url = $form.find('#base_url').val();
            var base_path_name = $form.find('#base_path_name').val();
            var new_filename = $form.find('#new_filename').val();
            if (!(new_filename && flaskcode.validResource(new_filename))) {
                $form.find('.form-msg').empty().append($('<span class="text-danger">Please enter valid file name.</span>').autoremove(10));
            } else {
                var resource_url = base_url + '/' + new_filename + '.txt';
                $.ajax({
                    type: 'HEAD',
                    url: resource_url,
                    dataType: 'text',
                    cache: false,
                    beforeSend: function(xhr, settings) {
                        $button.button('loading');
                    },
                    complete: function(xhr, status) {
                        $button.button('reset');
                    },
                }).done(function(data, status, xhr) {
                    $form.find('.form-msg').empty().append($('<span class="text-danger">This file already exists.</span>').autoremove(10));
                }).fail(function(xhr, status, err) {
                    if (xhr.status == 404) {
                        flaskcode.loadEditor({ url: resource_url, filePath: base_path_name + '/' + new_filename }, false, true);
                        $('#fileNameModal').modal('hide');
                    } else {
                        $form.find('.form-msg').empty().append($('<span class="text-danger">Internal Error: ' + err + '</span>').autoremove(10));
                    }
                });
            }
            return false;
        });

        $('#editor-header #resource-close').on('click', function() {
            if (flaskcode.editorWidget.editorState == flaskcode.editorStates.MODIFIED && !confirm('Close without saving?')) {
                return false;
            }
            flaskcode.saveResourceState();
            flaskcode.clearEditor();
            flaskcode.resetSelectedResource();
            $('#editor-header #resource-mod').hide();
            $('#editor-header #resource-name').text('').attr('title', '');
            $(this).hide();
        });

        $(window).on('resize', function() {
            if (flaskcode.editorWidget.editor) {
                flaskcode.editorWidget.editor.layout();
            }
        });

        $(window).on('beforeunload', function(evt) {
            if (flaskcode.APP_BUSY || flaskcode.editorWidget.editorState == flaskcode.editorStates.BUSY) {
                evt.preventDefault();
                evt.returnValue = 'App is working...';
                return evt.returnValue;
            }
        });

        flaskcode.$pagePreloader.fadeOut();
    });
});