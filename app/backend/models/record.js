/*jslint node: true */

/* Immediately-invoked function (containing all other functions) - invokes strict mode globally */
(function () {
  'use strict';

  module.exports = function (Schema, ObjectId) {
    var Record = new Schema();

    Record.add({
      patient: ObjectId,
      text   : ObjectId,
      result : Object
    });
    return Record;
  };
}());
