(function () {
  // DO NOT PUT A STRICT MODE HERE
  var spawn = require('child_process').spawn;

  module.exports = {

    evaluateBDI: function (filePath, callback) {
      console.log("Filename: " + filePath.split('/')[3]);
      eval = spawn("./evaluateBDI.sh", ['tmp/' + filePath.split('/')[3]], {'cwd': '../..'});

      eval.stdout.on('data', function (data) {
        console.log("Script gave " + data);
        data = String(data);
        data = data.substring(1, data.length - 1)
        split = data.split(" ");
        values = []
        for (var i = 0; i < split.length; i++)
        {
          var value = parseFloat(split[i]);
          if(isNaN(value))
            continue;
          values.push(value);
        }
        console.log(values);
        callback(values);
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
