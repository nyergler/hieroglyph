(function(){

SlideDeck.prototype.BUILD_ITEM_RE = /build-item-(\d+)(-only)?/;

SlideDeck.prototype.makeBuildLists_ = function () {
  for (var i = this.curSlide_, slide; slide = this.slides[i]; ++i) {
    var items = slide.querySelectorAll('.build > *');

    for (var j = 0, item; item = items[j]; ++j) {
      if (item.classList) {
        item.classList.add('to-build');
        if (item.parentNode.classList.contains('fade')) {
          item.classList.add('fade');
        }
      }
    }

    var items = slide.querySelectorAll('[class*="build-item-"]');
    if (items.length) {
        slide._buildItems = [];
    };
    for (var j = 0, item; item = items[j]; ++j) {
      if (item.classList) {
        item.classList.add('to-build');
        if (!item.parentNode.classList.contains('build')) {
            item.parentNode.classList.add('build');
        }
        if (item.parentNode.classList.contains('fade')) {
          item.classList.add('fade');
        }
      }

      var build_info = this.BUILD_ITEM_RE.exec(item.classList),
          build_index = build_info[1],
          build_only = build_info[2];
      if (slide._buildItems[build_index] === undefined) {
          slide._buildItems[build_index] = [];
      }
      slide._buildItems[build_index].push(item);

      if (build_only) {
          // add the data-attribute
          item.setAttribute('data-show-only', build_index);
      }
    }

  }
};

SlideDeck.prototype.buildNextBuildItem_ = SlideDeck.prototype.buildNextItem_;

SlideDeck.prototype.buildNextItem_ = function() {

    var slide = this.slides[this.curSlide_];
    var built = slide.querySelectorAll('.build-current');

    var buildItems = slide.querySelectorAll('[class*="build-item-"]');
    var show_items;

    // Remove the classes from the previously built item
    if (built) {
        for (var j = 0, built_item; built_item = built[j]; ++j) {
            built_item.classList.remove('build-current');
            if (built_item.classList.contains('fade')) {
                built_item.classList.add('build-fade');
            }

            if (built_item.getAttribute('data-show-only')) {
                built_item.classList.add('build-hide');
            }
        };
    }

    if (slide._buildItems && slide._buildItems.length) {
        while ((show_items = slide._buildItems.shift()) === undefined) {};
        if (show_items) {

            // show the next items
            show_items.forEach(function(item, index, items) {
                item.classList.remove('to-build');
                item.classList.add('build-current');
            });

            return true;
        }
    }

    return this.buildNextBuildItem_();

};

}());
