(function () {
  'use strict';

  var mailer = require('../email.js'), // to send emails
    ip     = require('ip');

  module.exports = function (router, models, passport) {
    var Test = models.test,
      User   = models.user,
      Text   = models.text;

    // create new test and send link by email
    router.put('/test/send/', function (req, res) {
      var test = new Test();
      test.doctor  = req.body.doctor;
      test.patient = req.body.patient;
      test.text    = req.body.test.textID;
      test.type    = req.body.test.type;
      test.result  = -1;
      test.seen    = false;
      test.done    = false;

      test.save(function (err, test) {
        if (err) {
          res.status(500).json({error: 'Failed to create test'});
        }
        // add the test id to the patient's tests list
        User.findByIdAndUpdate(test.patient,
          { $push: {"tests": test._id}},
          {safe: true, upsert: true, new : true},
          function (err) {
            if (err) {
              res.status(500).json({error: "Failed to push test to patient's list"});
            }
          });
        // send test link to patient
        var link = 'http://' + ip.address() + ':8080/#/test/' + test._id;
        mailer.sendMail({
          to: req.body.to,
          subject: 'Test',
          text: req.body.test.emailMsg + '   ' + link
        });
        res.status(200).json({meassage: 'Created test and sent email'});
      });
    });

    router.get('/patient/tests/:patID', function (req, res) {
      User.findOne({"_id": req.params.patID}, function (err, patient) {
        if (err) {
          res.status(500).json({error: "Failed to find patient in find tests"});
        }
        Test.find({"_id": {$in: patient.tests}}, function (err, tests) {
          if (err) {
            res.status(500).json({error: "Failed to retrieve patient's tests"});
          }
          res.status(200).json({tests: tests});
        });
      });
    });
    // find test and return it with its real fields (not pointers)
    router.get('/test/:testID', function (req, res) {
      var testID = req.params.testID;
      Test.findOne({"_id": testID}, function (err, tst) {
        var pat, doc, txt;
        if (err) {
          return res.status(500).json({error: "Failed to get test"});
        }
        // find Patient
        User.findOne({"_id": tst.patient}, function (err, user1) {
          if (err) { return -1; }
          pat = user1;
          // find Doctor
          User.findOne({"_id": tst.doctor}, function (err, user2) {
            if (err) { return -1; }
            doc = user2;
            // find Text
            Text.findOne({"_id": tst.text}, function (err, doc1) {
              if (err) { return -1; }
              txt = doc1;
              if (pat === -1 || doc === -1) {
                return res.status(500).json({error: "failed to get test info"});
              }
              res.status(200).json({
                test: tst,
                patient: pat,
                doctor: doc,
                text: txt
              });
            });
          });
        });
      });
    });

    router.get('test/update/:testID', function (req, res) {
      Test.findByIdAndUpdate(req.params.testID, {$set: req.body},
        function (err) {
          if (err) {
            res.status(500).json({error: "Failed to update test"});
          }
          res.status(200).json({message: "Update test successfully"});
        });
    });
  };
}());
