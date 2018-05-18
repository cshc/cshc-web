/**
 * Count quantity wrapper.
 *
 * @author Htmlstream
 * @version 1.0
 *
 */
(function ($) {
  $.HSCore.components.HSCountQty = {
    /**
     *
     *
     * @var Object _baseConfig
     */
    _baseConfig: {},

    /**
     *
     *
     * @var jQuery pageCollection
     */
    pageCollection: $(),

    /**
     * Initialization of Count quantity wrapper.
     *
     * @param String selector (optional)
     * @param Object config (optional)
     *
     * @return jQuery pageCollection - collection of initialized items.
     */

    init(selector, config) {
      this.collection = selector && $(selector).length ? $(selector) : $();
      if (!$(selector).length) return;

      this.config =
        config && $.isPlainObject(config)
          ? $.extend({}, this._baseConfig, config)
          : this._baseConfig;

      this.config.itemSelector = selector;

      this.initCountQty();

      return this.pageCollection;
    },

    initCountQty() {
      // Variables
      let $self = this,
        collection = $self.pageCollection;

      // Actions
      this.collection.each((i, el) => {
        // Variables
        let $this = $(el),
          $plus = $this.find('.js-plus'),
          $minus = $this.find('.js-minus'),
          $result = $this.find('.js-result'),
          resultVal = parseInt($result.val()),
          min = parseInt($result.attr('min') || '0'),
          max = parseInt($result.attr('max') || '100000000');

        $result.keypress((e) => {
          // Ref: https://stackoverflow.com/a/42630560
          // Check for a positive integer
          const charCode = e.which ? e.which : e.keyCode;
          if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
          }
          return true;
        });

        $result.change((e) => {
          resultVal = Math.min(Math.max(parseInt(e.target.value), min), max);
          $result.val(resultVal);
        });

        $plus.on('click', (e) => {
          e.preventDefault();

          if (resultVal < max) {
            resultVal += 1;

            $result.val(resultVal);
          } else {
            return false;
          }
        });

        $minus.on('click', (e) => {
          e.preventDefault();

          if (resultVal > min) {
            resultVal -= 1;

            $result.val(resultVal);
          } else {
            return false;
          }
        });

        // Actions
        collection = collection.add($this);
      });
    },
  };
}(jQuery));
