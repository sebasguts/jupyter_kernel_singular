// Notebook Extension to allow singular Mode on Jupyter

define([
  'base/js/namespace',
  './singular'
], function (Jupyter) {
  "use strict";

  return {
    load_ipython_extension: function () {
      console.log('Loading singular Mode...');
    }
  };

});
