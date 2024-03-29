(function () {
  'use strict';

/* mongoose Test schema */
  module.exports = function (Schema, ObjectId) {
    var Test = new Schema();

    Test.add({
      doctor  : ObjectId,
      patient : ObjectId,
      text    : ObjectId,
      type    : String,
      result  : Number,
      done    : Boolean,
      seen    : Boolean
    });
    return Test;
  };
}());
