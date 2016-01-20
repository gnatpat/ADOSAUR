/*jslint node: true */

/* mongoose text Schema */
(function () {
  'use strict';

  module.exports = function (Schema) {
    var Text = new Schema();

    Text.add({
      title   : String,
      content : String,
      comments: String
    });
    return Text;
  };
}());
