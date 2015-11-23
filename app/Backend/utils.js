(function () {
  'use strict';
  var spawn = require('child_process').spawn;

  module.exports = {

    evaluateBDI: function (filePath, callback) {
      console.log("Filename: " + filePath.split('/')[3]);
      eval = spawn("./evaluateBDI.sh", ['tmp/' + filePath.split('/')[3]], {'cwd': '../..'});

      eval.stdout.on('data', function (data) {
        console.log("Script gave " + data);
        callback(String(data));
      });

      eval.stderr.on('data', function (data) {
        console.log("Script errored:  " + data);
      });

      eval.on("error", function (err) {
        console.log(err);
      });
    }
  };

}());
