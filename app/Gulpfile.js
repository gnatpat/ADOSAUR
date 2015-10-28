var gulp = require('gulp'),
  shell = require('gulp-shell');

gulp.task('default', ['restart', 'watch']);

/* restarts server */
gulp.task('restart', shell.task([
  'http-server -a localhost -p 8100 -c-1'
]));

/* listens for changes in files */
gulp.task('watch', function () {
  gulp.watch('js/*.js', ['restart'])
});
