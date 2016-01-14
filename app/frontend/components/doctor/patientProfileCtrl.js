(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('patientProfileCtrl', ['$scope', 'util', '$stateParams', '$http',
    function ($scope, util, $stateParams, $http) {
      console.log('IN Patient Profile controller');
      var dlevels = {
        "0": "Minimal depression",
        "1": "Mild depression",
        "2": "Moderate depression",
        "3": "Severe depression",
        "-1": "Test not done yet"
      };
      util.getCurrentUser(function (user) {
        $scope.doctor = user.user;
      });
      util.getPatient($stateParams.pid, function (res) {
        $scope.patient = res.user;
        console.log($scope.patient._id);
        util.getPatientTests($scope.patient._id, function (data) {
          var l = data.tests.length,
            i = 0;
          $scope.tests = data.tests;
          //  get test information
          for (i; i < l; i += 1) {
            $scope.tests[i].result = dlevels[$scope.tests[i].result];
          }
        });
      });
    }]);
}());
