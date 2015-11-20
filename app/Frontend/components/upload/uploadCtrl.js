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

        $scope.resultMsg = "Your BDI is " + response.data.data;
	    }, function (response) {
	      if (response.status > 0)
	        $scope.errorMsg = response.status + ': ' + response.data;
	    });
    }
  }]);
}());
