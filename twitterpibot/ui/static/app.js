
var app = angular.module( 'myApp', [] );


app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.controller( 'MainCtrl', function($scope, $http) {
    $http.get('init').then(function(response) {
        console.log(response);
        $scope.actions = response.data.result.actions;
        $scope.identities = response.data.result.identities;
    });
});
