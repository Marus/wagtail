(function() {
  (function($) {
    return $.widget("IKS.hallowagtailsnippets", {
      options: {
        uuid: '',
        editable: null,
        content_types: []
      },
      populateToolbar: function(toolbar) {
        var button, widget;

        widget = this;
        var buttonset = $('<span class="' + widget.widgetName + '\"></span>');

        var makeButton = function(app_label, model_name, label) {
          button = $('<span></span>');
          button.hallobutton({
            uuid: widget.options.uuid,
            editable: widget.options.editable,
            label: label,
            icon: 'icon-snippet icon-snippet-' + model_name,
            command: null
          });
          buttonset.append(button);
          return button.on("click", function(event) {
            var insertionPoint, lastSelection;

            lastSelection = widget.options.editable.getSelection();
            insertionPoint = $(lastSelection.endContainer).parentsUntil('.richtext').last();
            return ModalWorkflow({
              url: window.chooserUrls.snippetChooser + app_label + '/' + model_name + '/',
              responses: {
                snippetChosen: function(embedData) {
                  console.log(embedData);
                  var elem;
                  elem = $('<div contenteditable="false">');
                  elem.attr('data-id', embedData.id);
                  elem.attr('data-snippet-type', embedData.app_label + '.' + embedData.model_name);
                  elem.attr('data-embedtype', 'snippet');
                  elem.text('Snippet: ' + embedData.id + ' (' + embedData.app_label + '.' + embedData.model_name + ')');
                  lastSelection.insertNode(elem.get(0));
                  insertRichTextDeleteControl(elem);
                  return widget.options.editable.element.trigger('change');
                }
              }
            });
          });
        }
        
        var types = this.options.content_types;
        for(var i = 0; i < types.length; i++) {
          var ct = types[i];
          makeButton(ct.app_label, ct.model_name, ct.label);
        }

        buttonset.hallobuttonset();
        return toolbar.append(buttonset);
      }
    });
  })(jQuery);

}).call(this);