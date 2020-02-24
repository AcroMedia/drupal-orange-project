from invoke import task
import boto3

@task
def start(c):
    """
    Starts the development containers
    """
    c.run('lando start')

@task
def update(c):
    """
    Pull down and update all content, including database and files.
    """
    c.run('authenticate-aws-mfa.sh', pty=True, warn=True)
    s3 = boto3.resource('s3')
    s3.meta.client.download_file('acro-dev-databases', 'Server/AROAIDGM7II4MQTJBBDQQ:INSTANCE_ID/database.sql.gz', 'database.sql.gz')
    c.run('lando db-import database.sql.gz')
    # add file syncs or other pulls here
    c.run("aws s3 sync s3://acro-dev-databases/Server/AROAIDGM7II4MQTJBBDQQ:i-0d36e73583f1b2a8a/images web/images")
    c.run('lando drush cr')

@task
def drush(c, command):
    """
    Pipes drush commands into the container
    """
    c.run("lando drush {}".format(command), pty=True)

@task()
def init(c):
    """
    Creates an initial Drupal Orange product in a 'web' subdirectory
    """
    if confirm() != True:
        return
    
    site_name = input("Site Name [Orange]:")
    if site_name == "":
        site_name = "Orange"
    email = input("Email:")
    profile = input("Profile\n 1. Orange \n 2. Orange Ecom \n [2]:")
    if profile == 1:
        profile = "orange_profile"
    if profile == 2 or profile == "":
        profile = "orange_ecom_profile"

    c.run("git clone --depth=1 https://github.com/AcroMedia/drupal-orange-project.git scaffold")
    c.run("rm scaffold/.git -rf")
    c.run("mv scaffold/.[!.]* .")
    c.run("mv scaffold/* .")
    c.run("rm scaffold -rf")
    start(c)
    c.run("lando ssh -c 'composer install'")
    c.run("lando drush si {} --db-url=mysql://drupal8:drupal8@database/drupal8 --account-mail={}".format(profile, email), pty=True)
    solr_config(c)

@task(pre=[start, update])
def setup(c):
    """
    Sets up the containers, downloads dependencies and updates content
    """
    c.run("lando ssh -c 'composer install'")
    solr_config(c)

def confirm():
    confirm = input("This operation will setup a new Drupal Orange project, are you sure you want to proceed [y/N]")
    if confirm.lower() == 'y':
        return True
    return False

@task
def solr_config(c):
    c.run("lando drush solr-gsc solr ../solr-config.zip")
    c.run("lando ssh -c 'unzip solr-config.zip -d solr-config'")
    c.run("touch solr-config/mapping-ISOLatin1Accent.txt")
    c.run("touch solr-config/synonyms.txt")
    c.run("touch solr-config/stopwords.txt")
    c.run("touch solr-config/protwords.txt")
    c.run("lando ssh -s search -c 'solr create_core -c orange -d solr-config'")
    c.run("rm solr-config -rf")