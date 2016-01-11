(function () {
  'use strict';

  module.exports = function (router, models, passport) {
    var Text = models.text,
      User   = models.user;

    /* Adds a new text to the database and adds its _id to the doctor's
       text list */
    router.put('/add/text/:doctor', function (req, res) {
      console.log('Adding new Text for: ' + req.params.doctor);
      var t  = req.body.text,
        text = new Text();
      // create the new text
      text.title    = t.title;
      text.content  = t.content;
      text.comments = t.comments;
      // Save new patient to database
      text.save(function (err, text) {
        // if an error occurs
        if (err) {
          res.status(500).json({
            error: "Failed to created new text"
          });
        } else {
          // if no error, add new text's _id to the doctor who added him
          User.findByIdAndUpdate(req.params.doctor,
            { $push: {"texts": text._id}},
            {safe: true, upsert: true, new : true},
            function (err) {
              if (err) {
                res.status(500).json({error: "Failed to update doctor's texts list"});
              }
            });
          res.status(200).json({
            message: "Text created successfully and added to doctor " + req.params.doctor
          });
        }
      });
    });

    router.get('/delete/text/:doctor/:id', function (req, res) {
      var id = req.params.id,
        doctor = req.params.doctor;
      console.log('Deleting: ', id);
      console.log('doctor: ', doctor);
      User.findByIdAndUpdate(doctor, {$pull : { "texts": id}},
        function (err) {
          if (err) {
            res.status(500).json({error: "Failed to delete text from doctor's list"});
          }
          // if doctor's patients list correctly updated then delete patient from DB
          Text.remove({"_id": id}, function (err) {
            if (err) {
              res.status(500).json({error: "Failed to delete text form DB"});
            }
          });
          res.status(200).json({message: "Text removed from DB"});
        });
    });
  };
}());
