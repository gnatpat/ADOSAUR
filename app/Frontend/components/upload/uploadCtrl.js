(function (){
  'use strict';
  var adosaur = angular.module('adosaur')
  adosaur.controller('uploadCtrl', ['$scope', 'Upload', '$timeout', function ($scope, Upload, $timeout) {
    $scope.uploadPic = function(file) {
	    file.upload = Upload.upload({
	      url: 'upload',
	      data: {file: file, username: $scope.username},
	    });

	    file.upload.then(function (response) {
	      $timeout(function () {
	        file.result = response.data;
	      });
	    }, function (response) {
	      if (response.status > 0)
	        $scope.errorMsg = response.status + ': ' + response.data;
	    }, function (evt) {
	      // Math.min is to fix IE which reports 200% sometimes
	      file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
	    });
    }
  }]);
}());
  