
var app = angular.module( 'myApp', [] );


app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.controller( 'MainCtrl', function($scope, $http) {
    $scope.actions = []
    $scope.identities = []
    $scope.following = []
    $scope.followinggraph = null

    $scope.getActions = function(){
      $http.get('actions').then(function(response) {
        $scope.actions = response.data.actions;
        });
    };
    $scope.getIdentities = function(){
      $http.get('identities').then(function(response) {
        $scope.identities = response.data.identities;
        });

    };
    $scope.getFollowing = function(){
      $http.get('following').then(function(response) {
        $scope.following = response.data.following;
        });
    };
    $scope.getExceptions = function(){
      $http.get('exceptions').then(function(response) {
        $scope.exceptions = response.data.exceptions;
        });
    };
    $scope.getExceptionSummary = function(){
      $http.get('exceptionsummary').then(function(response) {
        $scope.exceptionsummary = response.data.exceptionsummary;
        });
    };
    $scope.getFollowingGraph = function(){
      $http.get('followinggraph').then(function(response) {
        g = response.data.followinggraph;
        console.log(g);
        $scope.followinggraph = g;
        sys.graft(g);
      });
    };
    $scope.getLists = function(){

    };
    $scope.getUser = function(){

    };

    $scope.init = function(){
        $scope.getActions()
        $scope.getIdentities()
        $scope.getExceptionSummary()
        $scope.getExceptions()
        $scope.getFollowing()
        $scope.getFollowingGraph()


    };
    $scope.init()


});
