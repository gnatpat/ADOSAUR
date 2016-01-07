/*jslint node: true */

(function () {
  'use strict';

  module.exports = function (router, models, passport) {

    router.post('/login', passport.authenticate('local', {
      successRedirect: '/',
      failureRedirect: '/#/login'
    }));
  };
}());
