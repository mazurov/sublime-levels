module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    compress: {
      main: {
        options: {
          mode: 'zip',
          archive: "build/Levels.sublime-package"
        },
        files: [
          {
            expand: true,
            src: ['**', '!build/**', '!node_modules/**', '!package.json', '!Gruntfile.js']
          }
        ]
      }
    },
    copy: {
      main : {
        files: [
          { 
            expand: true,
            cwd: "build",
            src:'Levels.sublime-package',
            dest: "/home/amazurov/.config/sublime-text-3/Installed Packages/"
          }
        ]
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-compress');
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Default task(s).
  grunt.registerTask('default', ['compress', 'copy']);

};