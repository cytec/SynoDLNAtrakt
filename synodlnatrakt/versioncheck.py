#  This file is part of Headphones.
#
#  Headphones is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Headphones is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Headphones.  If not, see <http://www.gnu.org/licenses/>.

import platform, subprocess, re, os, urllib2, tarfile

from lib import requests
from synodlnatrakt import config
from synodlnatrakt.logger import logger

user = "cytec"
branch = "master"

def runGit(args):
    
    git_locations = ['git']
          
    output = err = None
    
    for cur_git in git_locations:
    
        cmd = cur_git+' '+args
    
        try:
            logger.debug('Trying to execute: "' + cmd + '" with shell in ' + config.basedir)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=config.basedir)
            output, err = p.communicate()
            logger.debug('Git output: ' + output)
        except OSError:
            logger.debug('Command ' + cmd + ' didn\'t work, couldn\'t find git')
            continue
            
        if 'not found' in output or "not recognized as an internal or external command" in output:
            logger.debug('Unable to find git with command ' + cmd)
            output = None
        elif 'fatal:' in output or err:
            logger.error('Git returned bad info. Are you sure this is a git installation?')
            output = None
        elif output:
            break
            
    return (output, err)
            
def getVersion():

    if os.path.isdir(os.path.join(config.basedir, '.git')):
    
        output, err = runGit('rev-parse HEAD')
        
        if not output:
            logger.error('Couldn\'t find latest installed version.')
            return None
            
        cur_commit_hash = output.strip()
        
        if not re.match('^[a-z0-9]+$', cur_commit_hash):
            logger.error('Output doesn\'t look like a hash, not using it')
            return None
        
        config.current_version = cur_commit_hash
        return cur_commit_hash

        
    else:
        
        return None
    
def checkGithub():

    # Get the latest commit available from github
    url = 'https://api.github.com/repos/%s/synodlnatrakt/commits/%s' % (user, branch)
    logger.info ('Retrieving latest version information from github')

    try:
        result = requests.get(url)
        config.latest_version = result.json["sha"]
    except:
        logger.warn('Could not get the latest commit from github')
        config.commits_behind = 0
        return config.current_version
    
    # See how many commits behind we are    
    if config.current_version:
        logger.info('Comparing currently installed version with latest github version')
        url = 'https://api.github.com/repos/%s/synodlnatrakt/compare/%s...%s' % (user, config.current_version, config.latest_version)
        
        try:
            result = requests.get(url)
            config.commits_behind = result.json['total_commits']
        except:
            logger.warn('Could not get commits behind from github')
            config.commits_behind = 0
            return config.current_version
            
        if config.commits_behind >= 1:
            logger.info('New version is available. You are %s commits behind' % config.commits_behind)
        elif config.commits_behind == 0:
            logger.info('SynoDLNAtrakt is up to date')
        elif config.commits_behind == -1:
            logger.info('You are running an unknown version of SynoDLNAtrakt. Run the updater to identify your version')
            
    else:
        logger.info('You are running an unknown version of SynoDLNAtrakt. Run the updater to identify your version')
    
    return config.latest_version
        
def update():

       
    output, err = runGit('pull origin ' + branch)
    
    if not output:
        logger.error('Couldn\'t download latest version')
        
    for line in output.split('\n'):
    
        if 'Already up-to-date.' in line:
            logger.info('No update available, not updating')
            logger.info('Output: ' + str(output))
        elif line.endswith('Aborting.'):
            logger.error('Unable to update from git: '+line)
            logger.info('Output: ' + str(output))
            
    