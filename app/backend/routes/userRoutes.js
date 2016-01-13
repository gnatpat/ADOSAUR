/*jslint node: true, nomen: true */

/* Immediately-invoked function (containing all other functions) - invokes strict mode globally */
(function () {
  'use strict';

  module.exports = function (router, models, passport) {
    var
      User = models.user,
      Text = models.text;

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
    router.get('/user/id/:_id', function (req, res) {
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

    router.get('/user/delete/:doctor/:id', function (req, res) {
      var id = req.params.id,
        doctor = req.params.doctor;
      console.log('Deleting: ', id);
      console.log('doctor: ', doctor);
      User.findByIdAndUpdate(doctor, {$pull : { "patients": id}},
        function (err) {
          if (err) {
            res.status(500).json({error: "Failed to delete patient from doctor's list"});
          }
          // if doctor's patients list correctly updated then delete patient from DB
          User.remove({"_id": id}, function (err) {
            if (err) {
              res.status(500).json({error: "Failed to delete patient form DB"});
            }
          });
          res.status(200).json({message: "Patient removed from DB"});
        });
    });

    /* gets the current user's information */
    router.get('/users/current', function (req, res) {
      var isFound = req.user !== undefined ? 1 : 0;
      res.status(200).json({
        found: isFound,
        user: req.user
      });
    });

    // gets the current user's patients
    router.post('/users/current/patients',
      passport.isAuthenticated,
      function (req, res) {
        User.find({ "_id" : { $in: req.body}},
          function (err, docs) {
            if (err) {
              res.status(500).json({ error: "Failed to retrieve patients"});
            }
            res.status(200).json({patients: docs});
          });
      });

    // gets the current user's texts
    router.post('/users/current/texts',
      passport.isAuthenticated,
      function (req, res) {
        Text.find({ "_id" : { $in: req.body}},
          function (err, docs) {
            if (err) {
              res.status(500).json({ error: "Failed to retrieve texts"});
            }
            res.status(200).json({texts: docs});
          });
      });

    /* Adds a new patient to the database and adds its _id to the doctor's
       patient list */
    router.put('/add/user/:doctor', function (req, res) {
      console.log('Adding new Patient for: ' + req.params.doctor);
      var p  = req.body.patient,
        user = new User();
      if (!p.profile_pic) {
        p.profile_pic = "./assets/img/default_profile.png";
      }
      // create the new patient
      user.first_name  = p.first_name;
      user.last_name   = p.last_name;
      user.doctor      = false;
      user.email       = p.email;
      user.dob         = p.dob;
      user.profile_pic = p.profile_pic;
      // Save new patient to database
      user.save(function (err, user) {
        // if an error occurs
        if (err) {
          res.status(500).json({
            error: "Failed to created new patient"
          });
        } else {
          // if no error, add new patient's _id to the doctor who added him
          User.findByIdAndUpdate(req.params.doctor,
            { $push: {"patients": user._id}},
            {safe: true, upsert: true, new : true},
            function (err) {
              if (err) {
                res.status(500).json({error: "Failed to update doctor's patients list"});
              }
            });
          res.status(200).json({
            patient: user,
            message: "User created successfully and added to doctor " + req.params.doctor
          });
        }
      });
    });
  };
}());
