(function () {
  'use strict';

  module.exports = function (Schema, ObjectId) {
    var Test = new Schema();

    Test.add({
      doctor  : ObjectId,
      patient : ObjectId,
      text    : ObjectId,
      type    : String,
      result  : Number
    });
    return Test;
  };
}());
