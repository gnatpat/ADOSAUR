(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('uploadCtrl', ['$scope', 'Upload', '$timeout', '$location', function ($scope, Upload, $timeout, $location) {
    var dlevels = {
      "0": "Minimal depression",
      "1": "Mild depression",
      "2": "Moderate depression",
      "3": "Severe depression",
      "-1": "Test not done yet"
    };
    $scope.prediction = dlevels[$location.search().prediction];

  }]);
}());
