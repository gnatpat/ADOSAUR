(function () {
  'use strict';

  var mailer = require('../email.js'), // to send emails
    ip     = require('ip');

  module.exports = function (router, models, passport) {
    var Test = models.test,
      User   = models.user,
      Text   = models.text,
      findDoc;

    findDoc = function (id, type) {
      console.log('ID: ', id);
      var res;
      if (type === "user") {
        User.findOne({"_id": id}, function (err, user) {
          if (err) { return -1; }
          res = user;
          console.log('User (res): ', res);
        });
      } else {
        Text.findOne({"_id": id}, function (err, text) {
          if (err) { return -1; }
          res = text;
        });
      }
      return res;
    };

    router.put('/test/send/', function (req, res) {
      console.log(ip.address());
      var test = new Test();
      test.doctor  = req.body.doctor;
      test.patient = req.body.patient;
      test.text    = req.body.test.textID;
      test.type    = req.body.test.type;
      test.result  = 5;

      test.save(function (err, test) {
        if (err) {
          res.status(500).json({error: 'Failed to create test'});
        }
        var link = 'http://' + ip.address() + ':8080/#/test/' + test._id;
        mailer.sendMail({
          to: req.body.to,
          subject: 'Test',
          text: req.body.test.emailMsg + '   ' + link
        });
        res.status(200).json({meassage: 'Created test and sent email'});
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
  };
}());
