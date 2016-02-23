/*global module:false*/
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    // Task configuration.
    jsdoc: {
      services: {
        src: ['services/*.js', 'services/README.md'],
        options: {
          destination: 'doc/services',
          template: "node_modules/ink-docstrap/template",
          configure: "config/jsdoc/jsdoc-services.conf.json"
        }
      },
      commons: {
        src: ['modules/common/*.js', 'modules/common/README.md'],
        options: {
          destination: 'doc/commons',
          template: "node_modules/ink-docstrap/template",
          configure: "config/jsdoc/jsdoc-commons.conf.json"
        }
      },
      templates: {
        src: ['services/templates/*.js', 'services/templates/README.md'],
        options: {
          destination: 'doc/templates',
          template: "node_modules/ink-docstrap/template",
          configure: "config/jsdoc/jsdoc-templates.conf.json"
        }
      }
    },
    shell: {
      options: {
        stderr: true,
        stdout: true
      },
      init_hop: {
        command: './run.sh'
      },
      clean_doc: {
        command: 'rm -rf doc/'
      }
    }
  });

  // Load jsdoc grunt task.
  grunt.loadNpmTasks('grunt-jsdoc');
  // Load shell grunt task
  grunt.loadNpmTasks('grunt-shell');

  // Generate documentation for all task.
  grunt.registerTask('doc-gen',
    ['jsdoc:services', 'jsdoc:commons','jsdoc:templates']);

  // Generate documentation for HOP Services
  grunt.registerTask('doc-gen-services', ['jsdoc:services']);

  // Generate documentation for common include modules
  grunt.registerTask('doc-gen-commons', ['jsdoc:commons']);

  // Generate documentation for HOP Services Creation Templates
  grunt.registerTask('doc-gen-templates', ['jsdoc:templates']);

  grunt.registerTask('clean-doc', ['shell:clean_doc']);

  // Initiate HOP task
  grunt.registerTask('init-hop', ['shell:init_hop']);

};
