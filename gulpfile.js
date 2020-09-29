const gulp = require('gulp');
const sass = require('gulp-sass');
const clean = require('gulp-clean');
const webpack = require('webpack-stream');
const package = require('./package.json');
const browserSync = require('browser-sync').create();

/**
 * final place for front end css, js and assets
 */
const assetsFolder = 'cms/static';

/* Remove all files from /cms/static/ */
const cleanStatic = () => {
  return gulp.src(assetsFolder, { allowEmpty: true })
    .pipe(clean())
}

/* Build the CSS from source packages without compression */
const compileCSS = () => {
  return gulp.src(['packages/nhsuk.scss'])
    .pipe(sass())
    .pipe(gulp.dest(assetsFolder + '/css/'))
    .on('error', (err) => {
      console.log(err)
      process.exit(1)
    })
    .pipe(browserSync.reload({
      stream: true
    }))
}

/**
 * Build the CSS from source packages with compression
 * only differnce here is outputStyle = compressed
 */

const compressCSS = () => {
  return gulp.src(['packages/nhsuk.scss'])
    .pipe(sass({
      outputStyle: 'compressed'
    }))
    .pipe(gulp.dest(assetsFolder + '/css/'))
    .on('error', (err) => {
      console.log(err)
      process.exit(1)
    })
    .pipe(browserSync.reload({
      stream: true
    }))
}

/* Use Webpack to build the components JS. */
const webpackJS = () => {
  return gulp.src('./packages/nhsuk.js')
    .pipe(webpack({
      mode: 'development',
      output: {
        filename: 'nhsuk.js',
      },
      target: 'web',
      module: {
        rules: [
          {
            use: {
              loader: 'babel-loader',
              options: {
                presets: ['@babel/preset-env']
              }
            }
          }
        ]
      }
    }))
    .pipe(gulp.dest(assetsFolder + '/js/'));
}

/* Use Webpack to build and minify the components JS. */
// only differnce here is the mode = production
const webpackJSProd = () => {
  return gulp.src('./packages/nhsuk.js')
    .pipe(webpack({
      mode: 'production',
      output: {
        filename: 'nhsuk.js',
      },
      target: 'web',
      module: {
        rules: [
          {
            use: {
              loader: 'babel-loader',
              options: {
                presets: ['@babel/preset-env']
              }
            }
          }
        ]
      }
    }))
    .pipe(gulp.dest(assetsFolder + '/js/'));
}

/* Copy assets folder (favicons, icons, logoso into static */
const assets = () => {
  return gulp.src('packages/assets/**')
    .pipe(gulp.dest(assetsFolder + '/assets/'))
}

/* start browserSync and watch processes */
const serve = () => {
  browserSync.init({
    proxy: "127.0.0.1:8000",
    open: false
  });
  gulp.watch("packages/**/*.scss", compileCSS);
  gulp.watch(['packages/**/*.js'], webpackJS).on("change", browserSync.reload);
  gulp.watch(["cms/**/*.html", "cms/**/*.py"]).on("change", browserSync.reload);
  gulp.watch(["core/**/*.html", "core/**/*.py"]).on("change", browserSync.reload);
};

/**
 * set a default method
 * npm start for dev
 * npm run build to compress
 */
exports.default = gulp.series(cleanStatic, assets, webpackJS, compileCSS, serve);
exports.build = gulp.series(cleanStatic, assets, webpackJSProd, compressCSS,);