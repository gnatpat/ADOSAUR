/*jslint node: true */

/* Immediately-invoked function (containing all other functions) - invokes strict mode globally */
(function () {
  'use strict';

  module.exports = function (Schema, ObjectId) {
    var User = new Schema();

    User.add({
      uid         : String,
      pwd         : String,
      email       : String,
      first_name  : String,
      last_name   : String,
      profile_pic : String,
      dob         : Date,
      doctor      : Boolean,
      patients    : [ObjectId],
      tests       : [ObjectId],
      texts       : [ObjectId]
    });
    /*TODO: encrypt passwords */
    User.methods.validPassword = function (password) {
      return this.pwd === password;
    };
    return User;
  };
}());
