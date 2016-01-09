/*jslint node: true */

(function () {
  'use strict';

  module.exports = function (router, models, passport) {

    router.post('/login', passport.authenticate('local'), function (req, res) {
      res.redirect('/#/doctor/' + req.body.username);
    });
  };
}());
