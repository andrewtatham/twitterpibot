
var app = angular.module( 'myApp', [] );


app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.controller( 'MainCtrl', function($scope, $http) {
    console.log('status');
    $http.get('/status').then(function successCallback(response) {
        console.log(response);
        $scope.identities = response.data.result;
    });
});
