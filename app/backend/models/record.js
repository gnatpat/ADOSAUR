/*jslint node: true */

/* Record mongoose schema */
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
