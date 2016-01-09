/*jslint node: true */

(function () {
  'use strict';

  module.exports = function (router, models, passport) {

    /* logs the user in */
    router.post('/login', function (req, res, next) {
      // authenticate user
      passport.authenticate('local', function (err, user, info) {
        // if there is an error
        if (err) { return next(err); }
        // if authentication fails
        if (!user) {
          return res.redirect('/#/login?err=' + info.message);
        }
        // if authentication succeeds
        req.logIn(user, function (err) {
          if (err) {
            return next(err);
          }
          // if everything is fine
          return res.redirect('/#/doctor/' + user.uid);
        });
      })(req, res, next);
    });

    /* logs the user out, must be loged in */
    router.get('/logout', passport.isAuthenticated, function (req, res) {
      req.logout();
      res.redirect('/');
    });
  };
}());
