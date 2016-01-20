(function () {
  'use strict';

  /* Passport strategy configuration files. Configure the different
   * authentication strategies here
   TODO: implement other strategies? 
   */

  var LocalStrategy = require('passport-local');
  module.exports = function (passport, models) {
    var User = models.user;

    passport.serializeUser(function (user, done) {
      done(null, user._id);
    });

    passport.deserializeUser(function (id, done) {
      User.findOne({ _id: id }, function (err, user) {
        done(err, user);
      });
    });

    passport.use(new LocalStrategy(
      function (username, password, done) {
        User.findOne({ 'uid': username }, function (err, user) {
          if (err) { return done(err); }
          if (!user) { return done(null, false, {message: "1"}); }
          if (!user.validPassword(password)) {
            return done(null, false, {message: "2"});
          }
          // if no errors and correct username/pwd return user
          return done(null, user);
        });
      }
    ));

    // check if current user is authenticated
    passport.isAuthenticated = function (req, res, next) {
      if (req.isAuthenticated()) {
        return next();
      }
      res.status(401).json({
        error: 'Not authenticated'
      });
    };
  };
}());
