# Drupal Orange Project Template

This project template should provide a kickstart for managing your site
dependencies with [Composer](https://getcomposer.org/).

Note: Currently this is only tested with Composer 1.x compatibility. Composer
2.x compatibility is on the roadmap shortly.

## Usage

First you need to [install composer](https://getcomposer.org/doc/00-intro.md#installation-linux-unix-osx).

> Note: The instructions below refer to the [global composer installation](https://getcomposer.org/doc/00-intro.md#globally).
You might need to replace `composer` with `lando composer` (or similar)
for your setup.

After that you can create the project:

```
composer create-project acromedia/drupal-orange-project some-dir --stability dev --no-interaction
```

With `lando composer require ...` you can download new dependencies to your
installation.

```
cd some-dir
composer require drupal/devel:~1.0
```

The `composer create-project` command passes ownership of all files to the
project that is created. You should create a new git repository, and commit
all files not excluded by the .gitignore file.

## Orange Profiles

> Some documentation to help you get started.

Starting a Drupal build with Drupal Commerce?
* [Orange E-Commerce Profile](https://github.com/AcroMedia/orange_ecom_profile/blob/8.x-1.x/README.md)
* [Orange E-Commerce Starter Theme](https://github.com/AcroMedia/orange_ecom_starter/blob/8.x-1.x/README.md)

Starting a Drupal build that doesn't need Drupal Commerce?
* [Orange Profile](https://github.com/AcroMedia/orange_profile/blob/8.x-1.x/README.md)
* [Orange Starter Theme](https://github.com/AcroMedia/orange_starter/blob/8.x-1.x/README.md)

## Applied Patches

* Drupal Core
  * [Issue](https://www.drupal.org/project/drupal/issues/2771837) | [Patch](https://www.drupal.org/files/issues/2018-09-13/drupalimage_ckeditor-2771837-34.patch) - Problem with CKEditor not maintain data-entity attributes.
* CKEditor Font Size and Family
  * [Issue](https://www.drupal.org/project/ckeditor_font/issues/2729087) | [Patch](https://www.drupal.org/files/issues/2018-09-27/2729087_ckeditor_font_file_path.patch) - Path to plugin is incorrect unless base path is /.
* Commerce Google Tag Manager
  * [Issue](https://www.drupal.org/project/commerce_google_tag_manager/issues/3066949) | [Patch](https://www.drupal.org/files/issues/2020-03-27/use-product-variation-sku-if-available-3066949-7-alpha3.patch) - Use product variation SKU if available instead of product ID.

## Applied Web Libraries

- [CKEditor Media Embed Plugin](https://www.drupal.org/project/ckeditor_media_embed)
  - `ckeditor/ckeditor`
  - `/web/libraries/ckeditor`
- [CKEditor Color Button](https://www.drupal.org/project/colorbutton)
  - `ckeditor/colorbutton`
  - `/web/libraries/colorbutton`
- [CKEditor Font](https://www.drupal.org/project/ckeditor_font)
  - `ckeditor/font`
  - `/web/libraries/font`
- [CKEditor Panel Button](https://www.drupal.org/project/panelbutton)
  - `ckeditor/panelbutton`
  - `/web/libraries/panelbutton`
- [Spectrum for Color Field](https://www.drupal.org/project/color_field)
  - `bgrins/spectrum`
  - `/web/libraries/spectrum`
- [Magnific Popup](https://www.drupal.org/project/magnific_popup)
  - `dimsemenov/magnific-popup`
  - `/web/libraries/magnific-popup`

## What does the template do?

When installing the given `composer.json` some tasks are taken care of:

* Drupal will be installed in the `web`-directory.
* Autoloader is implemented to use the generated composer autoloader in `vendor/autoload.php`,
  instead of the one provided by Drupal (`web/vendor/autoload.php`).
* Modules (packages of type `drupal-module`) will be placed in `web/modules/contrib/`
* Theme (packages of type `drupal-theme`) will be placed in `web/themes/contrib/`
* Profiles (packages of type `drupal-profile`) will be placed in `web/profiles/contrib/`
* Creates default writable versions of `settings.php` and `services.yml`.
* Creates `web/sites/default/files`-directory.
* Latest version of drush is installed locally for use at `vendor/bin/drush`.
* Latest version of DrupalConsole is installed locally for use at `vendor/bin/drupal`.

## Updating Drupal Core

This project will attempt to keep all of your Drupal Core files up-to-date; the
project [drupal/core-composer-scaffold](https://github.com/drupal/core-composer-scaffold)
is used to ensure that your scaffold files are updated every time drupal/core is
updated. If you customize any of the "scaffolding" files (commonly .htaccess),
you may need to merge conflicts if any of your modified files are updated in a
new release of Drupal core.

Follow the steps below to update your core files.

1. Run `composer update drupal/core-recommended --with-dependencies` to update Drupal Core and its dependencies.
2. Next, apply any required database updates using `drush updb` and clear the cache using `drush cr`.
3. Make sure to export the config with `drush cex` after the database update because some core updates may change the
structure of the config files or introduce new values to them. Add the option `--diff` to view actual changes.
4. Run `git diff` to determine if any of the scaffolding files have changed.
   Review the files for any changes and restore any customizations to
  `.htaccess` or `robots.txt`.
5. Commit everything all together in a single commit, so `web` will remain in
   sync with the `core` when checking out branches or running `git bisect`.
6. In the event that there are non-trivial conflicts in step 4, you may wish
   to perform these steps on a branch, and use `git merge` to combine the
   updated core files with your customized files. This facilitates the use
   of a [three-way merge tool such as kdiff3](http://www.gitshah.com/2010/12/how-to-setup-kdiff-as-diff-tool-for-git.html). This setup is not necessary if your changes are simple;
   keeping all of your modifications at the beginning or end of the file is a
   good strategy to keep merges easy.

## Generate composer.json from existing project

With using [the "Composer Generate" drush extension](https://www.drupal.org/project/composer_generate)
you can now generate a basic `composer.json` file from an existing project. Note
that the generated `composer.json` might differ from this project's file.

## FAQ

### Should I commit the contrib modules I download?

Composer recommends **no**. They provide [argumentation against but also
workrounds if a project decides to do it anyway](https://getcomposer.org/doc/faqs/should-i-commit-the-dependencies-in-my-vendor-directory.md).

### Should I commit the scaffolding files?

The [Drupal Composer Scaffold](https://github.com/drupal/core-composer-scaffold) plugin can download the scaffold files (like
index.php, update.php, …) to the web/ directory of your project. If you have not customized those files you could choose
to not check them into your version control system (e.g. git). If that is the case for your project it might be
convenient to automatically run the drupal-scaffold plugin after every install or update of your project. You can
achieve that by registering `@composer drupal:scaffold` as post-install and post-update command in your composer.json:

```json
"scripts": {
    "post-install-cmd": [
        "@composer drupal:scaffold",
        "..."
    ],
    "post-update-cmd": [
        "@composer drupal:scaffold",
        "..."
    ]
},
```

### How can I apply patches to downloaded modules?

If you need to apply patches (depending on the project being modified, a pull
request is often a better solution), you can do so with the
[composer-patches](https://github.com/cweagans/composer-patches) plugin.

To add a patch to drupal module foobar insert the patches section in the extra
section of composer.json:

```json
"extra": {
    "patches": {
        "drupal/foobar": {
            "Patch description": "URL or local path to patch"
        }
    }
}
```

### How do I switch from packagist.drupal-composer.org to packages.drupal.org?

Follow the instructions in the [documentation on drupal.org](https://www.drupal.org/docs/develop/using-composer/using-packagesdrupalorg).

### How do I specify a PHP version?

This project supports PHP 7.2 as minimum version (see [Drupal 8 PHP requirements](https://www.drupal.org/docs/8/system-requirements/drupal-8-php-requirements)), however it's possible that a `composer update` will upgrade some package that will then require PHP 7+.

To prevent this you can add this code to specify the PHP version you want to use in the `config` section of `composer.json`:

```json
"config": {
    "sort-packages": true,
    "platform": {
        "php": "7.3"
    }
},
```
