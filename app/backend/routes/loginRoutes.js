/*jslint node: true */

(function () {
  'use strict';

  module.exports = function (router, models, passport) {

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
          console.log(user);
          return res.redirect('/#/doctor/' + user.uid);
        });
      })(req, res, next);
    });
  };
}());
