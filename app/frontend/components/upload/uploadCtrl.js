(function (){
  'use strict';
  var adosaur = angular.module('adosaur')
  adosaur.controller('uploadCtrl', ['$scope', 'Upload', '$timeout', '$location', function ($scope, Upload, $timeout, $location) {

    $scope.prediction = $location.search().prediction;

  }]);
}());
