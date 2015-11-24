(function (){
  'use strict';
  var adosaur = angular.module('adosaur')
  adosaur.controller('uploadCtrl', ['$scope', 'Upload', '$timeout', function ($scope, Upload, $timeout) {
    $scope.resultMsg = "Please upload a file first"
    $scope.uploadAudio = function(file) {
	    file.upload = Upload.upload({
	      url: 'upload',
	      data: {file: file},
	    });

	    file.upload.then(function (response) {
	      $timeout(function () {
	        file.result = response.data;
	      });

          var data = response.data.data
          displayChart(data);
	    }, function (response) {
	      if (response.status > 0)
	        $scope.errorMsg = response.status + ': ' + response.data;
	    });
    }


    function displayChart(data) { 
      $('#graph').css("display","block");
      $('#graph').highcharts({
        chart: {
          type: 'column'
        },
        title: {
          text: "Depression Probabilities"
        },
        subtitle: {
          text: "According to the Beck Depression Inventory"
        },
        xAxis: {
          categories: [
            "Minimal",
            "Mild",
            "Moderate",
            "Severe"
          ]
        },
        yAxis: {
          min: 0,
          max: 1,
          title: {
            text: "Probability"
          }
        },
        series: [{
          name: 'Depression Probability',
          colour: 'blue',
          data: data
        }]
      });
    };
  }]);
}());
