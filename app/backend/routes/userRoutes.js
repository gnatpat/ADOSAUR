/*jslint node: true, nomen: true */

/* Immediately-invoked function (containing all other functions) - invokes strict mode globally */
(function () {
  'use strict';

  module.exports = function (router, models, passport) {
    var
      User = models.user,
      Record = models.record;

    router.get('/users/all', function (req, res) {
      User.find(function (err, users) {
        if (err) {
          res.status(500).json({ error: "Error in getting all users" });
        }
        res.status(200).json({
          users: users
        });
      });
    });

    router.get('/users/current', function (req, res) {
      res.status(200).json({
        found: (req.user !== undefined),
        user: req.user
      });
    });

    router.put('/user/new', function (req, res) {
      var user    = new User();
      user.uid    = req.body.uid;
      user.pwd    = req.body.pwd;
      user.email  = req.body.email;
      user.doctor = req.body.doctor;
      user.save(function (err) {
        if (err) {
          console.log("here");
          res.status(500).json({
            error: "Failed to created User"
          });
        }
        res.status(200).json({
          message: "User created successfully"
        });
      });
    });
  };
}());
