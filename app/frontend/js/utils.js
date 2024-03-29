(function () {
  'use strict';
  var app = angular.module('adosaur');

  app.factory('util', ['$http', function ($http) {
    var
      util = {},
      currentUser;

    util.getCurrentUser = function (callback, error) {
      // if (currentUser) {
      //   return currentUser;
      // }
      var rp = $http.get('/api/users/current');

      rp.success(function (data, status, headers, config) {
        currentUser = data;
        if (callback) {
          callback(currentUser);
        }
      });

      rp.error(function (data, status, headers, config) {
        if (error) {
          error(data);
        }
      });
    };

    util.getPatient = function (patientID, callback) {
      var rp = $http.get('/api/user/id/' + patientID);
      rp.success(function (data, status, headers, config) {
        if (callback) {
          callback(data);
        }
      });
      rp.error(function (data, status, headers, config) {
        console.log('UTILS: failed to retrieve patient');
      });
    };

    util.getUserPatients = function (patientIDs, callback, error) {
      var rp = $http.post('/api/users/current/patients', patientIDs);

      rp.success(function (data, status, headers, config) {
        if (callback) {
          callback(data);
        }
      });

      rp.error(function (data, status, headers, config) {
        console.log('UTILS: Failed to retrieve Patients');
      });
    };

    util.getUserTexts = function (textIDs, callback, error) {
      var rp = $http.post('/api/users/current/texts', textIDs);

      rp.success(function (data, status, headers, config) {
        if (callback) {
          callback(data);
        }
      });

      rp.error(function (data, status, headers, config) {
        console.log('Failed to retrieve Texts');
      });
    };

    util.getPatientTests = function (patientID, callback) {
      var rp = $http.get('/api/patient/tests/' + patientID);
      rp.success(function (data, status, headers, config) {
        if (callback) {
          callback(data);
        }
      });
      rp.error(function (data, status, headers, config) {
        console.log("UTILS: failed to get patient's test");
      });
    };

    return util;
  }]);
}());
