/*jslint node: true*/
(function () {
  'use strict';
  module.exports = function (grunt) {
    grunt.initConfig({
      nodemon: {
        dev: {
          script: 'server.js',
          options: {
            args: ['offline']
          }
        }
      }
    });

    grunt.loadNpmTasks('grunt-nodemon');
    grunt.registerTask('run', ['nodemon']);
  };
}());
