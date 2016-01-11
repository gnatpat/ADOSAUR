(function () {
  'use strict';
  var adosaur = angular.module('adosaur');
  adosaur.controller('doctorCtrl', ['$scope', '$stateParams', '$http', 'util',
    function ($scope, $stateParams, $http, util) {

      // jQuery modal plugin initialisation
      $(document).ready(function () {
        $('.modal-trigger').leanModal();
      });
      // jQuery datepicker initialisation
      $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 100 // Creates a dropdown of 15 years to control year
      });
      // get current user and retrieve his patients and texts
      util.getCurrentUser(function (user) {
        $scope.user = user;
        $scope.uid  = user.user.uid;
        // get current doctor's patients
        util.getUserPatients(user.user.patients, function (patients) {
          $scope.patients = patients.patients;
        });
        // get current doctor's patients
        util.getUserTexts(user.user.texts, function (texts) {
          $scope.texts = texts.texts;
        });
      }, null);

      // adds patient to current doctor
      $scope.addPatient = function () {
        var response = $http({
          method: 'PUT',
          url: '/api/add/user/' + $scope.user.user._id,
          data: {patient: $scope.newUser}
        });
        response.error(function (data, status, headers, config) {
          console.log('Failed to add new patient');
        });
      };

      $scope.addText = function () {
        console.log('Adding text: ', $scope.newText);
        var response = $http({
          method: 'PUT',
          url: '/api/add/text/' + $scope.user.user._id,
          data: {text: $scope.newText}
        });
        response.error(function (data, status, headers, config) {
          console.log('Failed to add new patient');
        });
      };

      // opens the modal containing the form to fill to send a test
      $scope.openSendTest = function (patient) {
        $scope.patient = patient;
        $('#send_test_modal').openModal();
      };

      // sends a test and closes the modal
      $scope.sendTest = function () {
        console.log("Sending test");
        console.log($scope.test);
        var response = $http({
          method: 'PUT',
          url: '/api/test/send',
          data: {
            test   : $scope.test,
            patient: $scope.patient._id,
            to     : $scope.patient.email,
            doctor : $scope.user.user._id
          }
        });
        response.error(function (data, status, headers, config) {
          console.log('Failed to send test to patient');
        });
      };

      // delete a user (from database)
      $scope.delete = function (id) {
        console.log('Deleting patient index', id);
        $http.get('/api/user/delete/' + $scope.user.user._id + '/' + id);
      };

      // edit patient information
      /* TODO: implement */
      $scope.edit = function (item) {
        console.log('Editing: ', item);
      };
      // sets the selected text in the send test form
      $scope.selectText = function (textID) {
        console.log('Selected text: ', textID);
        $scope.test.textID = textID;
      };
    }]);
}());
