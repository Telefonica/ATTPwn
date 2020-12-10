/* jquery treed plugin */
(function ($) {
    $.fn.treed = function (options) {
        var settings = $.extend({
            openedClass: 'fa-folder-open',
            closedClass: 'fa-folder',
        }, options || {});

        return this.each(function () {
            var $tree = $(this);
            $tree.addClass('tree');
            $tree.find('li').has('ul').each(function () {
                var $branch = $(this); //li with children ul
                $branch.prepend('<i class="indicator fa ' + settings.closedClass + '" aria-hidden="true"></i>');
                $branch.addClass('branch collapsed');
                $branch.on('click', function (e) {
                    if (this == e.target) {
                        var icon = $(this).children('i:first');
                        $(this).toggleClass('expanded collapsed');
                        icon.toggleClass(settings.openedClass + ' ' + settings.closedClass);
                        $(this).children().children().toggle();
                    }
                });
                $branch.children().children().toggle();
            });
            //fire event from the dynamically added icon
            $tree.on('click', '.branch .indicator', function() {
                $(this).closest('li').click();
            });
            //fire event to open branch if the li contains an anchor or button instead of text
            $tree.on('click', '.branch > a, .branch > button', function() {
                e.preventDefault();
                $(this).closest('li').click();
            });
        });
    };
})(jQuery);
