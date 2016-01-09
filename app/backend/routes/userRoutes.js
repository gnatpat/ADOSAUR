/*jslint node: true, nomen: true */

/* Immediately-invoked function (containing all other functions) - invokes strict mode globally */
(function () {
  'use strict';

  module.exports = function (router, models, passport) {
    var
      User = models.user,
      Record = models.record;

    /* retrieves all users from database */
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

    /* get a single user by its uid */
    router.get('/user/:uid', function (req, res) {
      User.findOne({uid: req.params.uid}, function (err, user) {
        if (err) {
          res.status(500).json({
            error: "could not retrieve user by uid"
          });
        }
        res.status(200).json({
          user: user
        });
      });
    });

    /* get a single user by its uid */
    router.get('/user/:_id', function (req, res) {
      User.findOne({_id: req.params._id}, function (err, user) {
        if (err) {
          res.status(500).json({
            error: "could not retrieve user by _id"
          });
        }
        res.status(200).json({
          user: user
        });
      });
    });

    router.get('/users/current', function (req, res) {
      var isFound = req.user !== undefined ? 1 : 0;
      res.status(200).json({
        found: isFound,
        user: req.user
      });
    });

    router.put('/user/new', function (req, res) {
      var user    = new User();
      user.uid    = req.body.uid;
      user.pwd    = req.body.pwd;
      user.email  = req.body.email;
      user.doctor = req.body.doctor;
      user.first_name = req.body.first_name;
      user.last_name = req.body.last_name;
      user.save(function (err) {
        if (err) {
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
