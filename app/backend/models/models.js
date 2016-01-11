/*jslint node: true */

/* This file centralises all the mongoose schemas and exports them as models */

(function () {
  'use strict';
  /* get the schemas */
  var
    mongoose     = require('mongoose'),
    ObjectId     = mongoose.Schema.Types.ObjectId, /* MongoDB primary key type */
    Schema       = mongoose.Schema,
    UserSchema   = require('./user.js')(Schema, ObjectId),
    RecordSchema = require('./record.js')(Schema, ObjectId),
    TextSchema   = require('./text.js')(Schema, ObjectId),
    TestSchema   = require('./test.js')(Schema, ObjectId);

  /* export the mongoose schemas for further use */
  module.exports = {
    user  : mongoose.model('users', UserSchema),
    record: mongoose.model('debates', RecordSchema),
    text  : mongoose.model('texts', TextSchema),
    test  : mongoose.model('tests', TestSchema)
  };

}());
