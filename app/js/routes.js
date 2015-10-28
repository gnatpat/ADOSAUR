var adosaur = angular.module('adosaur');

adosaur.config(function($stateProvider, $urlRouterProvider){
  
  $urlRouterProvider.otherwise('/home');
  
  $stateProvider
    .state('home', {
      url: "/home",
      templateUrl: "components/home/home.html",
      controller: "homeCtrl"
  });
})