/*jslint node: true */

/* Immediately-invoked function (containing all other functions) - invokes strict mode globally */
(function () {
  'use strict';

  module.exports = function (Schema) {
    var Text = new Schema();

    Text.add({
      Title   : String,
      Content : String,
      Comments: String
    });
    return Text;
  };
}());
